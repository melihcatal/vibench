import dataclasses

@dataclasses.dataclass
class DocumentAIConfig:
    project_id: str
    location: str
    processor_id: str

@dataclasses.dataclass
class DocumentPayload:
    document_bytes: bytes
    mime_type: str
