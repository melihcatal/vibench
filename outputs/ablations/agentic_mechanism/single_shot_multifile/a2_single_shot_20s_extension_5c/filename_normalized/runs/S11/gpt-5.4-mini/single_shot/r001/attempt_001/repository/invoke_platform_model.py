from google import genai
from google.genai import types
from model_client import get_platform_client, get_platform_model_id
from model_models import PlatformRequest, normalize_platform_text


def invoke_platform_model(prompt, system_instruction=None, temperature=0.2, max_output_tokens=512):
    client = get_platform_client()
    model_id = get_platform_model_id()
    request = PlatformRequest(prompt=prompt, system_instruction=system_instruction, temperature=temperature, max_output_tokens=max_output_tokens)
    config = types.GenerateContentConfig(
        temperature=request.temperature,
        max_output_tokens=request.max_output_tokens,
        system_instruction=request.system_instruction,
    )
    response = client.models.generate_content(
        model=model_id,
        contents=normalize_platform_text(request.prompt),
        config=config,
    )
    return response.text if hasattr(response, "text") else str(response)
