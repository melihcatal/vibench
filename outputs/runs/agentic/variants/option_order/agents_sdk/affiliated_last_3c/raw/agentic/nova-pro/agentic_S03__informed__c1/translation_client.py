import os
from google.cloud import translate_v2 as translate

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'

translate_client = translate.Client()