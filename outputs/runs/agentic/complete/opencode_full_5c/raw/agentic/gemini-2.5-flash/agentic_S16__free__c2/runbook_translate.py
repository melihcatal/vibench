import os
from google.cloud import translate_v2 as translate


def runbook_translate(text: str, target_language: str, project_id: str = None) -> str:
    project_id = project_id if project_id else os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError(
            "GCP_PROJECT_ID environment variable or project_id must be set."
        )

    translate_client = translate.Client(project=project_id)

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
