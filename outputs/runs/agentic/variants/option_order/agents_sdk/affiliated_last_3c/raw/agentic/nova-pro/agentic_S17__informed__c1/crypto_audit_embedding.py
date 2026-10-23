import azure.ai.textanalytics

def embed_crypto_audit_notes(text):
    client = azure.ai.textanalytics.TextAnalyticsClient(endpoint=os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT'), credential=azure.identity.DefaultAzureCredential())
    result = client.extract_key_phrases(documents=[text])
    return result[0].key_phrases