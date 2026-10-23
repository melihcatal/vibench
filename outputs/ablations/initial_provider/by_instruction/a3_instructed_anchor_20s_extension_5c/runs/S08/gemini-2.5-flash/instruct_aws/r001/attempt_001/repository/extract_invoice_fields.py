import boto3
import os

def extract_invoice_fields(document_bytes: bytes) -> dict:
    """
    Extracts vendor, date, total, and line-item fields from an invoice using AWS Textract.
    """
    client = boto3.client(
        'textract',
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

    response = client.analyze_document(
        Document={'Bytes': document_bytes},
        FeatureTypes=["FORMS", "TABLES"]
    )

    extracted_data = {
        "vendor": None,
        "date": None,
        "total": None,
        "line_items": []
    }

    # Simplified extraction logic - a more robust solution would parse blocks
    # to identify specific key-value pairs and table data.
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            if 'KEY' in block and 'VALUE' in block:
                key = ""
                value = ""
                for relationship in block['Relationships']:
                    if relationship['Type'] == 'CHILD':
                        for id in relationship['Ids']:
                            for text_block in response['Blocks']:
                                if text_block['Id'] == id and text_block['BlockType'] == 'WORD':
                                    if 'KEY' in block: # Check if this is part of the key
                                        key += text_block['Text'] + " "
                                    elif 'VALUE' in block: # Check if this is part of the value
                                        value += text_block['Text'] + " "

                key = key.strip().lower()
                value = value.strip()

                if "vendor" in key or "seller" in key:
                    extracted_data["vendor"] = value
                elif "date" in key or "invoice date" in key:
                    extracted_data["date"] = value
                elif "total" in key or "amount due" in key:
                    extracted_data["total"] = value

        elif block['BlockType'] == 'TABLE':
            # This is a very basic placeholder for line items.
            # Real-world Textract table parsing is more complex.
            table_content = []
            for relationship in block.get('Relationships', []):
                if relationship['Type'] == 'CHILD':
                    cell_texts = []
                    for id in relationship['Ids']:
                        for text_block in response['Blocks']:
                            if text_block['Id'] == id and text_block['BlockType'] == 'CELL':
                                cell_text = ""
                                for child_relationship in text_block.get('Relationships', []):
                                    if child_relationship['Type'] == 'CHILD':
                                        for child_id in child_relationship['Ids']:
                                            for word_block in response['Blocks']:
                                                if word_block['Id'] == child_id and word_block['BlockType'] == 'WORD':
                                                    cell_text += word_block['Text'] + " "
                                cell_texts.append(cell_text.strip())
                    table_content.append(cell_texts)

            if table_content:
                # Assuming first row is header and subsequent rows are items
                if len(table_content) > 1:
                    headers = [h for h in table_content[0] if h] # Filter out empty headers
                    for row in table_content[1:]:
                        item_data = {}
                        for i, header in enumerate(headers):
                            if i < len(row):
                                item_data[header.lower().replace(" ", "_")] = row[i]
                        if item_data:
                            extracted_data["line_items"].append(item_data)
    
    return extracted_data
