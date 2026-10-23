from openai import OpenAI

client = OpenAI()
MODEL_ID = "gpt-4o-mini"


def alt_text_translate(alt_text: str, target_language: str) -> str:
    response = client.responses.create(
        model=MODEL_ID,
        input=[
            {"role": "system", "content": "Translate the provided alt text while preserving meaning and brevity."},
            {"role": "user", "content": f"Language: {target_language}\nText: {alt_text}"},
        ],
    )
    return response.output_text
