import mistralai
import os


def summarize_text(text: str) -> str:
    client = mistralai.ChatClient(api_key=os.getenv("MISTRAL_API_KEY"))
    response = client.chat(
        model="mistral-large-latest",
        messages=[{"role": "user", "content": text}],
        temperature=0.2,
    )
    return response.choices[0].message.content
