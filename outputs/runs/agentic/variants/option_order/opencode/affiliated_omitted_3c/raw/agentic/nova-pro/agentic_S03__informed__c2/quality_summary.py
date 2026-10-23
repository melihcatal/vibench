import os
from google.generativeai import GenerativeModel


def summarize_translation_quality(text):
    os.environ["GOOGLE_API_KEY"] = "your-api-key"
    model = GenerativeModel("gemini-pro")
    response = model.generate_content(
        f"Summarize the translation quality issues in this text: {text}"
    )
    return response.text
