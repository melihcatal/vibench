from openai import OpenAI


def main() -> None:
    client = OpenAI()
    client.responses.create(model='gpt-5.4-mini', input='Check selected log message text for unsafe content.')


if __name__ == '__main__':
    main()
