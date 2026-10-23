from google.cloud import translate_v3

from translation_client import get_translation_client


def summarize_quality_issues(translations, config=None):
    config = config or {}
    client = get_translation_client(config)
    parent = f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    response = client.detect_translation_issues(request={
        "parent": parent,
        "translations": translations,
   })
    quality_issues = []
    for issue in response.issues:
        quality_issues.append({
            "description": issue.description,
            "severity": issue.severity,
       })
    return quality_issues