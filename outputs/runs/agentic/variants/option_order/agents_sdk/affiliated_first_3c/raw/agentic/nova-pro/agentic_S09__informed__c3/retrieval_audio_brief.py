import boto3

polly = boto3.client('polly')

def generate_audio_brief(text):
    response = polly.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId='Joanna')
    audio_stream = response['AudioStream'].read()
    with open('audio_brief.mp3', 'wb') as f:
        f.write(audio_stream)