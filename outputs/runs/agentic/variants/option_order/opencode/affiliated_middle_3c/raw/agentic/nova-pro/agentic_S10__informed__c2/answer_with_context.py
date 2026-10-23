from .model_client import client


def answer_with_context(question, context):
    response = client.completions.create(
        model="claude-v2",
        prompt=f"Answer the following question using the provided context: {question}\n\nContext: {context}",
        max_tokens_to_sample=100,
    )
    return response.completion
