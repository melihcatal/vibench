from model_client import client


def answer_with_context(question, context):
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Answer the following question using the provided context: {question}. Context: {context}",
            }
        ],
    )
    return response.content
