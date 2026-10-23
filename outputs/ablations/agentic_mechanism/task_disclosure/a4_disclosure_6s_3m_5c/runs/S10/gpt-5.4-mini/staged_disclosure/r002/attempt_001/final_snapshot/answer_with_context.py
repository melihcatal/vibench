import os
import sys
from openai import OpenAI


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit("usage: answer_with_context.py <question> <context>")
    question = sys.argv[1]
    context = sys.argv[2]
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": "Answer the user's question using only the provided context. If the context does not contain the answer, say you do not know.",
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}",
            },
        ],
    )
    print(response.output_text)


if __name__ == "__main__":
    main()
