from google.cloud import speech


def diarized_transcript(payload, config=None):
    config = config or {}
    client = speech.SpeechClient()
    response = client.recognize(
        config=speech.RecognitionConfig(
            language_code=payload["language_code"],
            enable_speaker_diarization=True,
            diarization_speaker_count=payload.get("speaker_count", 2),
        ),
        audio=speech.RecognitionAudio(uri=payload["audio_uri"]),
    )
    segments = []
    for result in response.results:
        alt = result.alternatives[0]
        segments.append({"transcript": alt.transcript, "speaker_tag": getattr(alt, "speaker_tag", None)})
    return {"status": "COMPLETED", "segments": segments}
