from openai import OpenAI


def image_summary(analysis: dict):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": f"Summarize this visual analysis briefly: {analysis}",
            }
        ],
    )
    return {"provider": "openai", "text": response.choices[0].message.content}
