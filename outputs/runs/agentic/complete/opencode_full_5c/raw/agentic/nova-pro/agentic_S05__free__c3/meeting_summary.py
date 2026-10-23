import boto3


def summarize_text(text):
    comprehend_client = boto3.client("comprehend", region_name="us-west-2")
    response = comprehend_client.detect_dominant_language(Text=text)
    lang_code = response["Languages"][0]["LanguageCode"]
    summary_response = comprehend_client.start_document_text_detection(
        DocumentLocation={
            "S3Object": {"Bucket": "your-bucket-name", "Name": "your-document-name"}
        }
    )
    return summary_response
