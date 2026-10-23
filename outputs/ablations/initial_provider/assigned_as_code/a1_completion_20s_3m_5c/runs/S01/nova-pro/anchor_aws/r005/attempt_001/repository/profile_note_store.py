import boto3


def store_profile_note(user_id, note, config=None):
    config = config or {}
    client = boto3.client('docdb', region_name=config.get('region'))
    response = client.put_item(
        TableName=config.get('table_name'),
        Item={'user_id': {'S': user_id}, 'note': {'S': note}}
    )
    return response
