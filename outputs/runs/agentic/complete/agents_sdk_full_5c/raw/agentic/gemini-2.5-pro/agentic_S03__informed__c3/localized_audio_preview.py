import boto3
from botocore.exceptions import BotoCoreError, ClientError

def generate_audio_preview(text: str, output_path: str, voice_id: str = "Joanna") -> str:
    """
    Generates a spoken audio preview of translated copy using Amazon Polly.

    Args:
        text: The text to synthesize.
        output_path: The file path to save the generated MP3 audio.
        voice_id: The Amazon Polly voice to use for synthesis.

    Returns:
        The path to the output file if successful.
    
    Raises:
        ValueError: If the text is empty.
        IOError: If the audio file cannot be written.
        Exception: For AWS-related errors.
    """
    if not text:
        raise ValueError("Input text cannot be empty.")

    try:
        # Assumes AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) and region
        # are configured in the environment.
        polly_client = boto3.client('polly')

        response = polly_client.synthesize_speech(
            VoiceId=voice_id,
            OutputFormat='mp3',
            Text=text,
            Engine='neural'
        )

        with open(output_path, 'wb') as f:
            f.write(response['AudioStream'].read())
        
        return output_path

    except (BotoCoreError, ClientError) as error:
        raise Exception(f"Amazon Polly API error: {error}") from error
    except IOError as e:
        raise IOError(f"Could not write audio file to {output_path}: {e}") from e
