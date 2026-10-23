import os
from model_client import get_llm_client
from model_models import LLMResponse

def extract_json(text: str, model_name: str = "gpt-4o-mini") -> dict:
    """Extract structured JSON from text using a hosted LLM via OpenAI provider.
    Identifies provider via SDK import and model identifier.
    """
    client = get_llm_client(model_name)
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": f"Extract the following information from the text and return it as JSON:\n{text}"}],
        temperature=0.0,
    )
    norm_resp = LLMResponse.from_openai(response)
    json_str = norm_resp.choices[0].message.content.strip()
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        raise ValueError(f"Extracted content is not valid JSON: {json_str}")
