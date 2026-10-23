from google.cloud import documentai

from document_client import get_client, get_config, processor_path, raw_document


def extract_layout(payload, config=None):
    config = get_config(config)
    client = get_client(config["location"])
    name = processor_path(client, config["project_id"], config["location"], config["layout_processor_id"])
    response = client.process_document(request={"name": name, "raw_document": raw_document(payload)})
    document = response.document
    return {
        "blocks": [block.text_anchor.content if hasattr(block.text_anchor, "content") else "" for block in document.pages[0].blocks] if document.pages else [],
        "lines": [line.layout.text_anchor.content if hasattr(line.layout.text_anchor, "content") else "" for page in document.pages for line in page.lines],
        "tables": len(document.pages[0].tables) if document.pages else 0,
        "text": document.text,
    }
