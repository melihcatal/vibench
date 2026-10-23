
class CreateDocumentRequest:
    def __init__(self, collection_name: str, document_data: dict):
        self.collection_name = collection_name
        self.document_data = document_data

class CreateDocumentResponse:
    def __init__(self, document_id: str, success: bool, message: str = ""):
        self.document_id = document_id
        self.success = success
        self.message = message

class GetDocumentRequest:
    def __init__(self, collection_name: str, document_id: str):
        self.collection_name = collection_name
        self.document_id = document_id

class GetDocumentResponse:
    def __init__(self, document_data: dict, success: bool, message: str = ""):
        self.document_data = document_data
        self.success = success
        self.message = message

def normalize_document_data(data: dict) -> dict:
    """
    Normalizes document data by ensuring all keys are strings and handling common data types.
    This is a placeholder for actual normalization logic.
    """
    normalized_data = {}
    for key, value in data.items():
        normalized_data[str(key)] = value
    return normalized_data
