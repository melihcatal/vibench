import os
import google.generativeai as genai
import dataclasses
from typing import List, Optional


@dataclasses.dataclass
class AnalysisResult:
    labels: List[str] = dataclasses.field(default_factory=list)
    text_content: Optional[str] = None
    safety_scores: Optional[dict] = None
    image_description: Optional[str] = None


def summarize_visual_analysis(analysis_result: AnalysisResult) -> str:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-pro")

    prompt_parts = [
        "Given the following visual analysis results, provide a concise summary of the image:",
        f"Labels: {', '.join(analysis_result.labels)}"
        if analysis_result.labels
        else "",
        f"Detected Text: {analysis_result.text_content}"
        if analysis_result.text_content
        else "",
        f"Image Description: {analysis_result.image_description}"
        if analysis_result.image_description
        else "",
        f"Safety Scores: {analysis_result.safety_scores}"
        if analysis_result.safety_scores
        else "",
        "---",
        "Summary:",
    ]

    # Filter out empty strings from prompt_parts
    cleaned_prompt_parts = [part for part in prompt_parts if part]

    response = model.generate_content("\n".join(cleaned_prompt_parts))
    return response.text
