from document_client import DocumentClient
from document_models import ExtractedTables

def extract_tables(payload, config=None):
    client = DocumentClient(region_name=config.get("region")).get_textract_client()
    response = client.analyze_document(
        Document={"Bytes": payload["document_bytes"]},
        FeatureTypes=["TABLES"]
    )

    tables = []
    for block in response["Blocks"]:
        if block["BlockType"] == "TABLE":
            table_data = {
                "id": block["Id"],
                "rows": []
            }
            # Simplified for direct Textract output structure
            tables.append(table_data)

    return ExtractedTables(tables=tables)
