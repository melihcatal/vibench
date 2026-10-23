from azure.ai.translation.text import TextTranslationClient, TextTranslationApiKeyCredential

def translate_platform_output(text, to_language):
    endpoint = "https://<your-translation-resource-name>.cognitiveservices.azure.com/"
    key = "<your-translation-resource-key>"
    credential = TextTranslationApiKeyCredential(key)
    client = TextTranslationClient(endpoint=endpoint, credential=credential)
    result = client.translate([text], to_language)
    return result[0].translations[0].text