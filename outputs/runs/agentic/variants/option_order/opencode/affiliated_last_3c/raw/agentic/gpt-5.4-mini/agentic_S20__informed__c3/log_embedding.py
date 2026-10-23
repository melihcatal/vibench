import os

import openai


def main() -> None:
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    client.embeddings.create(
        model="text-embedding-3-small", input=["selected log message"]
    )


if __name__ == "__main__":
    main()
