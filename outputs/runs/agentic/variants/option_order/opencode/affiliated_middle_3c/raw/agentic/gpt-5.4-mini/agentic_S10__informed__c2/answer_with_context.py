from model_client import get_chat_client, select_chat_model, chat_messages, chat_text


def answer_with_context(context: str, question: str) -> str:
    client = get_chat_client()
    model = select_chat_model('qa')
    response = client.chat.completions.create(
        model=model,
        messages=chat_messages(
            'Answer the question using only the provided context.',
            f'Context:
{context}

Question:
{question}',
        ),
        temperature=0.1,
    )
    return chat_text(response)
