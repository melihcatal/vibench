import os
from typing import Dict, Any
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def moderate_vendor_notes(notes: str) -> Dict[str, Any]:
    """
    Moderates vendor notes or memo fields using Mistral Chat API for content safety.
    Model: mistral/mistral-large-latest
    """
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))

    prompt = (
        "Analyze the following vendor notes for inappropriate or unsafe content:\n"
        f"Notes: {notes}\n"
        "Respond with a JSON object containing 'is_safe' (boolean) and 'reason' (string)."
    )

    messages = [ChatMessage(role="user", content=prompt)]
    response = client.chat(
        model="mistral-large-latest",
        messages=messages,
        response_format={"type": "json_object"},
    )

    return eval(response.choices[0].message.content)
