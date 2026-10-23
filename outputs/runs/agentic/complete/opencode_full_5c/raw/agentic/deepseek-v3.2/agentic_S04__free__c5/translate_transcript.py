from google.cloud import translate_v2 as translate


def translate_transcript_segments(transcript_segments, target_language="es"):
    """Translate completed transcript segments using Google Cloud Translation API."""
    client = translate.Client()

    translated_segments = []

    for segment in transcript_segments:
        if isinstance(segment, dict):
            text = segment.get("transcript", "")
        else:
            text = segment

        if text:
            result = client.translate(text, target_language=target_language)
            translated_text = result["translatedText"]

            translated_segment = {
                "original_text": text,
                "translated_text": translated_text,
                "target_language": target_language,
                "detected_language": result.get("detectedSourceLanguage", "en"),
            }

            if isinstance(segment, dict):
                translated_segment.update(
                    {k: v for k, v in segment.items() if k != "transcript"}
                )
                translated_segment["original_transcript"] = segment.get(
                    "transcript", ""
                )

            translated_segments.append(translated_segment)

    return translated_segments


if __name__ == "__main__":
    segments = [
        {
            "transcript": "Hello, welcome to our meeting.",
            "start_time": 0.0,
            "end_time": 2.5,
        },
        {
            "transcript": "Today we will discuss the quarterly results.",
            "start_time": 2.5,
            "end_time": 5.0,
        },
    ]

    translated = translate_transcript_segments(segments, target_language="es")
    for item in translated:
        print(f"Translated: {item['translated_text']}")
