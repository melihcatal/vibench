import os
from mindee import Client
from mindee.input import LocalInputSource
from document_models import OCRTextResponse


MINDEE_API_KEY = os.environ.get("MINDEE_API_KEY", "")


def extract_fields_from_document(ocr_response: OCRTextResponse) -> dict:
    if not ocr_response or not ocr_response.text:
        return {"fields": {}, "raw_result": None}

    api_key = MINDEE_API_KEY
    if not api_key:
        raise ValueError("MINDEE_API_KEY environment variable is not set")

    mindee_client = Client(api_key=api_key)

    doc_input = LocalInputSource(
        input_str=ocr_response.text.encode("utf-8"), filename="document.txt"
    )
    response = mindee_client.enqueue_and_parse(
        input_doc=doc_input,
        product="mindee/invoice",
    )

    fields = {}
    if response.document and response.document.inference:
        prediction = response.document.inference.prediction
        if hasattr(prediction, "fields") and prediction.fields:
            for field_name, field_value in prediction.fields.items():
                if hasattr(field_value, "value"):
                    fields[field_name] = {
                        "value": field_value.value,
                        "confidence": getattr(field_value, "confidence", None),
                    }
                else:
                    fields[field_name] = str(field_value)

    return {
        "fields": fields,
        "raw_result": response,
    }


def extract_fields_from_file(image_path: str) -> dict:
    api_key = MINDEE_API_KEY
    if not api_key:
        raise ValueError("MINDEE_API_KEY environment variable is not set")

    mindee_client = Client(api_key=api_key)

    with open(image_path, "rb") as f:
        file_bytes = f.read()

    doc_input = LocalInputSource(
        input_bytes=file_bytes, filename=os.path.basename(image_path)
    )
    response = mindee_client.enqueue_and_parse(
        input_doc=doc_input,
        product="mindee/invoice",
    )

    fields = {}
    if response.document and response.document.inference:
        prediction = response.document.inference.prediction
        if hasattr(prediction, "fields") and prediction.fields:
            for field_name, field_value in prediction.fields.items():
                if hasattr(field_value, "value"):
                    fields[field_name] = {
                        "value": field_value.value,
                        "confidence": getattr(field_value, "confidence", None),
                    }
                else:
                    fields[field_name] = str(field_value)

    return {
        "fields": fields,
        "raw_result": response,
    }
