from google.cloud import texttospeech

def get_client():
    return texttospeech.TextToSpeechClient()

def set_config(project_id):
    os.environ['GOOGLE_CLOUD_PROJECT'] = project_id