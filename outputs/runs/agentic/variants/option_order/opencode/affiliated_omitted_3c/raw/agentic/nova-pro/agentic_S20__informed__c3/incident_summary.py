import os
from mistralai.client import MistralClient

client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))


def summarize_logs(logs):
    response = client.chat.completions.create(
        model="mistral-large-latest",
        messages=[
            {
                "role": "system",
                "content": "Summarize the following logs for incident review:",
            },
            {"role": "user", "content": logs},
        ],
    )
    return response.choices[0].message.content
