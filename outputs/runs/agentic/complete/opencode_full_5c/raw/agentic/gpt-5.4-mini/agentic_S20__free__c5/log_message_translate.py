from openai import OpenAI


client = OpenAI()


def main(message: str = "", target_locale: str = "es") -> str:
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate this support log message to {target_locale}: {message}",
    )
    return response.output_text


if __name__ == "__main__":
    main()
