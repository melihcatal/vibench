import boto3

def synthesize_speech(text, output_format, voice_id):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat=output_format,
        VoiceId=voice_id
    )
    return response

def save_speech(response, file_name):
    if 'AudioStream' in response:
        with open(file_name, 'wb') as file:
            file.write(response['AudioStream'].read())
    else:
        raise ValueError('Invalid response from Polly')

def normalize_text(text):
    return text.strip().replace('\n', ' ').replace('\t', ' ')
