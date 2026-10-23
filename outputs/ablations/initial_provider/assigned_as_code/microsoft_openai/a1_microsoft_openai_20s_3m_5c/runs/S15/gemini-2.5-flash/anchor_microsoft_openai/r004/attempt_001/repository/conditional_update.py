from database_client import get_cosmos_client
from database_models import Document

def conditional_update(document_id: str, new_data: dict, etag: str):
    container = get_cosmos_client()
    try:
        # Read the item to get its current state and etag
        current_item = container.read_item(item=document_id, partition_key=document_id)
        
        if current_item['_etag'] != etag:
            raise ValueError("ETag mismatch. Document has been modified by another process.")

        # Merge new data with existing data, preserving 'id' and '_etag' for the update operation
        updated_item = {**current_item, **new_data, 'id': document_id}

        # Replace the item conditionally using the etag
        response = container.replace_item(item=document_id, body=updated_item, 
                                          options={'access_condition': {'type': 'IfMatch', 'condition': etag}})
        return Document.from_dict(response)
    except Exception as e:
        print(f"Error performing conditional update: {e}")
        return None
