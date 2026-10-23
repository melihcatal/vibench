from model_client import invoke_bedrock, model_id
from model_models import json_prompt, parse_anthropic_text, safe_json_loads, clean_text


def extract_json(text, schema_description="Return valid JSON only.", max_tokens=512):
    payload = json_prompt(
        "Extract structured data from the input and respond with JSON only.",
        f"{schema_description}\n\nText:\n{clean_text(text)}",
        max_tokens=max_tokens,
        temperature=0.0,
    )
    return safe_json_loads(parse_anthropic_text(invoke_bedrock(model_id("extract"), payload)))
