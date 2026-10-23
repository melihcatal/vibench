from google.cloud import texttospeech

def normalize_synthesis_input(text):
    return texttospeech.SynthesisInput(text=text)

def normalize_synthesis_output(response):
    return response.audio_content