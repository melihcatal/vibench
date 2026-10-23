import os
from openai import OpenAI
from model_client import get_client
from model_models import QARequest, QAResponse

def answer_with_context(question: str, context: str) -> str:
    """Answer a question using provided context with a hosted LLM."""
    client = get_client()
    
    prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {question}

Answer based only on the provided context. If the context doesn't contain enough information to answer, say "I cannot answer based on the provided context.""""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=500
        )
        
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        raise Exception(f"Failed to answer question: {str(e)}")