import boto3

def generate_audio_preview(text, voice_id='Joanna', output_format='mp3'):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat=output_format,
        VoiceId=voice_id
    )
    if 'AudioStream' in response:
        with open('audio_preview.mp3', 'wb') as file:
            file.write(response['AudioStream'].read())
        print('Audio preview generated successfully.')
    else:
        print('Failed to generate audio preview.')

# Example usage:
# generate_audio_preview('Hello, this is a test audio preview.')