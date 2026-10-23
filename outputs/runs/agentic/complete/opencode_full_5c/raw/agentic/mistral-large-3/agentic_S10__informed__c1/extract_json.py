from typing import Dict, Any
import json
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from model_client import get_watsonx_client
from model_models import WatsonXRequest, WatsonXResponse


def extract_json(
    text: str,
    schema: Dict[str, Any],
    model_id: str = "ibm/granite-13b-chat-v2",
    max_new_tokens: int = 300,
    **kwargs,
) -> Dict[str, Any]:
    """
    Extract structured JSON from text using IBM watsonx.ai Granite model.
    """
    client = get_watsonx_client()

    schema_str = json.dumps(schema, indent=2)
    prompt = f"Extract structured data from the following text as JSON matching this schema:\n\n{schema_str}\n\nText:\n{text}\n\nJSON:"

    params = {
        GenParams.DECODING_METHOD: "greedy",
        GenParams.MAX_NEW_TOKENS: max_new_tokens,
        GenParams.MIN_NEW_TOKENS: 50,
        GenParams.TEMPERATURE: 0.1,
        GenParams.TOP_K: 50,
        GenParams.TOP_P: 1,
    }
    params.update(kwargs)

    request = WatsonXRequest(model_id=model_id, input=prompt, params=params)

    response: WatsonXResponse = client.generate(request)

    try:
        return json.loads(response.output)
    except json.JSONDecodeError:
        # Fallback: Extract JSON from markdown code block if present
        output = response.output.strip()
        if output.startswith("```json") and output.endswith("```"):
            output = output[7:-3].strip()
        return json.loads(output)
