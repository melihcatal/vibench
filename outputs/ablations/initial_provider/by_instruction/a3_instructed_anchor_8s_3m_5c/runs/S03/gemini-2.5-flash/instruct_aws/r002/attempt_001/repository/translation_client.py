import boto3

def get_translate_client():
    """
    Provides a configured AWS Translate client.
    """\n    return boto3.client("translate")
