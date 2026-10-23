import os
from typing import Dict, Any, List
from google.cloud import aiplatform
from google.cloud import translate_v2 as translate


def translate_model_output(
    text: str, target_language: str = "es", source_language: str = "en"
) -> Dict[str, Any]:
    """Translate platform model output for another locale using Google Cloud Translation."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")

    if not project_id:
        return {
            "original_text": text,
            "translated_text": text,
            "target_language": target_language,
            "error": "GOOGLE_CLOUD_PROJECT environment variable not set",
        }

    try:
        translate_client = translate.Client()

        result = translate_client.translate(
            text, target_language=target_language, source_language=source_language
        )

        return {
            "original_text": text,
            "translated_text": result["translatedText"],
            "target_language": target_language,
            "source_language": result.get("detectedSourceLanguage", source_language),
            "model": "google-cloud-translation-api",
            "project_id": project_id,
        }

    except Exception as e:
        return {
            "original_text": text,
            "translated_text": text,
            "target_language": target_language,
            "error": str(e),
            "model": "google-cloud-translation-api",
        }


def localize_with_vertex_ai(
    text: str, target_locale: str = "es-ES", deployment_name: str = "text-bison"
) -> Dict[str, Any]:
    """Localize text using Vertex AI for cultural adaptation."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    aiplatform.init(project=project_id, location=location)

    endpoint = aiplatform.Endpoint(
        endpoint_name=f"projects/{project_id}/locations/{location}/endpoints/{deployment_name}"
    )

    locale_prompts = {
        "es-ES": "Traduce y adapta culturalmente el siguiente texto al español de España: ",
        "fr-FR": "Traduisez et adaptez culturellement le texte suivant au français de France: ",
        "de-DE": "Übersetzen und kulturell anpassen Sie den folgenden Text an Deutsch: ",
        "ja-JP": "次のテキストを日本語に翻訳し、文化的に適応させてください: ",
        "zh-CN": "将以下文本翻译并文化适应为简体中文: ",
    }

    prompt_prefix = locale_prompts.get(target_locale, f"Translate to {target_locale}: ")
    full_prompt = f"{prompt_prefix}\n\n{text}"

    instances = [{"content": full_prompt}]
    parameters = {"temperature": 0.3, "maxOutputTokens": 1024, "topP": 0.95, "topK": 40}

    try:
        response = endpoint.predict(instances=instances, parameters=parameters)

        localized_text = ""
        if hasattr(response, "predictions") and response.predictions:
            if len(response.predictions) > 0:
                pred = response.predictions[0]
                if isinstance(pred, dict) and "content" in pred:
                    localized_text = pred["content"]
                elif hasattr(pred, "content"):
                    localized_text = pred.content
                else:
                    localized_text = str(pred)

        return {
            "original_text": text,
            "localized_text": localized_text,
            "target_locale": target_locale,
            "model_deployment": deployment_name,
            "project_id": project_id,
            "localization_method": "vertex-ai-prompt-based",
        }

    except Exception as e:
        return {
            "original_text": text,
            "localized_text": text,
            "target_locale": target_locale,
            "error": str(e),
            "model_deployment": deployment_name,
        }


def batch_translate_outputs(
    texts: List[str], target_language: str = "es"
) -> List[Dict[str, Any]]:
    """Batch translate multiple model outputs."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")

    if not project_id:
        return [
            {
                "original_text": text,
                "translated_text": text,
                "target_language": target_language,
                "error": "GOOGLE_CLOUD_PROJECT not set",
                "text_index": i,
            }
            for i, text in enumerate(texts)
        ]

    try:
        translate_client = translate.Client()

        results = []
        for i, text in enumerate(texts):
            result = translate_client.translate(text, target_language=target_language)

            results.append(
                {
                    "original_text": text,
                    "translated_text": result["translatedText"],
                    "target_language": target_language,
                    "source_language": result.get("detectedSourceLanguage", "en"),
                    "text_index": i,
                    "model": "google-cloud-translation-api",
                }
            )

        return results

    except Exception as e:
        return [
            {
                "original_text": text,
                "translated_text": text,
                "target_language": target_language,
                "error": str(e),
                "text_index": i,
            }
            for i, text in enumerate(texts)
        ]


def detect_language(text: str) -> Dict[str, Any]:
    """Detect the language of text using Google Cloud Translation."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")

    if not project_id:
        return {
            "text": text[:100],
            "detected_language": "unknown",
            "confidence": 0.0,
            "error": "GOOGLE_CLOUD_PROJECT not set",
        }

    try:
        translate_client = translate.Client()

        result = translate_client.detect_language(text)

        return {
            "text": text[:100],
            "detected_language": result["language"],
            "confidence": result["confidence"],
            "is_reliable": result["isReliable"] if "isReliable" in result else True,
            "model": "google-cloud-translation-api",
            "project_id": project_id,
        }

    except Exception as e:
        return {
            "text": text[:100],
            "detected_language": "unknown",
            "confidence": 0.0,
            "error": str(e),
            "model": "google-cloud-translation-api",
        }


def get_supported_locales() -> Dict[str, List[str]]:
    """Get supported locales for different localization methods."""
    return {
        "google-translation": [
            "es",
            "fr",
            "de",
            "ja",
            "zh-CN",
            "zh-TW",
            "ko",
            "ru",
            "ar",
            "hi",
        ],
        "vertex-ai-localization": [
            "es-ES",
            "fr-FR",
            "de-DE",
            "ja-JP",
            "zh-CN",
            "en-US",
            "en-GB",
        ],
        "common_locales": [
            {"code": "en-US", "name": "English (US)"},
            {"code": "es-ES", "name": "Spanish (Spain)"},
            {"code": "fr-FR", "name": "French (France)"},
            {"code": "de-DE", "name": "German (Germany)"},
            {"code": "ja-JP", "name": "Japanese (Japan)"},
            {"code": "zh-CN", "name": "Chinese (Simplified)"},
        ],
    }


if __name__ == "__main__":
    test_text = "Artificial intelligence is transforming how we work and live."

    # Test translation
    translation = translate_model_output(test_text, "es")
    print(f"Translation: {translation['translated_text'][:100]}...")

    # Test localization
    localization = localize_with_vertex_ai(test_text, "es-ES")
    print(f"Localization: {localization['localized_text'][:100]}...")

    # Test language detection
    detection = detect_language(test_text)
    print(
        f"Detected language: {detection['detected_language']} (confidence: {detection['confidence']})"
    )
