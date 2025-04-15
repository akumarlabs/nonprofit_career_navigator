import pdfplumber
import docx
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from tenacity import retry, stop_after_attempt, wait_fixed
from playwright.async_api import async_playwright


class ResumeParser:
    """
    Parses resume content from PDF or DOCX file.
    """

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def __call__(self, file_path: str) -> str:
        if file_path.endswith(".pdf"):
            with pdfplumber.open(file_path) as pdf:
                return "\n".join(
                    page.extract_text() for page in pdf.pages if page.extract_text()
                )

        elif file_path.endswith(".docx"):
            doc = docx.Document(file_path)
            return "\n".join(para.text for para in doc.paragraphs)

        else:
            raise ValueError(f"Unsupported resume file type: {file_path}")


class JobDescriptionParser:
    async def __call__(self, source: str) -> str:
        if source.startswith("http"):
            return await self._parse_url(source)
        elif source.endswith(".pdf"):
            with pdfplumber.open(source) as pdf:
                return "\n".join(
                    page.extract_text() for page in pdf.pages if page.extract_text()
                )
        else:
            raise ValueError(f"Unsupported job source: {source}")

    async def _parse_url(self, url: str) -> str:
        HEADERS = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/121.0.0.0 Safari/537.36"
            ),
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;"
                "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
            ),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.google.com/",
            "Connection": "keep-alive",
            "DNT": "1",
            "Upgrade-Insecure-Requests": "1",
        }

        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text(separator="\n", strip=True)

            if len(text.strip()) < 200:
                print("⚠️ Falling back to Playwright: insufficient text")
                return await self._render_with_playwright(url)

            return text

        except Exception as e:
            print("⚠️ Falling back to Playwright due to error:", e)
            return await self._render_with_playwright(url)

    async def _render_with_playwright(self, url: str) -> str:
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, timeout=20000)
                await page.wait_for_timeout(3000)

                html = await page.content()
                await browser.close()

                soup = BeautifulSoup(html, "html.parser")
                job_div = soup.find("div", {"data-uxi-widget": "JobDescription"})

                return (
                    job_div.get_text(separator="\n", strip=True)
                    if job_div else soup.get_text(separator="\n", strip=True)
                )

        except Exception as e:
            raise ValueError(
                f"Playwright rendering failed for URL '{url}': {e}"
            )
