from model_client import client


def extract_json(text):
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": f"Extract JSON from the following text: {text}"}
        ],
    )
    return response.content
