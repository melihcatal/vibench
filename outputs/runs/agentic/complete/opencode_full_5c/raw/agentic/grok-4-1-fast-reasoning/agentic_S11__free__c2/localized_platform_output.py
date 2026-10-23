from openai import OpenAI
from model_client import get_openai_config


def localize_platform_output(text: str, target_locale: str = "fr") -> str:
    config = get_openai_config()
    client = OpenAI(**config)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"Translate the following text to {target_locale}. Provide only the translation, no explanations.",
            },
            {"role": "user", "content": text},
        ],
        temperature=0.1,
    )
    return response.choices[0].message.content
