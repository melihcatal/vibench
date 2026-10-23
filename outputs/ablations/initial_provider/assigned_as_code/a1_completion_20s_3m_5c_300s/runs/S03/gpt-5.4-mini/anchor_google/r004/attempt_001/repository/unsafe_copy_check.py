from google.cloud import language_v1

from translation_client import get_config


def unsafe_copy_check(payload, config=None):
    config = get_config(config)
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=payload["text"], type_=language_v1.Document.Type.PLAIN_TEXT)
    analysis = client.analyze_entities(request={"document": document, "encoding_type": language_v1.EncodingType.UTF8})
    flagged = [entity.name for entity in analysis.entities if entity.salience > 0.2]
    return {
        "flagged_terms": flagged,
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
        "project_id": config["project_id"],
    }
