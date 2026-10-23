import boto3
import json
import os

class MessageAuditStore:
    def __init__(self, bucket_name: str, region_name: str = None):
        """
        Initializes the MessageAuditStore with an S3 bucket.
        """
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3', region_name=region_name)

    def store_message_record(self, record_id: str, record_data: dict):
        """
        Persists a processed message record to S3.

        Args:
            record_id: A unique identifier for the message record.
            record_data: The dictionary containing the message record data.
        """
        try:
            # Convert dictionary to a JSON string
            json_data = json.dumps(record_data)
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=record_id,
                Body=json_data,
                ContentType='application/json'
            )
            return True
        except Exception as e:
            print(f"Error storing message record {record_id}: {e}")
            return False

    def get_message_record(self, record_id: str) -> dict | None:
        """
        Retrieves a processed message record from S3.

        Args:
            record_id: The unique identifier for the message record.

        Returns:
            The message record data as a dictionary, or None if not found or an error occurs.
        """
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=record_id)
            # Read the object content and parse it as JSON
            body = response['Body'].read().decode('utf-8')
            return json.loads(body)
        except self.s3_client.exceptions.NoSuchKey:
            print(f"Message record {record_id} not found.")
            return None
        except Exception as e:
            print(f"Error retrieving message record {record_id}: {e}")
            return None
