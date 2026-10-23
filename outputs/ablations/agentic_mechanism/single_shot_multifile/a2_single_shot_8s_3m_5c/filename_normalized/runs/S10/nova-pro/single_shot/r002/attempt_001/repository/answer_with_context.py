from [HELPER] model_client import get_llm_client

def answer_with_context(question, context):
    client = get_llm_client()
    response = client.answer_with_context(question, context)
    return response.answer