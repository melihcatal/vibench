from model_client import get_openai_client
from model_models import TextGenerationInput, TextGenerationOutput

def summarize_text(input_data: TextGenerationInput) -> TextGenerationOutput:
    client = get_openai_client()
    messages = [
        {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
        {"role": "user", "content": f"Please summarize the following text: {input_data.prompt}"}
    ]
    response = client.chat.completions.create(
        model=input_data.model_name,
        messages=messages,
        max_tokens=input_data.max_tokens,
        temperature=input_data.temperature
    )
    summary = response.choices[0].message.content if response.choices else ""
    return TextGenerationOutput(
        generated_text=summary,
        model_name=input_data.model_name,
        finish_reason=response.choices[0].finish_reason if response.choices else None
    )