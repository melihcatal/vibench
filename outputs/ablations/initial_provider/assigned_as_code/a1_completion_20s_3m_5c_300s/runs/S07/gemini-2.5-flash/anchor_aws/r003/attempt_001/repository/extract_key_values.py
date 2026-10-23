import boto3


def extract_key_values(payload, config=None):
    config = config or {}
    client = boto3.client("textract", region_name=config.get("region"))
    response = client.analyze_document(
        Document={"Bytes": payload["document_bytes"]}, Features=["FORMS"]
    )

    key_values = []
    key_map = {}
    value_map = {}
    block_map = {block["Id"]: block for block in response["Blocks"]}

    for block in response["Blocks"]:
        if block["BlockType"] == "KEY_VALUE_SET":
            if "KEY" in block["EntityTypes"]:
                key_map[block["Id"]] = block
            else:
                value_map[block["Id"]] = block

    for block_id, key_block in key_map.items():
        value_block = None
        for relationship in key_block.get("Relationships", []):
            if relationship["Type"] == "VALUE":
                for value_id in relationship["Ids"]:
                    if value_id in value_map:
                        value_block = value_map[value_id]
                        break
            if value_block:
                break

        key_text = ""
        for relationship in key_block.get("Relationships", []):
            if relationship["Type"] == "CHILD":
                for child_id in relationship["Ids"]:
                    if block_map[child_id]["BlockType"] == "WORD":
                        key_text += block_map[child_id]["Text"] + " "
        key_text = key_text.strip()

        value_text = ""
        if value_block:
            for relationship in value_block.get("Relationships", []):
                if relationship["Type"] == "CHILD":
                    for child_id in relationship["Ids"]:
                        if block_map[child_id]["BlockType"] == "WORD":
                            value_text += block_map[child_id]["Text"] + " "
        value_text = value_text.strip()

        if key_text or value_text:
            key_values.append({"key": key_text, "value": value_text})

    return {"key_values": key_values}
