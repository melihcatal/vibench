import os

from openai import OpenAI


def main() -> None:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {
                "role": "user",
                "content": "Summarize recent error logs for incident review.",
            }
        ],
    )


if __name__ == "__main__":
    main()
