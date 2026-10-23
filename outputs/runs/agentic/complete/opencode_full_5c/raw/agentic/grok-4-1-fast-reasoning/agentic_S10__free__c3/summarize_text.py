from model_client import get_openai_client


def summarize_text(text: str) -> str:
    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following text in a concise paragraph:\\n\\n{text}",
            }
        ],
        max_tokens=500,
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()
