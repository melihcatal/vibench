from boto3 import client

# Initialize DynamoDB client
ddb = client('dynamodb')


def put_item(table_name, item):
    return ddb.put_item(
        TableName=table_name,
        Item=item
    )


def get_item(table_name, key):
    return ddb.get_item(
        TableName=table_name,
        Key=key
    )


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
