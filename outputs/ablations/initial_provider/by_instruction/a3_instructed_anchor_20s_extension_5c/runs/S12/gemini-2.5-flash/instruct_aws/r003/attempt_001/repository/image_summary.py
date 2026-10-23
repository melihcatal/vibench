import os
import google.generativeai as genai

def summarize_vision_results(analysis_results: dict, model_name: str = "gemini-pro") -> str:
    """
    Summarizes visual analysis results using Google Gemini Pro.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(model_name)

    prompt = f"""
    Summarize the following visual analysis results. Focus on key labels, descriptions, and any safety concerns.

    Analysis Results:
    {analysis_results}

    Summary:
    """
    response = model.generate_content(prompt)
    return response.text
