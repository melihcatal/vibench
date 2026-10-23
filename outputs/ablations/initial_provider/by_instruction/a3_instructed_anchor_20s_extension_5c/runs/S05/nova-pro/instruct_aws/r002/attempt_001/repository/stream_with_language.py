import boto3

def stream_with_language():
    client = boto3.client('transcribe', region_name='us-west-2')
    response = client.start_stream_transcription(
        LanguageCode='en-US',
        MediaEncoding='pcm',
        MediaSampleRateHertz=16000,
        EnablePunctuation=True,
        EnableSpeakerIdentification=True
    )
    return response