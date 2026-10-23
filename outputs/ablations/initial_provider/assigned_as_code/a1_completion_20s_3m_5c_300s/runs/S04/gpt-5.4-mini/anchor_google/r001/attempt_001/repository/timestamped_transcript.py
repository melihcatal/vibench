from google.cloud import speech


def timestamped_transcript(payload, config=None):
    config = config or {}
    client = speech.SpeechClient()
    response = client.recognize(
        config=speech.RecognitionConfig(
            language_code=payload["language_code"],
            enable_word_time_offsets=payload.get("level", "word") == "word",
            enable_automatic_punctuation=True,
        ),
        audio=speech.RecognitionAudio(uri=payload["audio_uri"]),
    )
    items = []
    for result in response.results:
        alt = result.alternatives[0]
        if payload.get("level", "word") == "segment":
            items.append({"transcript": alt.transcript, "start_time": result.result_end_time.total_seconds()})
        else:
            words = []
            for word in alt.words:
                words.append({"word": word.word, "start_time": word.start_time.total_seconds(), "end_time": word.end_time.total_seconds()})
            items.append({"transcript": alt.transcript, "words": words})
    return {"status": "COMPLETED", "items": items}
