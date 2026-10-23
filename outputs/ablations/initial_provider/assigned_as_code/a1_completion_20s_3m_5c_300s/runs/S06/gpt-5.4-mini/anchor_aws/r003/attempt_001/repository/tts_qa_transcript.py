from google.cloud import speech_v1


def tts_qa_transcript(payload, config=None):
    config = config or {}
    client = speech_v1.SpeechClient()
    audio = payload["audio_bytes"]
    recognition_audio = speech_v1.RecognitionAudio(content=audio)
    recognition_config = speech_v1.RecognitionConfig(
        encoding=speech_v1.RecognitionConfig.AudioEncoding.MP3,
        language_code=payload.get("language_code", "en-US"),
    )
    response = client.recognize(config=recognition_config, audio=recognition_audio)
    transcript = " ".join(result.alternatives[0].transcript for result in response.results)
    return {"transcript": transcript}
