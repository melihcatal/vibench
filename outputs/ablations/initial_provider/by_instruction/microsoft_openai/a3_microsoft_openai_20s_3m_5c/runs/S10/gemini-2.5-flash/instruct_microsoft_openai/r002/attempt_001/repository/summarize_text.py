import os
import openai

def summarize_text(text: str) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

    client = openai.OpenAI(
        api_key=openai.api_key,
        base_url=openai.api_base,
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": f"Please summarize the following text: {text}"}
        ]
    )
    return response.choices[0].message.content

