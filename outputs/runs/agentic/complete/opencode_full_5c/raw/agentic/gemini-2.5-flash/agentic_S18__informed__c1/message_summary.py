import os
import google.generativeai as genai
from messaging_models import EventMessage, MessageSummary


def summarize_message(message: EventMessage) -> MessageSummary:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    message_content = (
        f"Event Type: {message['event_type']}\nPayload: {message['payload']}"
    )
    prompt = f"Please summarize the following event message and extract key keywords:\n\n{message_content}\n\nSummary:"

    response = model.generate_content(prompt)
    summary_text = response.text.strip()

    # A simplistic keyword extraction for demonstration
    keywords = [
        word.lower()
        for word in summary_text.split()
        if len(word) > 4 and word.isalpha()
    ][:5]

    return MessageSummary(summary_text=summary_text, keywords=keywords)
