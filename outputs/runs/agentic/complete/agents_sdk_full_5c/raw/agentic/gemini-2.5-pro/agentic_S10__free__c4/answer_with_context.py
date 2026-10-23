from model_client import get_model
from model_models import GEMINI_MODEL_NAME

def answer(context: str, question: str) -> str:
    """
    Answers a question based on the provided context using a hosted LLM.

    Args:
        context: The context to use for answering the question.
        question: The question to answer.

    Returns:
        The answer string.
    """
    model = get_model(GEMINI_MODEL_NAME)
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
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"An error occurred while generating an answer: {e}")
        return "Error: Could not generate an answer."
