import boto3

def generate_audio_preview(text, language_code):
    polly = boto3.client('polly')
    result = polly.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId='Joanna', LanguageCode=language_code)
    return result['AudioStream'].read()