import os
import openai
from security_client import get_kms_client


def summarize_key_usage() -> str:
    kms_client = get_kms_client()
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    keys = kms_client.list_keys().get("Keys", [])
    key_details = []
    for key in keys:
        detail = kms_client.describe_key(KeyId=key["KeyId"])
        key_details.append(detail["KeyMetadata"])

    if not key_details:
        return "No KMS keys found."

    key_info_str = "\n".join(
        [
            f"Key ID: {k['KeyId']}, State: {k['KeyState']}, "
            f"Creation Date: {k['CreationDate']}, "
            f"Description: {k.get('Description', 'N/A')}"
            for k in key_details
        ]
    )

    prompt = f"Summarize the following AWS KMS key usage information:\n{key_info_str}"

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content
