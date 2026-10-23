import boto3

# Initialize the Amazon Transcribe client
def initialize_transcribe_client():
    transcribe_client = boto3.client('transcribe', region_name='us-west-2')
    return transcribe_client

# Configure the streaming settings
def configure_streaming_settings(language_code='en-US'):
    streaming_settings = {
        'LanguageCode': language_code,
        'MediaSampleRateHertz': 16000,
        'EnablePartialResultsStabilization': True,
        'PartialResultsStability': 'medium'
    }
    return streaming_settings
