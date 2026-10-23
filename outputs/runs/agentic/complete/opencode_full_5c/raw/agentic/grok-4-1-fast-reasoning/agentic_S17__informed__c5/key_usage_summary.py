import os
from mistralai.client import MistralClient

client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))


def summarize_key_usage(events: list[str]) -> str:
    content = "Summarize the key usage and crypto events:\\n" + "\\n".join(events)
    response = client.chat(
        model="open-mistral-nemo-2407", messages=[{"role": "user", "content": content}]
    )
    return response.choices[0].message.content
