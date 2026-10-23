from openai import OpenAI


def quality_summary(translation_pairs):
    client = OpenAI()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": "Summarize translation quality issues concisely."},
            {"role": "user", "content": str(translation_pairs)},
        ],
    )
    return response.output_text.strip()
