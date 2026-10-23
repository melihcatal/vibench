import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))


def summarize_record(record_text: str) -> str:
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(
        f"Summarize the following document record: {record_text}"
    )
    return response.text
