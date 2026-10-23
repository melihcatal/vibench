import boto3

transcribe_client = boto3.client("transcribe")
translate_client = boto3.client("translate")


def translate_transcript(transcript_text, target_language):
    response = translate_client.translate_text(
        Text=transcript_text,
        SourceLanguageCode="en",
        TargetLanguageCode=target_language,
    )
    return response["TranslatedText"]
