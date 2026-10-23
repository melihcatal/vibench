from openai import OpenAI


def quality_summary(translated_text: str, source_language: str | None = None, target_language: str | None = None) -> str:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {"role": "system", "content": "Summarize translation quality issues concisely."},
            {"role": "user", "content": translated_text},
        ],
    )
    return response.output_text
