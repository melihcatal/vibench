from google.cloud import language_v1

def get_language_client():
    return language_v1.LanguageServiceClient()
