import boto3
from botocore.exceptions import BotoCoreError, ClientError

def generate_audio_briefing(text_brief: str, output_file: str = "briefing.mp3"):
    """
    Generates an audio file from a text brief using Amazon Polly.
    
    Args:
        text_brief: The text to convert to speech.
        output_file: The path to save the output MP3 file.
    """
    try:
        # Provider-specific SDK import and client: boto3.client('polly')
        polly_client = boto3.client('polly')
        
        response = polly_client.synthesize_speech(
            VoiceId='Joanna',
            OutputFormat='mp3',
            Text=text_brief,
            Engine='neural'
        )
        
        # Save the audio stream to a file
        with open(output_file, 'wb') as f:
            f.write(response['AudioStream'].read())
            
        print(f"Audio briefing saved to {output_file}")
        
    except (BotoCoreError, ClientError) as error:
        print(f"Error using Amazon Polly: {error}")
        raise
