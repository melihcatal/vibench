from google.cloud import translate_v3

def get_translation_client():
    return translate_v3.TranslationServiceClient()

def get_parent_path(project_id, location='global'):
    return f"projects/{project_id}/locations/{location}"
