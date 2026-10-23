from model_client import client
from model_models import ModelRequest, normalize_response

def answer_with_context(question, context):
    request = ModelRequest(f'Answer the following question using the provided context: {question}. Context: {context}')
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": request.prompt}],
        model=request.model
    )
    return normalize_response(response)