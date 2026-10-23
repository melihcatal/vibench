import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def summarize_message_processing(message_data: dict) -> str:
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Summarize the following message processing results, highlighting key information like status, errors, and content type: {message_data}"
    response = model.generate_content(prompt)
    return response.text
