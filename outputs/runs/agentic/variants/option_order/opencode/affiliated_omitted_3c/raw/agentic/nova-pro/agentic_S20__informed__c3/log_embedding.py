import os
from mistralai.client import MistralClient

client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))


def embed_log(text):
    response = client.chat.completions.create(
        model="mistral-large-latest",
        messages=[
            {
                "role": "system",
                "content": "Generate an embedding for the following log message:",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content
