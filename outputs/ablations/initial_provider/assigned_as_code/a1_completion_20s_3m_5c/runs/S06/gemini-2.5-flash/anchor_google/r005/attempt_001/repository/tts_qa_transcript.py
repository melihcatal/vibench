import io
from google.cloud import speech_v1p1beta1 as speech

def tts_qa_transcript(payload, config=None):
    config = config or {}
    client = speech.SpeechClient()

    audio_content = payload["audio_bytes"] # This should be the raw audio bytes
    sample_rate_hertz = config.get("sample_rate_hertz", 16000)
    language_code = config.get("language_code", "en-US")
    audio_encoding = config.get("audio_encoding", "MP3") # Or LINEAR16, FLAC, etc.

    audio = speech.RecognitionAudio(content=audio_content)

    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding[audio_encoding],
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )

    response = client.recognize(config=recognition_config, audio=audio)

    transcripts = []
    for result in response.results:
        transcripts.append({"transcript": result.alternatives[0].transcript, "confidence": result.alternatives[0].confidence})

    return {"transcripts": transcripts}
