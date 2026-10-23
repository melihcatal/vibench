import os
from google.cloud import translate_v2 as translate


def get_client():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"
    return translate.Client()
