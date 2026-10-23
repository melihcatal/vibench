import boto3
import json
import wave

transcribe = boto3.client('transcribe')

def stream_microphone():
    audio_file = 'microphone_audio.wav'
    with wave.open(audio_file, 'rb') as f:
        audio_data = f.readframes(f.getnframes())
        audio_stream = {'AudioEvent': {'AudioChunk': audio_data}}
        response = transcribe.start_stream_transcription(
            LanguageCode='en-US',
            MediaEncoding='pcm',
            MediaSampleRate=f.getframerate(),
            AudioStream=audio_stream
        )
        for transcript in response['Transcripts']:
            yield transcript['Transcript']

if __name__ == '__main__':
    for transcript in stream_microphone():
        print(transcript)