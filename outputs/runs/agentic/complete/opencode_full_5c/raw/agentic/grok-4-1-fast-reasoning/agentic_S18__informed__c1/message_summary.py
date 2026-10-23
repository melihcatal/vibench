import os
import google.generativeai as genai
from messaging_models import Event

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


def summarize_message(event: Event) -> str:
    prompt = f"Summarize the processing results of this message: {event.payload}"
    response = model.generate_content(prompt)
    return response.text
