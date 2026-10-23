import os
import google.generativeai as genai

def summarize_image_analysis(analysis_results: dict) -> str:
    """
    Summarizes visual analysis results using the Google Gemini API.
    Requires GOOGLE_API_KEY environment variable.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Summarize the following image analysis results:
    {analysis_results}"

    response = model.generate_content(prompt)
    return response.text
