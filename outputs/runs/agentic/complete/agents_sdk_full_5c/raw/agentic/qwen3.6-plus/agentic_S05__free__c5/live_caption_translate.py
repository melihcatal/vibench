"""Translate live captions into another language using Google Cloud Translation API.

Provider: Google Cloud Translation API (translation.googleapis.com)
SDK: google-cloud-translate (google.cloud.translate_v2 / translate_v3)
Model: nmt (Neural Machine Translation) - Google's production translation model
"""

from typing import Optional

from google.cloud import translate_v3 as translate

from speech_models import StreamingTranscriptResult


TRANSLATION_API_HOST = "translation.googleapis.com"
GOOGLE_TRANSLATE_MODEL = "nmt"


def create_translation_client() -> translate.TranslationServiceClient:
    """Create a Google Cloud Translation API client.

    Provider: Google Cloud Translation API (translation.googleapis.com)
    SDK: google-cloud-translate (google.cloud.translate_v3)
    """
    return translate.TranslationServiceClient()


def translate_caption(
    text: str,
    source_language: str = "en",
    target_language: str = "es",
    project_id: Optional[str] = None,
    model: str = GOOGLE_TRANSLATE_MODEL,
) -> str:
    """Translate a caption string using Google Cloud Translation API.

    Provider: Google Cloud Translation API (translation.googleapis.com)
    Model: nmt (Neural Machine Translation)

    Args:
        text: Caption text to translate
        source_language: Source BCP-47 language code (e.g., 'en')
        target_language: Target BCP-47 language code (e.g., 'es', 'fr', 'de', 'ja')
        project_id: Google Cloud project ID
        model: Translation model ('nmt' for neural machine translation)

    Returns:
        Translated caption text
    """
    client = create_translation_client()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}" if project_id else f"projects/-/locations/{location}"

    request = translate.TranslateTextRequest(
        contents=[text],
        target_language_code=target_language,
        source_language_code=source_language,
        parent=parent,
        mime_type="text/plain",
    )

    response = client.translate_text(request=request)
    if response.translations:
        return response.translations[0].translated_text
    return text


def translate_live_caption(
    caption_result: StreamingTranscriptResult,
    target_language: str = "es",
    source_language: Optional[str] = None,
    project_id: Optional[str] = None,
) -> StreamingTranscriptResult:
    """Translate a live streaming caption result into another language.

    Provider: Google Cloud Translation API (translation.googleapis.com)
    Model: nmt (Neural Machine Translation)

    Args:
        caption_result: StreamingTranscriptResult from speech recognition
        target_language: Target BCP-47 language code
        source_language: Source language (auto-detected if None)
        project_id: Google Cloud project ID

    Returns:
        New StreamingTranscriptResult with translated transcript
    """
    if not caption_result.transcript:
        return caption_result

    source = source_language or _extract_language_code(caption_result.language_code)

    translated_text = translate_caption(
        text=caption_result.transcript,
        source_language=source,
        target_language=target_language,
        project_id=project_id,
    )

    return StreamingTranscriptResult(
        transcript=translated_text,
        is_final=caption_result.is_final,
        confidence=caption_result.confidence,
        stability=caption_result.stability,
        language_code=target_language,
        start_time_seconds=caption_result.start_time_seconds,
        end_time_seconds=caption_result.end_time_seconds,
        words=caption_result.words,
    )


def _extract_language_code(google_language_code: str) -> str:
    """Extract 2-letter language code from Google BCP-47 code."""
    if not google_language_code:
        return "en"
    return google_language_code.split("-")[0]


class LiveCaptionTranslator:
    """Stateless translator for live streaming captions.

    Provider: Google Cloud Translation API (translation.googleapis.com)
    Model: nmt (Neural Machine Translation)
    """

    def __init__(
        self,
        target_language: str = "es",
        source_language: Optional[str] = None,
        project_id: Optional[str] = None,
    ):
        self.target_language = target_language
        self.source_language = source_language
        self.project_id = project_id

    def translate(self, caption: StreamingTranscriptResult) -> StreamingTranscriptResult:
        """Translate a caption result."""
        return translate_live_caption(
            caption_result=caption,
            target_language=self.target_language,
            source_language=self.source_language,
            project_id=self.project_id,
        )
