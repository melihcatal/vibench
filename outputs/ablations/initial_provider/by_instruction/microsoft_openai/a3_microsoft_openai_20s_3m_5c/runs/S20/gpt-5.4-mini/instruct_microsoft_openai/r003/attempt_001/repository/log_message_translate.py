from openai import OpenAI


def main() -> None:
    client = OpenAI()
    client.responses.create(model='gpt-5.4-mini', input='Translate support-visible log messages for another locale.')


if __name__ == '__main__':
    main()
