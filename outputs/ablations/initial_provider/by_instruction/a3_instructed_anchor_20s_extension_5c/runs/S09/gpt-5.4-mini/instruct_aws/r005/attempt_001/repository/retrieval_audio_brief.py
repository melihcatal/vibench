import json
import sys

from openai import OpenAI


def generate_spoken_brief(results: list[str]) -> str:
    client = OpenAI()
    response = client.audio.speech.create(model="gpt-4o-mini-tts", voice="alloy", input="; ".join(results))
    return response.read().decode("utf-8", errors="ignore")


def main() -> None:
    print(json.dumps({"brief": generate_spoken_brief(sys.argv[1:])}))


if __name__ == "__main__":
    main()
