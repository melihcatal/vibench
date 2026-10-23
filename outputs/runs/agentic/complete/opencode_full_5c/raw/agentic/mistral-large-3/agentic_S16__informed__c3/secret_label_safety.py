import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from security_models import SecretLabelCheck


def secret_label_safety(secret_name: str, labels: dict) -> SecretLabelCheck:
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))

    prompt = f"Check the following secret labels and notes for unsafe or sensitive text:\n\nSecret Name: {secret_name}\nLabels: {labels}\n\nProvide a JSON response with keys 'is_safe' (bool) and 'unsafe_reasons' (list of strings if unsafe)."

    messages = [ChatMessage(role="user", content=prompt)]
    response = client.chat(
        model="mistral-large-latest",
        messages=messages,
        response_format={"type": "json_object"},
    )

    result = response.choices[0].message.content
    return SecretLabelCheck(
        **{"secret_name": secret_name, "labels": labels, **eval(result)}
    )
