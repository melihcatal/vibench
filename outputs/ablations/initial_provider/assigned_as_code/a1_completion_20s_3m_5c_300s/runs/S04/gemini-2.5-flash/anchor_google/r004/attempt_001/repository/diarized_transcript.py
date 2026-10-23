from google.cloud import speech
from speech_client import get_speech_client
from speech_models import TranscriptionResult

def diarized_transcript(audio_uri, language_code):
    client = get_speech_client()
    config = speech.RecognitionConfig(
        language_code=language_code,
        enable_speaker_diarization=True,
        diarization_speaker_count=2, # Example: assuming 2 speakers
    )
    audio = speech.RecognitionAudio(uri=audio_uri)

    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=9000)

    speaker_tags = []
    full_transcript = []

    for result in response.results:
        # The first alternative is the most likely one for a given speech segment.
        alternative = result.alternatives[0]
        full_transcript.append(alternative.transcript)

        for word_info in alternative.words:
            speaker_tags.append({
                "word": word_info.word,
                "start_time": word_info.start_time.seconds + word_info.start_time.nanos * 1e-9,
                "end_time": word_info.end_time.seconds + word_info.end_time.nanos * 1e-9,
                "speaker_tag": word_info.speaker_tag,
            })

    return TranscriptionResult(
        transcript=" ".join(full_transcript),
        speaker_diarization=speaker_tags,
    )
