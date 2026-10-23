import google.generativeai as genai
import os
from translation_models import QualitySummaryRequest, QualitySummaryResponse

def summarize_translation_quality(request: QualitySummaryRequest) -> QualitySummaryResponse:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""Review the following translation for quality issues.
    Source ({request.source_language}): """{request.source_text}"""
    Translation ({request.target_language}): """{request.translated_text}"""
    
    Identify any potential issues such as:
    - Inaccuracies or mistranslations
    - Grammatical errors or awkward phrasing
    - Tone mismatches
    - Missing or extra content
    - Cultural insensitivity
    
    Provide a concise summary of the quality, listing any identified issues and suggesting improvements if applicable."""
    
    response = model.generate_content(prompt)
    
    return QualitySummaryResponse(summary=response.text)
