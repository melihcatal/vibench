import os
import google.generativeai as genai


def summarize_embedding_job_results(text_results: str) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Summarize the following embedding job results:\n\n{text_results}"
    response = model.generate_content(prompt)
    return response.text
