import os
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def answer_with_context(question, context):
    response = client.completions.create(
        model="claude-3-opus-20240229",
        prompt=f"Answer the following question using the provided context: {question}\nContext: {context}",
        max_tokens_to_sample=1024,
    )
    return response.completion
