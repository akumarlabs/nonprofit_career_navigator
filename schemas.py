from pydantic import BaseModel, Field
from typing import List


class ATSFeedback(BaseModel):
    """
    Output schema for ATS analysis.
    - issues: list of specific formatting or keyword issues
    - recommendations: improvements for ATS compatibility
    - score: integer from 0 to 100
    """

    issues: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    score: int


class ResumeFeedback(BaseModel):
    """
    Feedback on resume's structure, tone, and overall effectiveness.
    """

    strengths: List[str] = Field(default_factory=list)
    areas_to_improve: List[str] = Field(default_factory=list)
    overall_assessment: str


class MatchEvaluation(BaseModel):
    """
    Output for matching resume to a job description.
    """

    match_score: int
    skills_matched: List[str] = Field(default_factory=list)
    skills_missing: List[str] = Field(default_factory=list)
    summary: str


class ResumeOptimization(BaseModel):
    """
    Output from resume improvement agent.
    """

    recommended_changes: List[str] = Field(default_factory=list)
    sections_to_update: List[str] = Field(default_factory=list)
    rationale: str


class CoverLetterAdvice(BaseModel):
    """
    Advice for including a cover letter with a job application.
    """

    is_cover_letter_needed: bool
    key_points_to_include: List[str] = Field(default_factory=list)
    tone_suggestions: List[str] = Field(default_factory=list)


class CompanyResearch(BaseModel):
    """
    Insightful interview preparation from company research.
    """

    company_insights: List[str] = Field(default_factory=list)
    suggested_questions: List[str] = Field(default_factory=list)
