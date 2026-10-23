import json
import os

from openai import OpenAI


DEFAULT_MODEL = "gpt-4.1-mini"


def translate_platform_output(output: str, locale: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model=os.environ.get("OPENAI_MODEL", DEFAULT_MODEL),
        input=[
            {
                "role": "system",
                "content": "Translate platform model output into the requested locale while preserving meaning, tone, and formatting.",
            },
            {
                "role": "user",
                "content": json.dumps({"locale": locale, "output": output}, ensure_ascii=False),
            },
        ],
    )
    return response.output_text


if __name__ == "__main__":
    print(translate_platform_output("Hello from the platform.", "es"))
