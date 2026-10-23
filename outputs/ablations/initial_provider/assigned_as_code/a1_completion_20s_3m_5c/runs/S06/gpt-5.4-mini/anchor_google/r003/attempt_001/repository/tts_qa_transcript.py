from google.cloud import speech_v1p1beta1 as speech


def tts_qa_transcript(payload, config=None):
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=payload["audio_bytes"])
    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        language_code=(config or {}).get("language_code", "en-US"),
    )
    response = client.recognize(config=recognition_config, audio=audio)
    transcript = " ".join(result.alternatives[0].transcript for result in response.results)
    return {"transcript": transcript, "provider": "google_speech_v1p1beta1"}
