import os
import google.generativeai as genai

def summarize_job_results(results: str) -> str:
    """
    Summarizes embedding job results using the Google Gemini API.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Summarize the following embedding job results:

{results}

Summary:"
    response = model.generate_content(prompt)
    return response.text
