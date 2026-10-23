from openai import OpenAI


def quality_summary(translated_text: str, source_text: str) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize translation quality issues concisely.",
            },
            {
                "role": "user",
                "content": f"Source: {source_text}\nTranslated: {translated_text}",
            },
        ],
    )
    return response.choices[0].message.content or ""
