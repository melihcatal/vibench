import boto3
from botocore.exceptions import BotoCoreError, ClientError
from safety_models import AudioResult

def generate_reviewer_brief_audio(brief_text: str, output_file: str) -> AudioResult:
    """
    Generates a spoken audio brief for a moderation reviewer using Amazon Polly.

    :param brief_text: The text to convert to speech.
    :param output_file: The path to save the output MP3 file.
    :return: An AudioResult object.
    """
    try:
        # By default, Boto3 will look for credentials in environment variables
        # (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, etc.)
        polly_client = boto3.client('polly')

        response = polly_client.synthesize_speech(
            VoiceId='Joanna',
            OutputFormat='mp3',
            Text=brief_text,
            Engine='neural'
        )

        # The audio stream is in the response body
        with open(output_file, 'wb') as f:
            f.write(response['AudioStream'].read())
            
        return AudioResult(text=brief_text, audio_file_path=output_file)

    except (BotoCoreError, ClientError) as error:
        print(f"Error generating audio with Amazon Polly: {error}")
        # Return a failure state
        return AudioResult(text=brief_text, audio_file_path="")
