from typing import List, Dict


def summarize_moderation_decisions(decisions: List[Dict]) -> Dict:
    """
    Summarizes moderation decisions using Google Cloud Natural Language API.
    Provider: Google Cloud Natural Language
    """
    from google.cloud import language_v1
    from google.oauth2 import service_account
    import os

    credentials = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    client = language_v1.LanguageServiceClient(credentials=credentials)

    summary_text = "\n".join(
        [
            f"Text: {decision.get('text', 'N/A')}, "
            f"Allowed: {decision.get('allowed', False)}, "
            f"Reason: {decision.get('reason', 'N/A')}"
            for decision in decisions
        ]
    )

    document = language_v1.Document(
        content=summary_text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.analyze_entities(request={"document": document})

    entities = []
    for entity in response.entities:
        entities.append(
            {
                "name": entity.name,
                "type": language_v1.Entity.Type(entity.type_).name,
                "salience": entity.salience,
            }
        )

    return {
        "summary": summary_text,
        "key_entities": entities,
        "total_decisions": len(decisions),
        "allowed_count": sum(1 for d in decisions if d.get("allowed", False)),
        "blocked_count": sum(1 for d in decisions if not d.get("allowed", True)),
    }
