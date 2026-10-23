import os
from google.generativeai import GenerativeModel


def check_unsafe_content(text):
    os.environ["GOOGLE_API_KEY"] = "your-api-key"
    model = GenerativeModel("gemini-pro")
    response = model.generate_content(
        f"Check if this text contains unsafe content: {text}"
    )
    return response.text
