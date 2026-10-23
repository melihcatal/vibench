from typing import List, Optional
from pydantic import BaseModel, Field

# Pydantic models for type hinting and data validation.
# These structures are inspired by the Azure AI Content Safety SDK responses.

class ContentCategory(BaseModel):
    category: str
    severity: int

class BlocklistMatch(BaseModel):
    blocklist_name: str
    offset: int
    length: int

class ModerationResult(BaseModel):
    text: str
    categories: List[ContentCategory] = Field(default_factory=list)
    blocklist_matches: Optional[List[BlocklistMatch]] = Field(default_factory=list)
    passed: bool

class BatchModerationResult(BaseModel):
    results: List[ModerationResult]
