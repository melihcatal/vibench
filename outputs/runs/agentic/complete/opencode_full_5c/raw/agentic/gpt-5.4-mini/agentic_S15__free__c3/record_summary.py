import json
import os
import sys

from openai import OpenAI


def summarize_record(record):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Summarize this document record concisely: {json.dumps(record)}",
    )
    return {"summary": response.output_text}


def main():
    print(json.dumps(summarize_record(json.loads(sys.stdin.read()))))


if __name__ == "__main__":
    main()
