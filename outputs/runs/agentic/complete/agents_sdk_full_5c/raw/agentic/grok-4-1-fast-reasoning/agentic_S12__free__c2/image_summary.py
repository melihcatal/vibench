from typing import Dict, Any
from vision_client import gemini_model

def image_summary(analysis_results: Dict[str, Any]) -> str:
    prompt = f"""Summarize the following image analysis results in a concise paragraph:

Labels: {analysis_results.get('labels', [])}
Description: {analysis_results.get('description', '')}
Detected Text: {analysis_results.get('text', '')}
Safety: {analysis_results.get('safety', {})}
"""
    response = gemini_model.generate_content(prompt)
    return response.text
