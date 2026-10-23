"""
[LATER-STEP] Translate completed transcript segments via DeepL API.

Uses DeepL's translation service to translate AssemblyAI transcript
text into a target language.
Provider: DeepL API
SDK: deepl
Auth: DEEPL_AUTH_KEY
"""

import os
from typing import List, Optional, Dict, Any

import deepl

from speech_models import TranscriptResponse, Utterance


def get_deepl_client(auth_key: Optional[str] = None) -> deepl.Translator:
    """
    Create and return a DeepL translator client.

    Args:
        auth_key: Optional DeepL auth key. Falls back to DEEPL_AUTH_KEY env var.

    Returns:
        Configured deepl.Translator instance.

    Raises:
        ValueError: If no auth key is found.
    """
    key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
    if not key:
        raise ValueError(
            "DeepL auth key not found. Set DEEPL_AUTH_KEY environment variable or pass auth_key."
        )
    return deepl.Translator(key)


def translate_transcript(
    transcript: TranscriptResponse,
    target_lang: str = "EN",
    source_lang: Optional[str] = None,
    preserve_formatting: bool = True,
    formality: Optional[str] = None,
) -> TranscriptResponse:
    """
    Translate the full transcript text into a target language using DeepL.

    Args:
        transcript: Normalized TranscriptResponse with full_text to translate.
        target_lang: Target language code (e.g., 'EN', 'DE', 'FR', 'ES', 'JA').
        source_lang: Source language code (optional; DeepL auto-detects if None).
        preserve_formatting: Preserve sentence formatting in translation.
        formality: Formality level ('more' or 'less').

    Returns:
        TranscriptResponse with translated text in full_text and utterances.

    Raises:
        deepl.DeepLError: If translation fails.
    """
    client = get_deepl_client()

    translate_kwargs = {
        "target_lang": target_lang,
    }
    if source_lang:
        translate_kwargs["source_lang"] = source_lang
    if formality:
        translate_kwargs["formality"] = formality

    # Translate the full text
    full_result = client.translate_text(
        transcript.full_text,
        **translate_kwargs,
    )

    # Translate individual utterances preserving speaker labels
    translated_utterances = []
    for utterance in transcript.utterances:
        if utterance.text.strip():
            utt_result = client.translate_text(
                utterance.text,
                **translate_kwargs,
            )
            translated_utterance = Utterance(
                speaker=utterance.speaker,
                text=utt_result.text,
                words=utterance.words,
                start_ms=utterance.start_ms,
                end_ms=utterance.end_ms,
                confidence=utterance.confidence,
                sentiment=utterance.sentiment,
            )
            translated_utterances.append(translated_utterance)
        else:
            translated_utterances.append(utterance)

    # Build translated response
    translated_response = TranscriptResponse(
        transcript_id=transcript.transcript_id,
        audio_url=transcript.audio_url,
        full_text=full_result.text,
        utterances=translated_utterances,
        words=transcript.words,
        status=transcript.status,
        language_code=target_lang.lower(),
        duration_ms=transcript.duration_ms,
        created_at=transcript.created_at,
    )

    return translated_response


def translate_segments(
    texts: List[str],
    target_lang: str = "EN",
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Translate a list of individual text segments via DeepL.

    Args:
        texts: List of text strings to translate.
        target_lang: Target language code.
        source_lang: Source language code (optional).
        formality: Formality level.

    Returns:
        List of dicts with 'original', 'translated', and 'detected_source_lang'.
    """
    client = get_deepl_client()

    # Filter out empty strings
    non_empty = [(i, t) for i, t in enumerate(texts) if t.strip()]
    if not non_empty:
        return [{"original": t, "translated": "", "detected_source_lang": None} for t in texts]

    indices = [i for i, _ in non_empty]
    texts_to_translate = [t for _, t in non_empty]

    translate_kwargs = {"target_lang": target_lang}
    if source_lang:
        translate_kwargs["source_lang"] = source_lang
    if formality:
        translate_kwargs["formality"] = formality

    results_batch = client.translate_text(
        texts_to_translate,
        **translate_kwargs,
    )

    # Reconstruct full result list preserving order
    results = []
    for i, text in enumerate(texts):
        if i in indices:
            idx = indices.index(i)
            result = results_batch[idx]
            results.append({
                "original": text,
                "translated": result.text,
                "detected_source_lang": result.detected_source_lang,
            })
        else:
            results.append({
                "original": text,
                "translated": "",
                "detected_source_lang": None,
            })

    return results


def main():
    """CLI entry point for translating a transcript."""
    import argparse

    parser = argparse.ArgumentParser(description="Translate transcript with DeepL")
    parser.add_argument("transcript_id", help="Transcript ID (to fetch full transcript)")
    parser.add_argument("--target", required=True, help="Target language code (e.g., EN, DE, FR, ES)")
    parser.add_argument("--source", help="Source language code (optional)")
    parser.add_argument("--formality", choices=["more", "less"], help="Formality level")

    args = parser.parse_args()

    # Import here to avoid circular dependency in demo
    from poll_transcription import poll_transcription

    transcript = poll_transcription(args.transcript_id)

    translated = translate_transcript(
        transcript=transcript,
        target_lang=args.target,
        source_lang=args.source,
        formality=args.formality,
    )

    print(f"Translated transcript (target: {translated.language_code}):")
    print(f"\n{translated.full_text}")

    return translated


if __name__ == "__main__":
    main()
