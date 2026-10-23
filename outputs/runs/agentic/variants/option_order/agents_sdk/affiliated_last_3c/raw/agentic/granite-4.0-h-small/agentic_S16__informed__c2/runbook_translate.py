import os
from google.cloud.translate_v2 import Translate
from security_client import get_project_id

def runbook_translate(runbook_text: str, target='es') -> str:
    client = Translate()
    result = client.translate(runbook_text, target_language=target)
    return result['translatedText']
