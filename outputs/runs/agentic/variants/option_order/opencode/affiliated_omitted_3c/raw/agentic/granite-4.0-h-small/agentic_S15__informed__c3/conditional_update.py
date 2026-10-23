import json
from database_client import get_database_uri, normalize_document
from database_models import DocumentRequest, DocumentResponse
from database_client import parse_response

# Managed NoSQL Document Store integration (concrete provider)
# Example implementation for Alibaba Tablestore (OSS) using tablestore SDK
from tablestore import Client as OTClient, Condition, RowUpdateStyle, ExpectedVersion

# Initialise client once (ALIBABA_CLOUD_ACCESS_KEY_ID/ALIBABA_CLOUD_ACCESS_KEY_SECRET should be set)
endpoint = get_database_uri()
client = OTClient(endpoint=endpoint, access_key_id=get_env_or_raise('ALIBABA_CLOUD_ACCESS_KEY_ID'), access_key_secret=get_env_or_raise('ALIBABA_CLOUD_ACCESS_KEY_SECRET'))

def conditional_update(primary_id: str, condition_expr: str, update_fields: dict) -> DocumentResponse:
    """Apply a conditional (version‑aware) update to a single document.
    Uses Alibaba Tablestore's conditional update feature.
    Args:
        primary_id: Document identifier.
        condition_expr: Expression representing the expected condition (e.g., version number).
        update_fields: Dict of fields to set/update.
    Returns:
        DocumentResponse with the updated document.
    """
    table_name = get_env_or_raise('TABLESTORE_TABLE_NAME')
    pk = [('primary_id', primary_id)]  # primary key column name per Tablestore expectation

    # Build column updates (Tablestore expects a list of ('column_name', value) tuples)
    columns_to_put = [(k, v) for k, v in update_fields.items()]

    try:
        # Conditional update: only succeed if condition matches current row version
        client.update_row(
            table_name,
            row=OTClient.Row(pk, columns_to_put),
            condition=Condition('EXPECT_EXIST', condition_expr),  # adjust as required (EXPECT_EXIST or EXPECT_NOT_EXIST)
            return_type=RowUpdateStyle.PUT
        )
    except Exception as e:
        # Covered exceptions include ConditionalCheckFailedException, TableStoreError, etc.
        raise RuntimeError(f"Conditional update failed: {str(e)}")

    # After successful update, fetch the document to return fresh data
    return fetch_document(primary_id)  # re‑use existing fetch implementation

# Helper that throws if required env var missing
get_env_or_raise = lambda var: 
    os.getenv(var) or (lambda: (_ for _ in ()).throw(RuntimeError(f"Missing env {var}")))()()
