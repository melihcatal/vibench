import os
from openai import OpenAI
from model_client import get_client
from model_models import QAResponse, QARequest

def answer_with_context(question: str, context: str) -> str:
    """
    Answer a question using provided context via a hosted LLM.
    """
    client = get_client()
    
    prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {question}

Answer the question based only on the provided context. If the context doesn't contain enough information to answer the question, say "I cannot answer based on the provided context.""""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based only on the provided context."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=300
        )
        
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        raise Exception(f"Failed to answer question: {str(e)}")