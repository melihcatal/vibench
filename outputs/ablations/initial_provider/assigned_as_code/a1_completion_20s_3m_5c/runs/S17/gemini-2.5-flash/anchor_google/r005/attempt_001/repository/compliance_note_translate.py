from security_models import ComplianceNoteTranslateConfig
from security_client import get_translate_client

def translate_compliance_notes(notes: list[str], config: ComplianceNoteTranslateConfig):
    client = get_translate_client(config.aws_region)
    translated_notes = []

    for note in notes:
        response = client.translate_text(
            Text=note,
            SourceLanguageCode=config.source_language_code,
            TargetLanguageCode=config.target_language_code,
        )
        translated_notes.append(response["TranslatedText"])
    
    return {"translated_notes": translated_notes}
