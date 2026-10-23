from typing import Dict, Any, Optional
import json
from model_client import LLMClient
from model_models import LLMRequest, normalize_request, normalize_response


async def extract_json(
    text: str,
    schema: Dict[str, Any],
    system_prompt: Optional[
        str
    ] = "Extract structured data from text as valid JSON matching the provided schema.",
    max_tokens: Optional[int] = None,
) -> Dict[str, Any]:
    """Extract structured JSON from text using Anthropic's hosted LLM."""
    client = LLMClient()
    schema_str = json.dumps(schema, indent=2)
    request = normalize_request(
        {
            "prompt": f"Extract data matching this schema from the text:\n\nSchema: {schema_str}\n\nText: {text}",
            "system_prompt": system_prompt,
            "max_tokens": max_tokens,
        }
    )

    response = await client.generate(
        prompt=request.prompt,
        system_prompt=request.system_prompt,
    )
    normalized = normalize_response(response, client.config.model_id)

    try:
        return json.loads(normalized.content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON from model output: {e}")
