import os
import boto3

class ComplianceNoteTranslateRequest:
    def __init__(self, text: str, source_language_code: str, target_language_code: str):
        self.text = text
        self.source_language_code = source_language_code
        self.target_language_code = target_language_code

class ComplianceNoteTranslateResponse:
    def __init__(self, translated_text: str, source_language_code: str, target_language_code: str):
        self.translated_text = translated_text
        self.source_language_code = source_language_code
        self.target_language_code = target_language_code

def translate_compliance_note(request: ComplianceNoteTranslateRequest) -> ComplianceNoteTranslateResponse:
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    translate_client = boto3.client("translate", region_name=region_name)

    translated_text = ""
    try:
        response = translate_client.translate_text(
            Text=request.text,
            SourceLanguageCode=request.source_language_code,
            TargetLanguageCode=request.target_language_code
        )
        translated_text = response['TranslatedText']

    except Exception as e:
        # In a real scenario, you'd want more robust error handling and logging.
        print(f"Error during translation: {e}")
        translated_text = f"Error: {e}"

    return ComplianceNoteTranslateResponse(
        translated_text=translated_text,
        source_language_code=request.source_language_code,
        target_language_code=request.target_language_code
    )