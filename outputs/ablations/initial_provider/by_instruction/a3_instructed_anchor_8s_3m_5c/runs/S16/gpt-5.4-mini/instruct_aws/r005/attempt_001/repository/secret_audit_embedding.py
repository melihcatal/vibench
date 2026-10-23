import os

from openai import OpenAI


def main():
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    text = os.environ["SECRET_AUDIT_NOTE"]
    result = client.embeddings.create(model="text-embedding-3-small", input=text)
    print(result.data[0].embedding)


if __name__ == "__main__":
    main()
