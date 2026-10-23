import os
from typing import Union
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from security_models import SafetyCheckResult


def check_payload_safety(text: Union[str, bytes]) -> SafetyCheckResult:
    if isinstance(text, bytes):
        text = text.decode("utf-8")

    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))

    messages = [
        ChatMessage(
            role="user",
            content=f"Analyze the following text for unsafe content and respond with a JSON object containing 'is_safe' (boolean), 'violations' (object with categories and descriptions), and 'confidence' (float between 0 and 1):\n\n{text}",
        )
    ]

    response = client.chat(
        model="mistral-large-latest",
        messages=messages,
        response_format={"type": "json_object"},
    )

    result = response.choices[0].message.content
    import json

    result_data = json.loads(result)

    return SafetyCheckResult(
        is_safe=result_data["is_safe"],
        violations=result_data["violations"],
        confidence=result_data["confidence"],
    )
