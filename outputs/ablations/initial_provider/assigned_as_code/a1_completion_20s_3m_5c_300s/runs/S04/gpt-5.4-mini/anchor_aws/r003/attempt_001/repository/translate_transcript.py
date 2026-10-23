import boto3


def translate_transcript(payload, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region"))
    segments = payload.get("segments") or []
    target_language = payload["target_language"]
    translated = []
    for segment in segments:
        text = segment.get("transcript") or segment.get("text") or ""
        if text:
            response = client.translate_text(Text=text, SourceLanguageCode=payload.get("source_language", "auto"), TargetLanguageCode=target_language)
            translated.append({
                "text": response["TranslatedText"],
                "start_time": segment.get("start_time"),
                "end_time": segment.get("end_time"),
                "speaker": segment.get("speaker"),
            })
    return {"segments": translated, "target_language": target_language}
