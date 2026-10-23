import os
import google.cloud.speech as speech

# Credentials via GOOGLE_APPLICATION_CREDENTIALS
client = speech.SpeechClient()

def transcribe_qa_sample(audio_path: str, language_code: str = 'en-US') -> dict:
    """Transcribe a synthesized QA sample using Google Cloud Speech-to-Text.

    Args:
        audio_path (str): Path to audio file (local or GCS URI like gs://bucket/file).
        language_code (str): BCP-47 language tag.

    Returns:
        dict: Transcription result with transcript and confidence.
    """
    # Prepare audio config
    audio_config = speech.RecognitionAudio(uri=audio_path) if audio_path.startswith('gs://') else speech.RecognitionAudio(content=open(audio_path, 'rb').read())
    config = speech.RecognitionConfig(language_code=language_code, encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16)
    # Run synchronous transcription
    response = client.recognize(config=config, audio=audio_config)
    result = response.results[0]
    return {
        'transcript': result.alternatives[0].transcript,
        'confidence': result.alternatives[0].confidence
    }

if __name__ == '__main__':
    # Example: transcribe a locally stored demo MP3
    result = transcribe_qa_sample('demo.mp3')
    print('Transcription result:', result)
