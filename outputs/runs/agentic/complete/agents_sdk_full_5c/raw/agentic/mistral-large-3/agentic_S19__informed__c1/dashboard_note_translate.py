import boto3
from observability_models import TranslationRequest, TranslationResponse


def translate_dashboard_note(request: TranslationRequest) -> TranslationResponse:
    client = boto3.client(
        "translate",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    )
    
    response = client.translate_text(
        Text=request.text,
        SourceLanguageCode="auto",
        TargetLanguageCode=request.target_locale.split("-")[0]
    )
    
    return TranslationResponse(
        translated_text=response["TranslatedText"]
    )