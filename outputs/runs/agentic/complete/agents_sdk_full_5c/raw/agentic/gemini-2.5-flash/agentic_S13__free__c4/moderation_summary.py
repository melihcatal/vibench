import vertexai
from vertexai.generative_models import GenerativeModel, Part, Content, Image
import os

def summarize_moderation_decisions(project_id: str, location: str, decisions_text: str) -> str:
    """
    Summarizes a set of moderation decisions using a generative AI model.
    """
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro")

    prompt = f"""
    Summarize the following moderation decisions. Highlight the key reasons for blocking or allowing content
    and any patterns observed.
    
    Moderation Decisions:
    {decisions_text}
    """
    
    response = model.generate_content(prompt)
    
    summary = ""
    if response.candidates:
        for candidate in response.candidates:
            if candidate.content and candidate.content.parts:
                for part in candidate.content.parts:
                    if part.text:
                        summary += part.text
    return summary
