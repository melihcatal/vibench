import os

from openai import OpenAI


def translate_log_message(message: str, target_locale: str) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"Translate support-visible log messages into {target_locale}.",
            },
            {"role": "user", "content": message},
        ],
    )
    return response.choices[0].message.content or ""


def main() -> None:
    translate_log_message("service unavailable", "es")


if __name__ == "__main__":
    main()
