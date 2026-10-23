from model_client import get_anthropic_client

MODEL_NAME = "claude-3-5-sonnet-20240620"

def answer_with_context(question: str, context: str) -> str:
    """
    Answers a question based on the provided context using the Anthropic API.
    """
    client = get_anthropic_client()

    prompt = f"""
    Based on the context provided below, please answer the question.
    If the answer cannot be found in the context, state that clearly.

    Context:
    ---
    {context}
    ---

    Question: {question}
    """

    try:
        message = client.messages.create(
            model=MODEL_NAME,
            max_tokens=1500,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        if message.content and isinstance(message.content, list) and hasattr(message.content[0], 'text'):
            return message.content[0].text
        return "No answer could be generated."
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred while generating an answer."

