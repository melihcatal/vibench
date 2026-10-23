import boto3

def synthesize_ssml(ssml_text, voice_id, output_format='mp3'):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        VoiceId=voice_id,
        OutputFormat=output_format,
        Text=ssml_text,
        TextType='ssml'
    )
    if 'AudioStream' in response:
        with open('output.mp3', 'wb') as file:
            file.write(response['AudioStream'].read())
        return 'output.mp3'
    else:
        raise Exception('AudioStream not found in response')

# Example usage:
# synthesize_ssml("<speak>Hello, world!</speak>", "Joanna")