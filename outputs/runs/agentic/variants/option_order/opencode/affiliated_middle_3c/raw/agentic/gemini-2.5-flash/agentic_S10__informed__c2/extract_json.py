import os
import json
import google.generativeai as genai
from model_client import GeminiClient
from model_models import JSONExtractRequest, JSONExtractResponse


def extract_json(request: JSONExtractRequest) -> JSONExtractResponse:
    client = GeminiClient()
    model = client.get_generative_model(request.model_name)

    # It's often helpful to explicitly tell the model to output JSON
    prompt = (
        f"Extract information from the following text into a JSON object "
        f"that conforms to this schema: {json.dumps(request.json_schema)}\n\n"
        f"Text: {request.text_content}\n\nJSON:"
    )

    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=request.temperature,
            max_output_tokens=request.max_output_tokens,
        ),
    )

    try:
        extracted_data = json.loads(response.text)
    except json.JSONDecodeError:
        # Attempt to clean up and re-parse if the model output is not perfect JSON
        # This is a basic attempt; more robust error handling might be needed.
        cleaned_text = response.text.strip().replace("```json", "").replace("```", "")
        extracted_data = json.loads(cleaned_text)

    return JSONExtractResponse(extracted_json=extracted_data)
