from typing import Dict, Any, List
import openai
from database_models import DocumentResponse

# Configure OpenAI API
openai.api_key = "sk-proj-..."  # Replace with a valid OpenAI API key

def summarize_document(document: DocumentResponse, model: str = "gpt-4o-mini") -> str:
    """
    Summarizes the content of a document using OpenAI's GPT model.
    
    Args:
        document: The document to summarize.
        model: The OpenAI model to use for summarization.
        
    Returns:
        A summary of the document content.
    """
    prompt = f"Summarize the following document in a concise manner:\n\n{document.data}"
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response.choices[0].message["content"].strip()