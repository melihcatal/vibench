import openai
import os

def answer_question_with_context(question: str, context: str) -> str:
    """
    Calls a hosted LLM (OpenAI) to answer a question using provided context.

    Args:
        question: The question to be answered.
        context: The context to use for answering the question.

    Returns:
        The LLM's answer to the question.
    """
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4",  # Concrete model identifier
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
        ],
        temperature=0.7,
        max_tokens=500,
    )
    return response.choices[0].message.content

