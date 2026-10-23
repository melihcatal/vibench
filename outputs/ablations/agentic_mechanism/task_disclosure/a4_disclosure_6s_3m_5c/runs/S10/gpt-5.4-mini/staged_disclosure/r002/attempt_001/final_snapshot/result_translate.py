import os
from openai import OpenAI


def translate_result(text: str, target_language: str = "en") -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": f"Translate the provided model output into {target_language}. Return only the translation.",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.output_text
