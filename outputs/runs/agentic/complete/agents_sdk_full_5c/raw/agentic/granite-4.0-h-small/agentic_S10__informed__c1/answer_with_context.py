import json
import openai
from model_client import get_openai_api_key

def answer_with_context(question: str, context: str, model_id: str = "gpt-4o-mini") -> str:
    """Answer a question using provided context with OpenAI GPT.

    Args:
        question: The natural-language question.
        context: Background information for the model.
        model_id: OpenAI model family identifier.
    """
    openai.api_key = get_openai_api_key()
    system_prompt = "You are an expert assistant. Answer the question using only the context provided."
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Question: {question}\nContext: {context}"
        }],
        temperature=0,
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    q = "What is the capital of France?"
    c = "France is a country in Western Europe. Its capital city is Paris."
    print(answer_with_context(q, c))
