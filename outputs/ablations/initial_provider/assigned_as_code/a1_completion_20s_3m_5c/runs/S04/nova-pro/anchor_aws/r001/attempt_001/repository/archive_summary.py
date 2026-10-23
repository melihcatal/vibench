import boto3

from speech_client import get_textract_client


def archive_summary(transcript, config=None):
    config = config or {}
    client = get_textract_client(config)
    response = client.analyze_document(
        Document={'Text': transcript},
        FeatureTypes=['TABLES', 'FORMS']
    )
    blocks = response['Blocks']
    summary = "\n".join([block['Text'] for block in blocks if block['BlockType'] == 'LINE'])
    return summary