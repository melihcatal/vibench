from google.cloud.vision import types

def normalize_response(response):
    normalized_response = {}
    normalized_response['text'] = response.full_text_annotation.text
    normalized_response['layout'] = response.full_text_annotation
    normalized_response['tables'] = response.full_text_annotation.pages[0].tables
    return normalized_response