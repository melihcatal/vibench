import json
from model_client import get_openai_client
from model_models import JsonExtractionInput, JsonExtractionOutput

def extract_json(input_data: JsonExtractionInput) -> JsonExtractionOutput:
    client = get_openai_client()
    messages = [
        {"role": "system", "content": f"You are an expert at extracting structured JSON data according to the provided schema: {json.dumps(input_data.json_schema)}. Extract the requested information from the text."},
        {"role": "user", "content": f"Extract information from the following text: {input_data.text}"}
    ]
    response = client.chat.completions.create(
        model=input_data.model_name,
        response_format={"type": "json_object"},
        messages=messages,
        temperature=input_data.temperature
    )
    extracted_content = response.choices[0].message.content if response.choices else "{}"
    return JsonExtractionOutput(
        extracted_json=json.loads(extracted_content),
        model_name=input_data.model_name,
        finish_reason=response.choices[0].finish_reason if response.choices else None
    )