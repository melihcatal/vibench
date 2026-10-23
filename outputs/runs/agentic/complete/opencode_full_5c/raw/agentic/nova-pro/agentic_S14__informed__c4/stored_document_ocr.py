from google.cloud import documentai


def stored_document_ocr(project_id, location, processor_id, gcs_uri):
    client = documentai.DocumentProcessorServiceClient()
    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    raw_document = {"gcs_uri": gcs_uri}
    document = {"raw_document": raw_document}
    response = client.process_document(name=name, document=document)

    for entity in response.entities:
        print(
            f"{entity.type_} : {entity.mention_text} (confidence: {entity.confidence})"
        )

    return response
