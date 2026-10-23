import json
import os

from openai import OpenAI

from security_models import OperationResult, normalize_text


def crypto_audit_embedding(note):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model="text-embedding-3-small", input=normalize_text(note)
    )
    return OperationResult(ok=True, data={"embedding": response.data[0].embedding})


def main():
    print(json.dumps({"status": "ready"}))


if __name__ == "__main__":
    main()
