from openai import OpenAI


def main() -> None:
    client = OpenAI()
    client.responses.create(model='gpt-5.4-mini', input='Summarize error-log findings for incident review.')


if __name__ == '__main__':
    main()
