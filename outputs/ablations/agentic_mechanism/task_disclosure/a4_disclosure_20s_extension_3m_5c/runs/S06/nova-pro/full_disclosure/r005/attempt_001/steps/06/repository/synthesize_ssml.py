import boto3

def synthesize_ssml(ssml_text, voice_id, output_format='mp3'):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        VoiceId=voice_id,
        OutputFormat=output_format,
        TextType='ssml',
        Text=ssml_text
    )
    if 'AudioStream' in response:
        with open('synthesized_speech.mp3', 'wb') as file:
            file.write(response['AudioStream'].read())
        return 'synthesized_speech.mp3'
    else:
        return 'Error synthesizing speech'