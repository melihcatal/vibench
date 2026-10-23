from model_client import get_openai_client

def answer_with_context(question: str, context: str) -> str:
    client = get_openai_client()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Answer the question truthfully using only the provided context. If the answer is not in the context, say \"I don't know.\""},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
        ]
    )
    return response.choices[0].message.content