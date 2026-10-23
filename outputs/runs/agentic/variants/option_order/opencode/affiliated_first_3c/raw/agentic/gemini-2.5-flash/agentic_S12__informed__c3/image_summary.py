import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))


def summarize_visual_analysis(analysis_results: dict) -> str:
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Summarize the following visual analysis results:\n\n{analysis_results}"
    response = model.generate_content(prompt)
    return response.text
