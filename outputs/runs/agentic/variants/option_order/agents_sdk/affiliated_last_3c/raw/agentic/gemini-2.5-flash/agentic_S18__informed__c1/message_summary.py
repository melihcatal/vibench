from typing import Dict, Any
from messaging_client import configure_gemini

def summarize_message(message_payload: Dict[str, Any]) -> str:
    """Summarizes a message payload using the Google Gemini API (gemini-pro)."""
    model = configure_gemini()

    # Convert the payload to a string for summarization
    message_text = str(message_payload)

    prompt = f"Please summarize the following message payload concisely:\n\n{message_text}"
    
    response = model.generate_content(prompt)
    
    if response.candidates and response.candidates[0].content.parts:
        return response.candidates[0].content.parts[0].text
    else:
        return "Could not generate summary."
