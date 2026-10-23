# document_client.py
# Helper utilities for OCR and layout extraction services

from abc import ABC, abstractmethod


class TextExtractionClient(ABC):
    @abstractmethod
def extract(self, document_bytes: bytes) -> str:
        """Extract plain text from a document image and return as a string."""
        pass


class LayoutExtractionClient(ABC):
    @abstractmethod
def extract(self, document_bytes: bytes) -> list:
        """Extract blocks, lines, tables, or layout elements from a document and return a normalized structure."""
        pass


class KeyValueExtractionClient(ABC):
    @abstractmethod
def extract(self, document_bytes: bytes) -> dict:
        """Extract key-value pairs from a form-like document and return as a dict."""
        pass


class TableExtractionClient(ABC):
    @abstractmethod
def extract(self, image_bytes: bytes) -> list:
        """Extract table cells and row information from a document image."""
        pass

# Example base usage (uncomment in service files if needed)
# client = TextExtractionClient()  # would be one of the specific implementations
