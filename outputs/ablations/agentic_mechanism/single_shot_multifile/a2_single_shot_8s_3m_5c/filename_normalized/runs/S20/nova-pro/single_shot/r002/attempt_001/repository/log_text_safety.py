import os
from azure.ai.contentsafety import ContentSafetyClient, ContentSafetyKeyCredential
from azure.ai.contentsafety.models import Screen, TextScreen

def check_log_safety(log_text):
    endpoint = os.environ['CONTENT_SAFETY_ENDPOINT']
    key = os.environ['CONTENT_SAFETY_KEY']
    client = ContentSafetyClient(endpoint=endpoint, credential=ContentSafetyKeyCredential(key))
    screen = Screen(text=TextScreen(content=log_text))
    result = client.screen(screen)
    return result.text_results[0].hate_result.severity, result.text_results[0].violence_result.severity

log_text = 'This is a sample log text.'
print(check_log_safety(log_text))