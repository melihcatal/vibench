import json
import os
import sys

from openai import OpenAI


def translate_record(record, target_language):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate the user-facing fields of this record into {target_language}: {json.dumps(record)}",
    )
    return {"translated_text": response.output_text}


def main():
    payload = json.loads(sys.stdin.read())
    print(json.dumps(translate_record(payload["record"], payload["target_language"])))


if __name__ == "__main__":
    main()
