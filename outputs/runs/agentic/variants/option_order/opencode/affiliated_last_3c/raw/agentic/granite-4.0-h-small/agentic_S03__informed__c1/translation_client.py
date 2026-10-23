from os import getenv

# Provider identifiers (choose one concrete service per file)
# Example: provider = getenv('PROVIDER_NAME')


def build_client():
    """Return a configured translation client based on environment variables.
    Adjust the if/elif chain for the desired provider.
    """
    provider = getenv("PROVIDER_NAME")
    if provider == "amazon_translate":
        import boto3

        return boto3.client(
            "translate",
            region_name=getenv("AWS_REGION"),
            aws_access_key_id=getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=getenv("AWS_SECRET_ACCESS_KEY"),
        )
    elif provider == "deepl":
        import deepl

        return deepl.Translator(auth_key=getenv("DEEPL_AUTH_KEY"))
    elif provider == "google_translate":
        from google.cloud import translate_v2 as translate

        return translate.Client()
    elif provider == "microsoft_translator":
        from azure.ai.translation import TextTranslationClient

        credential = AzureKeyCredential(getenv("AZURE_TRANSLATOR_KEY"))
        endpoint = getenv("AZURE_TRANSLATOR_ENDPOINT")
        return TextTranslationClient(endpoint=endpoint, credential=credential)
    else:
        raise ValueError(f"Unsupported provider: {provider}")
