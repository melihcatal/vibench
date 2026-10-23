import os
import tempfile
from google.cloud import speech


def transcribe_audio(audio_bytes, language_code="en-US"):
    """Transcribe synthesized QA samples to verify spoken output using Google Cloud Speech-to-Text."""
    client = speech.SpeechClient()

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
        temp_file.write(audio_bytes)
        temp_file_path = temp_file.name

    try:
        with open(temp_file_path, "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            sample_rate_hertz=24000,
            language_code=language_code,
            enable_automatic_punctuation=True,
        )

        response = client.recognize(config=config, audio=audio)

        transcriptions = []
        for result in response.results:
            transcriptions.append(
                {
                    "transcript": result.alternatives[0].transcript,
                    "confidence": result.alternatives[0].confidence,
                    "is_final": result.is_final,
                }
            )

        return transcriptions
    finally:
        os.unlink(temp_file_path)


def transcribe_long_audio(gcs_uri, language_code="en-US"):
    """Transcribe long audio files from Google Cloud Storage."""
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=24000,
        language_code=language_code,
        enable_automatic_punctuation=True,
        enable_word_time_offsets=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    results = []
    for result in response.results:
        alternative = result.alternatives[0]
        results.append(
            {
                "transcript": alternative.transcript,
                "confidence": alternative.confidence,
                "word_count": len(alternative.words),
                "words": [
                    {
                        "word": word.word,
                        "start_time": word.start_time.total_seconds(),
                        "end_time": word.end_time.total_seconds(),
                    }
                    for word in alternative.words
                ]
                if alternative.words
                else [],
            }
        )

    return results


def verify_tts_output(original_text, audio_bytes, language_code="en-US"):
    """Verify TTS output by comparing original text with transcription."""
    transcriptions = transcribe_audio(audio_bytes, language_code)

    if not transcriptions:
        return {
            "original_text": original_text,
            "transcribed_text": "",
            "match_score": 0.0,
            "confidence": 0.0,
            "error": "No transcription obtained",
        }

    transcribed_text = " ".join([t["transcript"] for t in transcriptions])
    avg_confidence = sum(t["confidence"] for t in transcriptions) / len(transcriptions)

    original_lower = original_text.lower()
    transcribed_lower = transcribed_text.lower()

    match_score = 0.0
    if original_lower in transcribed_lower:
        match_score = 1.0
    elif transcribed_lower in original_lower:
        match_score = 0.8
    else:
        common_words = set(original_lower.split()) & set(transcribed_lower.split())
        if common_words:
            match_score = len(common_words) / max(
                len(original_lower.split()), len(transcribed_lower.split())
            )

    return {
        "original_text": original_text,
        "transcribed_text": transcribed_text,
        "match_score": match_score,
        "confidence": avg_confidence,
        "is_acceptable": match_score > 0.7 and avg_confidence > 0.8,
    }
