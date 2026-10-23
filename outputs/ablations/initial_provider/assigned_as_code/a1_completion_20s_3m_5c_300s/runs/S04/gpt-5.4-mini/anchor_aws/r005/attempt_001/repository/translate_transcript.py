import boto3


def translate_transcript(payload, config=None):
    client = boto3.client("translate", region_name=(config or {}).get("region"))
    segments = payload.get("segments", [])
    target_language = payload["target_language"]
    translated = []
    for segment in segments:
        text = segment.get("transcript") or segment.get("text") or ""
        response = client.translate_text(Text=text, SourceLanguageCode=payload["source_language"], TargetLanguageCode=target_language)
        translated.append({"text": response["TranslatedText"], "start_time": segment.get("start_time"), "end_time": segment.get("end_time")})
    return {"target_language": target_language, "segments": translated}
