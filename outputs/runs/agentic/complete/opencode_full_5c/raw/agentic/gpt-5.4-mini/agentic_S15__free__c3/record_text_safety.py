import json
import os
import sys

from openai import OpenAI


def check_text_safety(record):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Check this user-generated document for unsafe content and return a brief verdict: {json.dumps(record)}",
    )
    return {"safety_report": response.output_text}


def main():
    print(json.dumps(check_text_safety(json.loads(sys.stdin.read()))))


if __name__ == "__main__":
    main()
