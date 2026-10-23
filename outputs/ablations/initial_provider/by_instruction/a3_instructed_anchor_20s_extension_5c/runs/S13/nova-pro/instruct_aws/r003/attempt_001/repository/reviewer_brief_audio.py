import boto3

def generate_spoken_briefs(briefs):
    polly = boto3.client('polly')
    audio_briefs = []
    for brief in briefs:
        response = polly.synthesize_speech(Text=brief, OutputFormat='mp3', VoiceId='Joanna')
        audio_briefs.append(response['AudioStream'].read())
    return audio_briefs
