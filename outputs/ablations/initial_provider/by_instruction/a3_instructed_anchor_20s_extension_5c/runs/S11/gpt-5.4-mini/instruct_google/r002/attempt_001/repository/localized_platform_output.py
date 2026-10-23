from model_client import get_default_locale, get_default_model, get_google_client
from model_models import PlatformRequest


def localized_platform_output(request: PlatformRequest):
    client = get_google_client()
    model_name = request.model or get_default_model()
    locale = request.locale or get_default_locale()
    response = client.models.generate_content(
        model=model_name,
        contents=request.prompt,
        config={"system_instruction": f"Translate the response into {locale}."},
    )
    return {"locale": locale, "text": getattr(response, "text", None) or response.candidates[0].content.parts[0].text}
