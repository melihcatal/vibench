import boto3

def summarize_asset(asset_path):
    textract_client = boto3.client('textract')
    with open(asset_path, 'rb') as document:
        imageBytes = document.read()
    response = textract_client.detect_document_text(Document={'Bytes': imageBytes})
    text = ''
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text += item['Text'] + ' '
    return text

if __name__ == '__main__':
    asset_path = 'path/to/asset'
    summary = summarize_asset(asset_path)
    print(summary)