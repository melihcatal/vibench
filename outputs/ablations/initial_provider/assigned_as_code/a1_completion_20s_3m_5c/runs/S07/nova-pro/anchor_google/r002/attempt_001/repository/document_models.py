from google.cloud.documentai_v1beta3.types import Document


def normalize_response(response):
    normalized_response = {
        "text": response.document.text,
        "pages": []
    }
    for page in response.document.pages:
        page_data = {
            "blocks": [],
            "tables": [],
            "key_value_pairs": []
        }
        for block in page.blocks:
            page_data["blocks"].append({
                "block_type": block.block_type,
                "text": block.text,
                "confidence": block.confidence,
                "bounding_box": block.bounding_box
            })
        for table in page.tables:
            table_data = {
                "header_rows": [],
                "body_rows": [],
                "footer_rows": []
            }
            for row in table.header_rows:
                table_data["header_rows"].append([cell.text for cell in row.cells])
            for row in table.body_rows:
                table_data["body_rows"].append([cell.text for cell in row.cells])
            for row in table.footer_rows:
                table_data["footer_rows"].append([cell.text for cell in row.cells])
            page_data["tables"].append(table_data)
        for key_value_pair in page.key_value_pairs:
            page_data["key_value_pairs"].append({
                "key": key_value_pair.key.text,
                "value": key_value_pair.value.text
            })
        normalized_response["pages"].append(page_data)
    return normalized_response