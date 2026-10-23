import os
import google.generativeai as genai
from messaging_models import PubSubMessage

# Google Gemini API provider-specific signal

def summarize_message(message: PubSubMessage) -> str:
    if not os.environ.get("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    # Use a specific model that supports text generation and summarization
    # Using 'gemini-pro' as a commonly available and capable model for text tasks.
    model = genai.GenerativeModel('gemini-pro')

    message_data_str = str(message.data)
    prompt = f"Please provide a concise summary of the following message content:\n\n{message_data_str}"

    try:
        response = model.generate_content(prompt)
        if response.parts:
            return response.text
        elif response.candidates and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text
        else:
            return "No summary generated."
    except Exception as e:
        return f"Error summarizing message: {e}"
