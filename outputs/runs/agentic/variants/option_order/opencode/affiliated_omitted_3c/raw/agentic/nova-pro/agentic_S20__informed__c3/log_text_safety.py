import os
from mistralai.client import MistralClient

client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))


def check_safety(text):
    response = client.chat.completions.create(
        model="mistral-large-latest",
        messages=[
            {
                "role": "system",
                "content": "Check if the following text contains unsafe content:",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content
