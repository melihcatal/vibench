# database_models.py
# Local helper: Request/response and normalization helpers for Managed NoSQL Document Store


class DocumentRequest:
    """Utility to build a DynamoDB Put/Update request payload.

    Attributes:
        id (str): Primary key of the document.
        data (dict): Full document content.
        condition (dict, optional): Optional condition expression for conditional updates.
    """

    def __init__(self, id: str, data: dict, condition: dict | None = None):
        self.id = id
        self.data = data
        self.condition = condition


class DocumentResponse:
    """Normalized response wrapper for fetched documents.

    Attributes:
        id (str): Document identifier.
        data (dict): Document fields as a dict.
        status (str): "created", "updated", or "not_found".
    """

    def __init__(self, id: str, data: dict | None = None, status: str = "not_found"):
        self.id = id
        self.data = data if data is not None else {}
        self.status = status


def normalize_response(api_response: dict) -> DocumentResponse:
    """Convert raw DynamoDB response into a standardized DocumentResponse.

    Args:
        api_response (dict): Raw response from boto3 client call.

    Returns:
        DocumentResponse: Normalized representation.
    """
    if (
        api_response.get("ResponseMetadata")
        and api_response["ResponseMetadata"]["HTTPStatusCode"] == 200
    ):
        return DocumentResponse(
            id=api_response.get("Item", {}).get("id"),
            data=api_response.get("Item", {}),
            status="updated",
        )
    return DocumentResponse(id=api_response.get("id"), data=None, status="not_found")
