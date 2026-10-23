from model_client import OpenAIClient
from model_models import ExtractionRequest, ExtractionResponse
import json


def extract_json(request: ExtractionRequest) -> ExtractionResponse:
    client = OpenAIClient().get_client()
    response = client.chat.completions.create(
        model=request.model,
        messages=[
            {
                "role": "system",
                "content": f"You are an assistant that extracts structured JSON data according to the following schema: {json.dumps(request.schema)}",
            },
            {
                "role": "user",
                "content": f"Extract JSON from the following text: {request.text}",
            },
        ],
        response_format={"type": "json_object"},
        max_tokens=1024,
        temperature=0.0,
    )
    return ExtractionResponse(
        extracted_json=json.loads(response.choices[0].message.content)
    )
