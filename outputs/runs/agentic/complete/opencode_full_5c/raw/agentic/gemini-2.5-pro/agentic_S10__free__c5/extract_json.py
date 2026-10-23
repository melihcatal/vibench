import json
from model_client import get_model_client
from model_models import CompletionResponse


def extract_json(unstructured_text: str) -> CompletionResponse:
    client = get_model_client()
    prompt = f"Extract structured JSON from the following text:\n\n{unstructured_text}"

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that extracts JSON from text. Respond with only the JSON object.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    extracted_json = response.choices[0].message.content
    finish_reason = response.choices[0].finish_reason

    return CompletionResponse(text=extracted_json, finish_reason=finish_reason)
