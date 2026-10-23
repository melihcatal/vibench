class DatabaseModels:
    """Helper classes for request, response, and normalization with MongoDB Atlas.
    Provides structures and utilities to transform between external payloads and MongoDB documents.
    """

    class DocumentRequest:
        def __init__(self, identifier: str, data: dict):
            self.identifier = identifier
            self.data = data

    class DocumentResponse:
        def __init__(self, identifier: str, content: dict):
            self.identifier = identifier
            self.content = content

    @staticmethod
    def normalize_request(req: "DocumentRequest") -> dict:
        """Convert request DTO to MongoDB document representation."""
        return {"_id": req.identifier, **req.data}

    @staticmethod
    def normalize_response(doc: dict) -> "DocumentResponse":
        """Convert MongoDB document to response DTO."""
        identifier = doc.pop("_id")
        return DatabaseModels.DocumentResponse(identifier=identifier, content=doc)
