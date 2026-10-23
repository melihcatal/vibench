from azure.ai.contentsafety import ContentSafetyClient, ContentSafetyApiKeyCredential
from azure.ai.contentsafety.models import Screen, TextScreen

def check_platform_output_safety(text):
    endpoint = "https://<your-content-safety-resource-name>.cognitiveservices.azure.com/"
    key = "<your-content-safety-resource-key>"
    credential = ContentSafetyApiKeyCredential(key)
    client = ContentSafetyClient(endpoint=endpoint, credential=credential)
    screen = Screen(text=TextScreen(content=text))
    result = client.screen(screen)
    return result