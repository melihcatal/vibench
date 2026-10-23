import google.generativeai as genai
import os


def summarize_record(record_data: dict, model_name: str = "gemini-pro"):
    """Summarizes a given record using Google Gemini API."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(model_name)

    prompt = f"Summarize the following document record: {record_data}"
    response = model.generate_content(prompt)

    return response.text
