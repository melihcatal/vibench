import google.generativeai as genai
import os


def record_summary(document_text: str):
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(
        f"Summarize the following document record: {document_text}"
    )
    return response.text
