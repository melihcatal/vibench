from typing import Dict, Any
from model_client import LLMClient
from model_models import LLMRequest, normalize_response


async def extract_json(text: str, schema: Dict[str, Any]) -> Dict[str, Any]:
    """Extract structured JSON from text using Mistral's hosted LLM."""
    client = LLMClient()
    prompt = (
        f"Extract structured data from the following text as JSON matching this schema:\n"
        f"Schema: {schema}\n\n"
        f"Text: {text}\n\n"
        f"Return only the JSON data, no additional text."
    )
    request = LLMRequest(prompt=prompt, max_tokens=1000)

    response = await client.generate(
        request.prompt, request.temperature, request.max_tokens
    )
    normalized = normalize_response(response)
    await client.close()

    # Extract JSON from the response
    content = normalized.choices[0]["message"]["content"]
    import json

    return json.loads(content)
