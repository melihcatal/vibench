from document_client import DocumentClient
from document_models import ExtractedKeyValues

def extract_key_values(payload, config=None):
    client = DocumentClient(region_name=config.get("region")).get_textract_client()
    response = client.analyze_document(
        Document={"Bytes": payload["document_bytes"]},
        FeatureTypes=["FORMS"]
    )

    key_values = {}
    for block in response["Blocks"]:
        if block["BlockType"] == "KEY_VALUE_SET" and "ENTITY_TYPES" in block and "KEY" in block["EntityTypes"]:
            key_block_id = None
            value_block_id = None
            for relationship in block.get("Relationships", []):
                if relationship["Type"] == "CHILD":
                    # Find the key and value blocks
                    for child_id in relationship["Ids"]:
                        child_block = next((b for b in response["Blocks"] if b["Id"] == child_id), None)
                        if child_block and child_block["BlockType"] == "WORD": # Simplified, usually points to SELECTION_ELEMENT or WORD
                            # In a more complete solution, we would iterate through connected blocks to get full key/value text
                            if 'KEY' in child_block.get('EntityTypes', []):
                                key_block_id = child_id
                            elif 'VALUE' in child_block.get('EntityTypes', []):
                                value_block_id = child_id
            
            # This is a very simplified way to get text, a real implementation would traverse the relationships more carefully.
            # For the purpose of this exercise, we'll just associate text from blocks. 
            # A full implementation would link KEY_VALUE_SET blocks to their actual KEY and VALUE child blocks and extract text.
            # Given the requirement to use the provider, this demonstrates the call.

    # A more complete implementation would iterate through KEY_VALUE_SET blocks and their relationships
    # to construct the key-value pairs correctly. For this example, we'll just return a placeholder.
    # The goal is to show the Textract API call for forms.

    # This part is illustrative of how one would process FORM data, but highly simplified.
    # A proper implementation would link detected KEY_VALUE_SET blocks to their respective key and value text.
    for block in response.get('Blocks', []):
        if block.get('BlockType') == 'KEY_VALUE_SET':
            if 'KEY' in block.get('EntityTypes', []):
                key_text = ""
                value_text = ""
                for relationship in block.get('Relationships', []):
                    if relationship['Type'] == 'CHILD':
                        for child_id in relationship['Ids']:
                            child_block = next((b for b in response['Blocks'] if b['Id'] == child_id), None)
                            if child_block and child_block['BlockType'] == 'WORD':
                                key_text += child_block['Text'] + " "
                    if relationship['Type'] == 'VALUE':
                        for value_id in relationship['Ids']:
                            value_block = next((b for b in response['Blocks'] if b['Id'] == value_id), None)
                            if value_block and value_block['BlockType'] == 'KEY_VALUE_SET' and 'VALUE' in value_block.get('EntityTypes', []):
                                for value_child_rel in value_block.get('Relationships', []):
                                    if value_child_rel['Type'] == 'CHILD':
                                        for val_child_id in value_child_rel['Ids']:
                                            val_word_block = next((b for b in response['Blocks'] if b['Id'] == val_child_id), None)
                                            if val_word_block and val_word_block['BlockType'] == 'WORD':
                                                value_text += val_word_block['Text'] + " "
                if key_text and value_text:
                    key_values[key_text.strip()] = value_text.strip()

    return ExtractedKeyValues(key_values=key_values)
