import os
from model_client import ManagedModelClient
from model_models import ModelRequest, ModelResponse
from google.cloud.translate_v2 import Client as TranslateClient

def localize_output(text: str, target_locale: str = "es") -> str:
    """Translate the model output to another locale using Google Cloud Translation."""
    translate = TranslateClient()
    result = translate.translate(text, target_language=target_locale)
    return result["translatedText"]

if __name__ == "__main__":
    demo_req = ModelRequest(payload={"system": "You are concise.", "user": "Describe photosynthesis."},
                            config={"provider": "anthropic"})
    client = ManagedModelClient(provider=demo_req.config["provider"], api_key=os.getenv(demo_req.config["provider"] + "_API_KEY"))
    raw = client.chat(compute(demo_req.dict()))
    translated = localize_output(raw.get("output", ""), target_locale="es")
    print(json.dumps({"original": raw.get("output"), "translated": translated}, indent=2))
