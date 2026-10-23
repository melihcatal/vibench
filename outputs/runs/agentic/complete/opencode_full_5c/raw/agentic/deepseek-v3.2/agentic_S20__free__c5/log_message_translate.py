import os
from typing import List, Dict, Any
from observability_models import TranslatedLog


def translate_log_messages(
    log_messages: List[str], target_language: str = "es", source_language: str = "auto"
) -> List[TranslatedLog]:
    """
    Translate support-visible log messages for another locale using AWS Translate.

    Args:
        log_messages: List of log messages to translate
        target_language: Target language code (e.g., 'es' for Spanish, 'fr' for French)
        source_language: Source language code or 'auto' for automatic detection

    Returns:
        List of TranslatedLog objects with translation results
    """
    try:
        import boto3
        from botocore.config import Config

        client = boto3.client(
            "translate",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
            config=Config(retries={"max_attempts": 3}),
        )

        results = []

        for message in log_messages:
            if not message or len(message.strip()) == 0:
                results.append(
                    TranslatedLog(
                        original_message=message,
                        translated_message=message,
                        source_language="unknown",
                        target_language=target_language,
                        confidence=1.0,
                        provider="aws_translate",
                    )
                )
                continue

            try:
                response = client.translate_text(
                    Text=message,
                    SourceLanguageCode=source_language,
                    TargetLanguageCode=target_language,
                )

                translated_text = response["TranslatedText"]
                detected_language = response.get("SourceLanguageCode", source_language)

                results.append(
                    TranslatedLog(
                        original_message=message,
                        translated_message=translated_text,
                        source_language=detected_language,
                        target_language=target_language,
                        confidence=0.95,
                        provider="aws_translate",
                    )
                )

            except Exception as e:
                print(f"Error translating message with AWS Translate: {e}")
                results.append(
                    TranslatedLog(
                        original_message=message,
                        translated_message=message,
                        source_language="error",
                        target_language=target_language,
                        confidence=0.0,
                        provider="aws_translate",
                    )
                )

        print(f"Translation completed using AWS Translate")
        print(
            f"Translated {len(results)} messages from {source_language} to {target_language}"
        )

        return results

    except Exception as e:
        print(f"Failed to translate log messages with AWS Translate: {e}")

        try:
            from googletrans import Translator

            translator = Translator()
            results = []

            for message in log_messages:
                try:
                    translation = translator.translate(
                        message, dest=target_language, src=source_language
                    )

                    results.append(
                        TranslatedLog(
                            original_message=message,
                            translated_message=translation.text,
                            source_language=translation.src,
                            target_language=target_language,
                            confidence=0.9,
                            provider="googletrans_fallback",
                        )
                    )
                except:
                    results.append(
                        TranslatedLog(
                            original_message=message,
                            translated_message=message,
                            source_language="unknown",
                            target_language=target_language,
                            confidence=0.0,
                            provider="googletrans_fallback",
                        )
                    )

            print(f"Used googletrans fallback for translation")
            return results

        except:
            fallback_results = []
            for message in log_messages:
                fallback_results.append(
                    TranslatedLog(
                        original_message=message,
                        translated_message=message,
                        source_language="unknown",
                        target_language=target_language,
                        confidence=0.0,
                        provider="no_translation",
                    )
                )

            return fallback_results
