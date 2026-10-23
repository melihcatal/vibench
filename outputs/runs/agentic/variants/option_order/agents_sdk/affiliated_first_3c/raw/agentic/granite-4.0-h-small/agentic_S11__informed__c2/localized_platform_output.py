import os
import json
from google.cloud import translate_v2 as translate
from model_models import PromptResponse

# ---------------------------------------------------------------------------
# Example: Google Cloud Translation integration for locale translation
# ---------------------------------------------------------------------------

# Set GOOGLE_APPLICATION_CREDENTIALS env var pointing to a JSON key file
if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
    raise RuntimeError("Set GOOGLE_APPLICATION_CREDENTIALS env var to a Google Cloud credentials JSON file")

# Create a client; the client automatically reads the credentials from env var
translate_client = translate.Client()


def translate_output(response: PromptResponse, target_locale: str = "es") -> PromptResponse:
    """Translate the generated text to the specified locale and return a new PromptResponse."""
    target = translate_client.translate(response.generated_text, target_language=target_locale)
    # The response from google.cloud.translate_v2 contains a 'translatedText' field
    translated_text = target.get('translatedText', '')
    enriched = response._replace(
        generated_text=translated_text,
        usage_info={"translation": {"target": target_locale, "original": response.model_id}}
    )
    return enriched

# Demo snippet (uncomment for quick test)
# if __name__ == "__main__":
#     prompt = input("Enter prompt: ")
#     raw = collect_platform_metadata(prompt)
#     translated = translate_output(raw, target_locale='fr')
#     print('\n--- TRANSLATED OUTPUT (FR) ---')
#     print(translated.generated_text)