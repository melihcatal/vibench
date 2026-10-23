from google.cloud import speech_v1p1beta1 as speech


def tts_qa_transcript(payload, config=None):
    config = config or {}
    client = speech.SpeechClient()
    response = client.recognize(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            language_code=config.get("language_code", "en-US"),
        ),
        audio=speech.RecognitionAudio(content=payload["audio_bytes"]),
    )
    return {"transcript": " ".join(result.alternatives[0].transcript for result in response.results)}
