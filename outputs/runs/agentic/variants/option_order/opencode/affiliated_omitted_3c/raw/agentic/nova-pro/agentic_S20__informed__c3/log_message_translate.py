import os
from mistralai.client import MistralClient

client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))


def translate_log(text, target_language):
    response = client.chat.completions.create(
        model="mistral-large-latest",
        messages=[
            {
                "role": "system",
                "content": f"Translate the following log message to {target_language}:",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content
