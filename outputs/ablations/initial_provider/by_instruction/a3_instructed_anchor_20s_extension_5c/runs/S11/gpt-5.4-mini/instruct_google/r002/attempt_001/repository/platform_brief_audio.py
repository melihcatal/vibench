from google import genai

from model_client import get_default_model, get_google_client
from model_models import PlatformRequest


def platform_brief_audio(request: PlatformRequest):
    client = get_google_client()
    model_name = request.model or get_default_model()
    tts = genai.Client(api_key=client.api_key) if getattr(client, "api_key", None) else client
    response = tts.models.generate_content(
        model=model_name,
        contents=f"Create a spoken briefing from this text: {request.prompt}",
    )
    return {"audio_script": getattr(response, "text", None) or response.candidates[0].content.parts[0].text}
