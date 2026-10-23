import boto3

transcribe_client = boto3.client('transcribe', region_name='us-west-2')

def handle_recognition_events(events):
    for event in events:
        if 'Transcript' in event:
            print(event['Transcript']['Transcript']})