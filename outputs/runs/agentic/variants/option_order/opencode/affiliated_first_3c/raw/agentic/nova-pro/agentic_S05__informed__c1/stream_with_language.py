import speech_client


def stream_with_language():
    speech_client.transcribe_client.start_stream_transcription(
        LanguageCode="en-US",
        MediaSampleRateHertz=16000,
        MediaEncoding="pcm",
        EnablePunctuation=True,
        EnableSpeakerDiarization=True,
    )
