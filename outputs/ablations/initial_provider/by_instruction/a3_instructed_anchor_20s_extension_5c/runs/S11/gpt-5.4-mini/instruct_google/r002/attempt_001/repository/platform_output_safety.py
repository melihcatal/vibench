from google import genai

from model_client import get_default_model, get_google_client
from model_models import PlatformRequest


def platform_output_safety(request: PlatformRequest):
    client = get_google_client()
    model_name = request.model or get_default_model()
    response = client.models.generate_content(
        model=model_name,
        contents=request.prompt,
    )
    text = getattr(response, "text", None) or response.candidates[0].content.parts[0].text
    safety_client = genai.Client(api_key=client.api_key) if getattr(client, "api_key", None) else client
    safety = safety_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Assess this content for unsafe material and return a short verdict:\n{text}",
    )
    return {"text": text, "safety": getattr(safety, "text", None) or str(safety)}
