import os
import google.generativeai as genai


def record_summary(document_content: str):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Summarize the following document content:\n\n{document_content}"
    response = model.generate_content(prompt)
    return {"status": "success", "summary": response.text}
