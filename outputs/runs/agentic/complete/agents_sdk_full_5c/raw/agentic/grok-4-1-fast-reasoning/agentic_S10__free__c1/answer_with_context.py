import google.generativeai as genai
from model_client import GOOGLE_API_KEY

def answer_with_context(question: str, context: str) -> str:
    \"\"\"Calls Google Gemini 1.5 Pro to answer question using provided context.\"\"
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(
        model_name='gemini-1.5-pro',
        system_instruction='You are a helpful assistant. Use only the provided context to answer the question accurately. If context lacks info, say so.'
    )
    prompt = f'Context: {context}\\n\\nQuestion: {question}\\n\\nAnswer:'
    response = model.generate_content(prompt)
    return response.text
