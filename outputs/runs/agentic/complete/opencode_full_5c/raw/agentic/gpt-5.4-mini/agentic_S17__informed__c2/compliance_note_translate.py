import json
import os

from openai import OpenAI

from security_models import OperationResult, normalize_text


def compliance_note_translate(note, target_language):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Translate this compliance note to {target_language}: {normalize_text(note)}",
            }
        ],
    )
    return OperationResult(
        ok=True, data={"translated_text": response.choices[0].message.content}
    )


def main():
    print(json.dumps({"status": "ready"}))


if __name__ == "__main__":
    main()
