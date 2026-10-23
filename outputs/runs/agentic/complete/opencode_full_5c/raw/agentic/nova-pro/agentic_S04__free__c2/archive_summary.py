import boto3

comprehend_client = boto3.client("comprehend")


def archive_summary(transcript_text):
    response = comprehend_client.summarize_text(Text=transcript_text, LanguageCode="en")
    return response["SummaryText"]
