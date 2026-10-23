import os
import google.generativeai as genai


def summarize_job_results(job_report: str) -> str:
    """
    Summarizes embedding job results using the Google Gemini API.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"Please summarize the key points of the following embedding job report:\n\n{job_report}"

    response = model.generate_content(prompt)

    return response.text
