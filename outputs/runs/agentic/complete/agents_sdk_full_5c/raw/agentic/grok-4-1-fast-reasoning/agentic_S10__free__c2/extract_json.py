from model_client import client
from model_models import parse_json_response

def extract_json(text: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts structured information from text into JSON format. Output only valid JSON with keys like entities, dates, locations, etc."},
            {"role": "user", "content": f"Extract key structured data from this text: {text}"}
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
    )
    return parse_json_response(response)