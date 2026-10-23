import openai
import model_client
import model_models

def answer_with_context(question: str, context: str, model: str = "gpt-4o-mini") -> str:
    """Answers a question using the provided context and a hosted LLM.
    Args:
        question (str): The user question.
        context (str): Supporting text the model can reference.
        model (str): LLM model identifier (default: gpt-4o-mini).
    Returns:
        str: The generated answer.
    """
    safe_question = model_client.check_prompt(question)
    safe_context = model_client.check_prompt(context)
    prompt = f"You are a helpful assistant. Answer the following question using ONLY the provided context. Do not add extra information.\n\nQuestion: {safe_question}\nContext: {safe_context}\nAnswer:"
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()
