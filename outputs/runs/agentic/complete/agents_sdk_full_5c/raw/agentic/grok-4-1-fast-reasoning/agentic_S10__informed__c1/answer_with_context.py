from model_client import get_gemini_client
from model_models import mk_system, mk_user

genai = get_gemini_client()
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

def answer_with_context(question: str, context: str) -> str:
    messages = [
        mk_system(f'Answer the question based only on the provided context. Context: {context}'),
        mk_user(question)
    ]
    response = model.generate_content(messages)
    return response.text
