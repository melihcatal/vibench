from document_client import ddb_resource


def expense_record_store(payload, config=None):
    resource = ddb_resource(config)
    table = resource.Table((config or {}).get("table_name", "expense_records"))
    record = payload.get("record", payload)
    table.put_item(Item=record)
    return {"stored": True, "table_name": table.name}
