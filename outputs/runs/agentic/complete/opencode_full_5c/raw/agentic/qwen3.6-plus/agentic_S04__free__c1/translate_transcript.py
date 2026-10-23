from typing import Optional

from speech_client import request_lemur_task
from speech_models import (
    TranslationRequest,
    TranslationResult,
)


def translate_transcript(
    transcript_id: str,
    target_language: str = "es",
    custom_prompt: Optional[str] = None,
) -> TranslationResult:
    request = TranslationRequest(
        transcript_id=transcript_id,
        target_language=target_language,
        prompt_template=custom_prompt,
    )

    response = request_lemur_task(
        transcript_ids=[transcript_id],
        prompt=request.to_lemur_payload()["prompt"],
        final_model="assemblyai-mistral-7b",
        max_output_size=3000,
    )

    return TranslationResult.from_lemur_response(
        transcript_id=transcript_id,
        target_language=target_language,
        response=response,
    )


def translate_segments(
    transcript_id: str,
    translations: dict[str, str],
) -> list[TranslationResult]:
    results = []
    for target_lang, custom_prompt in translations.items():
        result = translate_transcript(
            transcript_id=transcript_id,
            target_language=target_lang,
            custom_prompt=custom_prompt,
        )
        results.append(result)
    return results
