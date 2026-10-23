import json
import sys

from openai import OpenAI


def translate_query(query: str, target_language: str) -> str:
    client = OpenAI()
    response = client.responses.create(model="gpt-5.4-mini", input=f"Translate to {target_language}: {query}")
    return response.output_text


def main() -> None:
    print(json.dumps({"translated_query": translate_query(sys.argv[1], sys.argv[2])}))


if __name__ == "__main__":
    main()
