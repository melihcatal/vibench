import os

class DocumentClientConfig:
    def __init__(self):
        self.api_key = os.environ.get("DOCUMENT_EXTRACTION_API_KEY", "default_api_key")
        self.endpoint = os.environ.get("DOCUMENT_EXTRACTION_ENDPOINT", "https://api.example.com/document-extraction")
        self.timeout = int(os.environ.get("DOCUMENT_EXTRACTION_TIMEOUT", 30))

class DocumentClient:
    def __init__(self, config: DocumentClientConfig = None):
        self.config = config if config else DocumentClientConfig()

    def _prepare_request_headers(self):
        return {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def _log_request(self, method, url, headers, payload):
        pass

    def _log_response(self, status_code, response_data):
        pass
