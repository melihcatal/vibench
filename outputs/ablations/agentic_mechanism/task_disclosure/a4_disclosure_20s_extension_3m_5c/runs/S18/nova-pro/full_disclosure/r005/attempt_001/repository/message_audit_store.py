import boto3

dynamodb = boto3.resource('dynamodb')

TABLE_NAME = 'MessageAuditStore'


def create_table():
    table = dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {
                'AttributeName': 'message_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'message_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    table.meta.client.get_waiter('table_exists').wait(TableName=TABLE_NAME)
    print(f'Table {TABLE_NAME} created.')


def store_message(message_id, message_data):
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(Item={
        'message_id': message_id,
        'message_data': message_data
    })
    print(f'Message {message_id} stored.')


if __name__ == '__main__':
    create_table()
    store_message('1', 'This is a test message.')