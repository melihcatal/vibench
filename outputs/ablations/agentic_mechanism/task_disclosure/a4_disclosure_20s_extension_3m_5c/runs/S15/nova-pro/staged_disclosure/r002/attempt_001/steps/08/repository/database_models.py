from boto3 import client

dynamodb = client('dynamodb')

def create_request(table_name, item):
    return {
        'TableName': table_name,
        'Item': item
    }

def create_response(response):
    return response.get('Item', None)

def normalize_item(item):
    normalized_item = {}
    for key, value in item.items():
        if 'S' in value:
            normalized_item[key] = value['S']
        elif 'N' in value:
            normalized_item[key] = int(value['N'])
        elif 'BOOL' in value:
            normalized_item[key] = value['BOOL']
    return normalized_item