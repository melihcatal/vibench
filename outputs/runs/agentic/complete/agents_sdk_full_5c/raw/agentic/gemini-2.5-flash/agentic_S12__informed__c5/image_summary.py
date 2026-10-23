import google.generativeai as genai
import os
from typing import Dict, Any

def summarize_visual_analysis(analysis_results: Dict[str, Any]) -> str:
    """Summarizes visual analysis results using the Google Gemini API."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro') # Using gemini-pro for text summary

    prompt = (
        "Summarize the following visual analysis results in a concise paragraph:\n\n"
        f"Labels: {', '.join(analysis_results.get('labels', []))}\n"
        f"Description: {analysis_results.get('description', 'N/A')}\n"
        f"Detected Text: {analysis_results.get('text_content', 'N/A')}\n"
        f"Safety Scores: {analysis_results.get('safety_scores', {})}\n\n"
        "Summary:"
    )

    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Example usage
    # os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY"
    # sample_results = {
    #     "labels": ["cat", "pet", "animal"],
    #     "description": "This image appears to show: cat, pet, animal.",
    #     "text_content": "MEOW",
    #     "safety_scores": {"adult": "VERY_UNLIKELY", "violence": "UNLIKELY"}
    # }
    # summary = summarize_visual_analysis(sample_results)
    # print(f"Summary: {summary}")
    pass