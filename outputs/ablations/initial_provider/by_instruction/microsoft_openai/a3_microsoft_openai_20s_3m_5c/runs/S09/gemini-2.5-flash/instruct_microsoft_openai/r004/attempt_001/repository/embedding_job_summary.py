import google.generativeai as genai
import os

def summarize_embedding_job_results(results: dict) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Summarize the following embedding job results:\n\n{results}"
    response = model.generate_content(prompt)
    return response.text
