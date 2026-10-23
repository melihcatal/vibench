from model_client import get_openai_client
from model_models import ContextAnswerInput, ContextAnswerOutput

def answer_with_context(input_data: ContextAnswerInput) -> ContextAnswerOutput:
    client = get_openai_client()
    messages = [
        {"role": "system", "content": f"You are a helpful assistant. Answer the user's question based ONLY on the following context: {input_data.context}"},
        {"role": "user", "content": input_data.question}
    ]
    response = client.chat.completions.create(
        model=input_data.model_name,
        messages=messages,
        max_tokens=input_data.max_tokens,
        temperature=input_data.temperature
    )
    answer = response.choices[0].message.content if response.choices else ""
    return ContextAnswerOutput(
        answer=answer,
        model_name=input_data.model_name,
        finish_reason=response.choices[0].finish_reason if response.choices else None
    )