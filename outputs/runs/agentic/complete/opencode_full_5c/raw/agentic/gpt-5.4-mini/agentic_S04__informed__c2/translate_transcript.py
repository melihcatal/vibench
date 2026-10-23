from deep_translator import GoogleTranslator


def translate_transcript(segments, target_language="en"):
    translator = GoogleTranslator(source="auto", target=target_language)
    return [
        {
            "text": translator.translate(segment.get("text", "")),
            "start": segment.get("start"),
            "end": segment.get("end"),
        }
        for segment in segments
    ]
