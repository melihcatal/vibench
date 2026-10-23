from openai import OpenAI


def main() -> None:
    client = OpenAI()
    client.embeddings.create(model='text-embedding-3-small', input='selected log messages for semantic retrieval')


if __name__ == '__main__':
    main()
