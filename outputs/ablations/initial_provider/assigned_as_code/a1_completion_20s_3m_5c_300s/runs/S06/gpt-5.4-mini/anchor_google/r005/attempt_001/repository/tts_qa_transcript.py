from google.cloud import speech_v1p1beta1 as speech


def tts_qa_transcript(payload, config=None):
    client = speech.SpeechClient()
    response = client.recognize(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            language_code=payload.get("language_code", "en-US"),
        ),
        audio=speech.RecognitionAudio(content=payload["audio_bytes"]),
    )
    transcript = " ".join(result.alternatives[0].transcript for result in response.results)
    return {"transcript": transcript}
