import pytest
from tools import JobDescriptionParser

# Example URL with simple, static HTML content for testing.
TEST_JOB_URL = "https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/Director-of-AI-Research_JR1991669-1"

def test_parse_url_returns_text():
    parser = JobDescriptionParser()
    text = parser(TEST_JOB_URL)

    print("Extracted text preview:", text)  # <-- this will print with `-s`
    assert isinstance(text, str)
    assert len(text) > 100