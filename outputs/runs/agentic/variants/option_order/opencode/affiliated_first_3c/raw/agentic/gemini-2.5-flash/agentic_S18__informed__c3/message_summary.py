import google.generativeai as genai
import os
from messaging_models import PubSubMessage, SummarizedMessage
import datetime


def summarize_message(message: PubSubMessage) -> SummarizedMessage:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")
    message_data_str = str(message.data)
    prompt = f"Summarize the following message data: {message_data_str}"

    response = model.generate_content(prompt)
    summary_text = response.text

    return SummarizedMessage(
        message_id=message.id if message.id else "",
        summary=summary_text,
        processed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    )
