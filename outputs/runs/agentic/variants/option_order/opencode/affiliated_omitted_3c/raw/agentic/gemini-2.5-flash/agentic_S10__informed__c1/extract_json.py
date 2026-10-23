import json
from model_client import ModelClient
from model_models import LLMRequest, LLMResponse


def extract_json(request: LLMRequest) -> LLMResponse:
    client = ModelClient.get_openai_client()
    prompt = f"Extract structured JSON from the following text. The JSON should represent key information. If no specific JSON structure is provided, infer one based on the text. If the text contains information about a person, extract their name, age, and city. If it contains information about a book, extract its title, author, and year published.\n\nText: {request.prompt}"

    chat_completion = client.chat.completions.create(
        model=request.model,
        messages=[{"role": "user", "content": prompt}],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        response_format={"type": "json_object"},
    )

    json_output = chat_completion.choices[0].message.content
    return LLMResponse(
        text=json_output, finish_reason=chat_completion.choices[0].finish_reason
    )
