import boto3

def generate_localized_audio_preview(text, target_lang):
    client = boto3.client('polly')
    result = client.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId='Joanna', LanguageCode=target_lang)
    return result['AudioStream'].read()