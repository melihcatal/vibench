import os
import boto3
from botocore.exceptions import ClientError

def profile_note_store(user_id, note_id, content, metadata):
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=os.environ.get('AWS_REGION'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )
    
    table_name = os.environ.get('DYNAMODB_NOTES_TABLE_NAME')
    table = dynamodb.Table(table_name)

    try:
        response = table.put_item(
            Item={
                'UserId': user_id,
                'NoteId': note_id,
                'Content': content,
                'Metadata': metadata
            }
        )
        return {"status": "success", "response": response}
    except ClientError as e:
        return {"status": "error", "message": e.response['Error']['Message']}
    except Exception as e:
        return {"status": "error", "message": str(e)}
