import os
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest
from google.cloud import texttospeech  # concrete Google Cloud Text-to-Speech client

def platform_brief_audio(output_text: str, voice_name: str = 'en-US-Wavenet-D') -> bytes:
    """
    Converts the model output text into a short spoken audio clip using Google Cloud Text-to-Speech.
    Returns the binary audio data (OGG_OPUS format).
    """
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=output_text)
    voice = texttospeech.VoiceSelectionParams(language_code='en-US', name=voice_name)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.OGG_OPUS)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    return response.audio_content

if __name__ == '__main__':
    client = ManagedModelClient()
    req = ModelInvocationRequest(
        model='projects/{}/locations/{}/publishers/google/models/gemma'.format(
            os.getenv('GOOGLE_CLOUD_PROJECT'), os.getenv('GCLOUD_LOCATION', 'us-central1')
        ),
        parameters={'temperature': 0.7},
        messages=[{'role': 'user', 'content': 'Summarize the plot of "Moby Dick" in two sentences.'}],
    )
    resp = client.invoke(req)
    audio_blob = platform_brief_audio(resp.generated_text)
    # Write to a temporary file for demo purposes
    with open('brief.mp3', 'wb') as f:
        f.write(audio_blob)
    print('Audio briefing generated, saved as brief.mp3')
