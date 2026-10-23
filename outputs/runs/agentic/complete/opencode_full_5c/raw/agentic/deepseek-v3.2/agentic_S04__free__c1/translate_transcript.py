from google.cloud import translate_v2 as translate


def translate_transcript_segments(segments, target_language="es"):
    """Translate completed transcript segments using Google Cloud Translation API."""
    client = translate.Client()

    translated_segments = []

    for segment in segments:
        if isinstance(segment, dict):
            transcript_text = segment.get("transcript", "")
        else:
            transcript_text = (
                segment.transcript if hasattr(segment, "transcript") else str(segment)
            )

        if transcript_text:
            result = client.translate(
                transcript_text, target_language=target_language, model="nmt"
            )

            translated_segment = {
                "original": transcript_text,
                "translated": result["translatedText"],
                "detected_language": result.get("detectedSourceLanguage", "en"),
                "target_language": target_language,
            }

            if isinstance(segment, dict):
                translated_segment.update(
                    {
                        "start_time": segment.get("start_time"),
                        "end_time": segment.get("end_time"),
                        "speaker_tag": segment.get("speaker_tag"),
                    }
                )

            translated_segments.append(translated_segment)

    return translated_segments
