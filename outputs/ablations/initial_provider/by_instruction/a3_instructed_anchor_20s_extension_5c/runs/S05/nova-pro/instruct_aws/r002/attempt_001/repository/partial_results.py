import boto3

def partial_results(response):
    client = boto3.client('transcribe', region_name='us-west-2')
    for result in response['TranscriptionResults']:
        if result['IsPartial']:
            print('Partial result:', result['Transcript'])
        else:
            print('Final result:', result['Transcript'])