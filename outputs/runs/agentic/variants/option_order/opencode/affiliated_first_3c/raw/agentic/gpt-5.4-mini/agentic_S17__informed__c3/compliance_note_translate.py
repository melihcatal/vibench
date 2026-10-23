import os
from openai import OpenAI


def compliance_note_translate(text: str, target_language: str = "fr") -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate this compliance note to {target_language}: {text}",
    )
    return response.output_text


if __name__ == "__main__":
    compliance_note_translate(
        os.environ.get("TEXT", ""), os.environ.get("TARGET_LANGUAGE", "fr")
    )
