import uuid
from messaging_client import get_dynamodb_resource
from messaging_models import ProcessedMessage


def store_audit_record(table_name: str, processed_message: ProcessedMessage) -> str:
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(table_name)
    audit_id = str(uuid.uuid4())
    processed_message.audit_id = audit_id

    item_data = processed_message.model_dump()
    # Convert nested Pydantic model to dict for DynamoDB
    item_data["original_payload"] = item_data["original_payload"]

    table.put_item(Item=item_data)

    return audit_id
