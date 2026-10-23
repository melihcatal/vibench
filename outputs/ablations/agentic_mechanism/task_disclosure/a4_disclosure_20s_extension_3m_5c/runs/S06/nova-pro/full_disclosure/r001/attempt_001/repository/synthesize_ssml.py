import boto3

def synthesize_ssml(ssml_text, voice_id, output_format='mp3'):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        Text=ssml_text,
        TextType='ssml',
        VoiceId=voice_id,
        OutputFormat=output_format
    )
    with open('output.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())
    return 'output.mp3'