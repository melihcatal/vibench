import boto3

from speech_models import TranscriptChunk


def live_caption_translate(chunks, target_language="es"):
    client = boto3.client("translate", region_name="us-east-1")
    for chunk in chunks:
        result = client.translate_text(Text=chunk.text, SourceLanguageCode="en", TargetLanguageCode=target_language)
        yield TranscriptChunk(text=result["TranslatedText"], is_final=chunk.is_final)
