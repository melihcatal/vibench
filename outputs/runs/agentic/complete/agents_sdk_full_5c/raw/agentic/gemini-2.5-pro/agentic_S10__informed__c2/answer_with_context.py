from model_client import get_model_client
from model_models import ChatMessage

def answer_with_context(question: str, context: str) -> str:
    """
    Answers a question based on the provided context using an OpenAI model.
    """
    client = get_model_client()
    
    prompt = f"""
    Based on the context below, please answer the user's question.
    If the answer cannot be found in the context, say "I don't know".

    Context:
    ---
    {context}
    ---

    Question: {question}
    """
    
    messages = [
        ChatMessage(role="system", content="You are a helpful assistant that answers questions based on a given context."),
        ChatMessage(role="user", content=prompt)
    ]
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[m.to_dict() for m in messages],
            max_tokens=256,
            temperature=0.2,
        )
        answer = response.choices[0].message.content
        return answer.strip() if answer else "Could not generate an answer."
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred while generating an answer."
