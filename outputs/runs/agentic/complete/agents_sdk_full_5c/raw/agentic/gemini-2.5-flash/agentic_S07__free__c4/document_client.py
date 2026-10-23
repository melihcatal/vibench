import os

class DocumentClientConfig:
    """Configuration holder for document processing clients."""
    def __init__(self,
                 project_id: str = os.environ.get("GCP_PROJECT_ID", ""),
                 location: str = "us"):
        self.project_id = project_id
        self.location = location

    def get_project_id(self) -> str:
        if not self.project_id:
            raise ValueError("GCP_PROJECT_ID is not set in environment or config.")
        return self.project_id

    def get_location(self) -> str:
        return self.location

def get_document_ai_processor_path(config: DocumentClientConfig, processor_id: str) -> str:
    """Constructs the full resource name for a Document AI processor."""
    # This helper would typically use a Document AI client to format, but for a local helper,
    # we can construct it manually if the client isn't directly exposed here.
    # Using a placeholder for now as the Document AI client is instantiated within each extraction file.
    # In a real scenario, you might pass the client itself from here.
    return f"projects/{config.get_project_id()}/locations/{config.get_location()}/processors/{processor_id}"


if __name__ == '__main__':
    _config = DocumentClientConfig(project_id="my-test-project", location="eu")
    print(f"Client Config - Project ID: {_config.get_project_id()}, Location: {_config.get_location()}")
    _processor_path = get_document_ai_processor_path(_config, "my-processor-123")
    print(f"Sample Document AI Processor Path: {_processor_path}")
