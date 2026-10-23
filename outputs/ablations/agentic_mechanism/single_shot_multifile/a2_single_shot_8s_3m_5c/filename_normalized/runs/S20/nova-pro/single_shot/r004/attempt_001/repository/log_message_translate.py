import os
import google.auth
from google.cloud import translate_v2 as translate

credentials, project = google.auth.default()
translate_client = translate.Client(credentials=credentials)

log_message = 'User login failed due to invalid credentials'
translation = translate_client.translate(log_message, target_language='es')
print(translation['translatedText'])
