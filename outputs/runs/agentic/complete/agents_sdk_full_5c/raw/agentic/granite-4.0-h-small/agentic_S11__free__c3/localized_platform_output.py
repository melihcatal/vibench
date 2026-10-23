import json
from google.cloud import translate_v2 as translate
from model_models import NormalizedResponse

def localized_platform_output(normalized: NormalizedResponse, target_lang: str = "es") -> Dict[str, Any]:
    """
    Translate platform model output to another locale using Google Cloud Translation.
    Returns a new NormalizedResponse-like dict with translated text and original
    metadata preserved.
    """
    output_text = normalized.data.get("generated_text", "")
    if not output_text:
        raise ValueError("No generated text to translate")
    print(f"Translating output to {target_lang}...")
    client = translate.Client()
    result = client.translate(output_text, target_language=target_lang)
    translated_text = result.get("translatedText", "")
    # Preserve original metadata and add translation info
    new_data = normalized.data.copy()
    new_data["generated_text"] = translated_text
    new_data["source_lang"] = normalized.data.get("source_lang", "en")
    new_data["target_lang"] = target_lang
    return {
        "output": new_data,
        "translation": {
            "service": "google",
            "target": target_lang,
            "engine_id": result.get("detectedSourceLanguage")
        }
    }

# Example usage for local testing
if __name__ == "__main__":
    from model_client import ManagedModelClient
    client = ManagedModelClient()
    deployment = os.getenv("DEPLOYMENT_ID")
    txt = "Hello, world!"
    resp = client.invoke_model(deployment, txt, stream=False)
    norm = NormalizedResponse.from_openai(resp)
    localized = localized_platform_output(norm, target_lang="es")
    print(json.dumps(localized, indent=2))
