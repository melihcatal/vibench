import os
import google.generativeai as genai


def summarize_message(message_payload: dict) -> str:
    # GOOGLE_API_KEY environment variable should be set
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Summarize the following JSON message payload in one concise sentence: {message_payload}"

    response = model.generate_content(prompt)
    summary = response.text
    print(f"Message summary: {summary}")
    return summary
