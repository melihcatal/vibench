import boto3

def translate_platform_output(output, target_language, config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region", "us-east-1"))
    response = client.translate_text(
        Text=output["text"],
        SourceLanguageCode='en',
        TargetLanguageCode=target_language,
    )
    return response['TranslatedText']