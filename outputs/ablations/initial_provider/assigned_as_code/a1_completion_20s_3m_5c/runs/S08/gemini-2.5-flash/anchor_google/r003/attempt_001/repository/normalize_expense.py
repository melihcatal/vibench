import boto3
import json

def normalize_expense(extracted_data, config=None):
    config = config or {}
    client = boto3.client('glue', region_name=config.get('aws_region', 'us-east-1'))
    
    # In a real scenario, you would fetch the schema from Glue Schema Registry
    # For this example, we'll use a hardcoded schema for demonstration
    schema_name = config.get('schema_name', 'expense_schema')
    registry_name = config.get('registry_name', 'default-registry')

    # Example: Fetching schema from Glue Schema Registry (conceptual)
    # response = client.get_schema_version(
    #     SchemaId={'SchemaName': schema_name, 'RegistryName': {'RegistryName': registry_name}},
    #     VersionNumber=1
    # )
    # schema_definition = json.loads(response['SchemaDefinition'])

    # Hardcoded schema for demonstration purposes
    schema_definition = {
        "type": "object",
        "properties": {
            "transaction_id": {"type": "string"},
            "type": {"type": "string", "enum": ["invoice", "receipt"]},
            "vendor_name": {"type": "string"},
            "transaction_date": {"type": "string", "format": "date"},
            "total_amount": {"type": "number"},
            "currency": {"type": "string"},
            "line_items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "quantity": {"type": "number"},
                        "unit_price": {"type": "number"},
                        "amount": {"type": "number"}
                    },
                    "required": ["description", "amount"]
                }
            }
        },
        "required": ["type", "vendor_name", "transaction_date", "total_amount"]
    }

    normalized_record = {
        "transaction_id": extracted_data.get("transaction_id"),
        "type": extracted_data.get("document_type"),
        "vendor_name": extracted_data.get("vendor"),
        "transaction_date": extracted_data.get("date"),
        "total_amount": float(extracted_data["total"]) if extracted_data.get("total") else None,
        "currency": extracted_data.get("currency", "USD"),
        "line_items": extracted_data.get("line_items", [])
    }
    
    # In a real scenario, you would validate against the schema_definition
    # using a library like jsonschema, and then potentially register or store the data.
    # For now, we'll just return the normalized record.
    return normalized_record