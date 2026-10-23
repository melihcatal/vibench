import speech_client
import speech_models
import wave
import audioop


def stream_microphone():
    chunk_size = 1024
    wf = wave.open("sample.wav", "rb")
    stream = speech_client.transcribe_client.start_stream_transcription(
        LanguageCode="en-US", MediaSampleRateHertz=16000, MediaEncoding="pcm"
    )
    while True:
        data = wf.readframes(chunk_size)
        if len(data) == 0:
            break
        speech_client.transcribe_client.send_audio_event(AudioChunk=data)
    speech_client.transcribe_client.end_stream_transcription()
