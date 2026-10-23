from google.cloud import texttospeech


def get_tts_client():
    """Provides a configured Google Cloud Text-to-Speech client."""
    return texttospeech.TextToSpeechClient()


def get_translation_client():
    from google.cloud import translate_v2 as translate
    """Provides a configured Google Cloud Translation client."""
    return translate.Client()


def get_vertex_ai_prediction_client(project, location):
    from google.cloud import aiplatform
    """Provides a configured Google Cloud Vertex AI Prediction client."""
    aiplatform.init(project=project, location=location)
    return aiplatform.gapic.PredictionServiceClient()


def get_speech_to_text_client():
    from google.cloud import speech_v1p1beta1 as speech
    """Provides a configured Google Cloud Speech-to-Text client."""
    return speech.SpeechClient()