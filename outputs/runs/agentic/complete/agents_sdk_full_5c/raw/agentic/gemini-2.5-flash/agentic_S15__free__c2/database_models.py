from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class Document(BaseModel):
    id: str = Field(..., description="Unique identifier for the document.")
    title: str = Field(..., description="Title of the document.")
    content: str = Field(..., description="Main content of the document.")
    category: Optional[str] = Field(None, description="Category of the document.")
    tags: Optional[list[str]] = Field(None, description="List of tags associated with the document.")
    version: int = Field(1, description="Version of the document, used for optimistic locking.")
    created_at: Optional[str] = Field(None, description="Timestamp when the document was created (ISO 8601 format).")
    updated_at: Optional[str] = Field(None, description="Timestamp when the document was last updated (ISO 8601 format).")

    def to_dynamodb_item(self) -> Dict[str, Any]:
        """
        Converts the Document model to a DynamoDB item format.
        """
        item = {}
        for field_name, value in self.dict(exclude_unset=True).items():
            if value is not None:
                if isinstance(value, str):
                    item[field_name] = {'S': value}
                elif isinstance(value, int):
                    item[field_name] = {'N': str(value)}
                elif isinstance(value, list) and all(isinstance(v, str) for v in value):
                    item[field_name] = {'SS': value}
                # Add other types as needed (e.g., bool, float, dict)
        return item

    @staticmethod
    def from_dynamodb_item(item: Dict[str, Any]):
        """
        Converts a DynamoDB item format back to a Document model.
        """
        parsed_item = {}
        for key, value_obj in item.items():
            if 'S' in value_obj: # String
                parsed_item[key] = value_obj['S']
            elif 'N' in value_obj: # Number
                # Attempt to convert to int, fallback to float if it has a decimal
                try:
                    parsed_item[key] = int(value_obj['N'])
                except ValueError:
                    parsed_item[key] = float(value_obj['N'])
            elif 'SS' in value_obj: # String Set
                parsed_item[key] = list(value_obj['SS'])
            # Add other types as needed (e.g., BOOL, M, L)
        return Document(**parsed_item)


if __name__ == '__main__':
    # Example usage
    doc_data = {
        "id": "doc456",
        "title": "Understanding Pydantic",
        "content": "Pydantic is a data validation and settings management library...",
        "category": "programming",
        "tags": ["python", "data-validation"],
        "version": 1,
        "created_at": "2023-10-27T10:00:00Z"
    }
    my_doc = Document(**doc_data)
    print("Pydantic Model:", my_doc)

    dynamodb_item = my_doc.to_dynamodb_item()
    print("DynamoDB Item Format:", dynamodb_item)

    retrieved_doc = Document.from_dynamodb_item(dynamodb_item)
    print("Reconstructed Pydantic Model:", retrieved_doc)
