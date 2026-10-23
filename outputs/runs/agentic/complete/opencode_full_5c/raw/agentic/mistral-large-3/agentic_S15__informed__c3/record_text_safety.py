from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os
from typing import Dict, Any, List


def check_text_safety(texts: List[str]) -> List[Dict[str, Any]]:
    """
    Checks user-generated document fields for unsafe content using Mistral's moderation capabilities.
    """
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
    results = []

    for text in texts:
        prompt = (
            "Analyze the following text for unsafe content, including hate speech, violence, self-harm, "
            "sexual content, or harassment. Respond with a JSON object containing:
"
            "{\"is_safe\": bool, \"categories\": [str], \"explanation\": str}":
            f"\n\nText: {text}"
        )
        messages = [ChatMessage(role="user", content=prompt)]

        response = client.chat(
            model="mistral-large-latest",
            messages=messages,
            temperature=0.0
        )
        results.append({"text": text, "safety_analysis": response.choices[0].message.content})

    return results