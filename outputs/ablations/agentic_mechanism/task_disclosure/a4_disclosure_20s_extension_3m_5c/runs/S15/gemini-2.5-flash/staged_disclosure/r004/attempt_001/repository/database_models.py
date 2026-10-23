
class Document:
    def __init__(self, data: dict):
        self._data = data

    def to_dict(self):
        return self._data

    @staticmethod
    def from_dict(data: dict):
        return Document(data)

class RequestHelper:
    @staticmethod
    def create_document_request(collection_name: str, document_data: dict) -> dict:
        return {
            "collection": collection_name,
            "document": document_data
        }

    @staticmethod
    def get_document_request(collection_name: str, document_id: str) -> dict:
        return {
            "collection": collection_name,
            "document_id": document_id
        }

    @staticmethod
    def update_document_request(collection_name: str, document_id: str, updates: dict) -> dict:
        return {
            "collection": collection_name,
            "document_id": document_id,
            "updates": updates
        }

    @staticmethod
    def delete_document_request(collection_name: str, document_id: str) -> dict:
        return {
            "collection": collection_name,
            "document_id": document_id
        }

class ResponseHelper:
    @staticmethod
    def create_document_response(document_id: str, success: bool = True, message: str = "") -> dict:
        return {
            "document_id": document_id,
            "success": success,
            "message": message
        }

    @staticmethod
    def get_document_response(document_data: dict | None, success: bool = True, message: str = "") -> dict:
        return {
            "document": document_data,
            "success": success,
            "message": message
        }

    @staticmethod
    def update_document_response(document_id: str, success: bool = True, message: str = "") -> dict:
        return {
            "document_id": document_id,
            "success": success,
            "message": message
        }

    @staticmethod
    def delete_document_response(document_id: str, success: bool = True, message: str = "") -> dict:
        return {
            "document_id": document_id,
            "success": success,
            "message": message
        }

class NormalizationHelper:
    @staticmethod
    def normalize_document(document: dict) -> dict:
        # Example: Ensure all documents have an 'id' field, generating one if missing
        if "_id" not in document:
            # In a real scenario, this would generate a unique ID, e.g., using UUID
            document["_id"] = "generated_id_" + str(hash(frozenset(document.items())))
        return document

    @staticmethod
    def denormalize_document(document: dict) -> dict:
        # Example: Remove internal fields if necessary for external representation
        if "_internal_field" in document:
            del document["_internal_field"]
        return document
