from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

# Define models for Azure AI Content Safety request and response normalization

class CategoryAnalysisResult(BaseModel):
    category: str
    severity: int = Field(..., ge=0, le=7) # Azure Content Safety severity is 0-7

class BlocklistMatchResult(BaseModel):
    blocklist_name: str
    text: str
    offset: int
    length: int

class ModerationResponse(BaseModel):
    text: str
    categories_analysis: List[CategoryAnalysisResult]
    blocklist_matches: Optional[List[BlocklistMatchResult]] = None

class NormalizedModerationResult(BaseModel):
    original_text: str
    moderation_results: List[Dict[str, Any]] # To hold category and severity, or blocklist matches
    
    def from_azure_content_safety_response(self, text: str, response: Any):
        """
        Normalizes an Azure AI Content Safety analyze_text response.
        `response` is expected to be an object from azure.ai.contentsafety.models.AnalyzeTextResult
        """
        self.original_text = text
        self.moderation_results = []

        if response.categories_analysis:
            for category_result in response.categories_analysis:
                self.moderation_results.append({
                    "type": "category_analysis",
                    "category": category_result.category.value,
                    "severity": category_result.severity
                })
        
        if response.blocklist_matches:
            for match in response.blocklist_matches:
                self.moderation_results.append({
                    "type": "blocklist_match",
                    "blocklist_name": match.blocklist_name,
                    "matched_text": match.text,
                    "offset": match.offset,
                    "length": match.length
                })
        return self

if __name__ == '__main__':
    # Example usage
    # This example assumes you have an Azure Content Safety response object.
    # For demonstration, we'll create a dummy one.
    class DummyCategoryResult:
        def __init__(self, category_val, severity_val):
            self.category = type('Category', (object,), {'value': category_val})()
            self.severity = severity_val

    class DummyBlocklistMatch:
        def __init__(self, name, text, offset, length):
            self.blocklist_name = name
            self.text = text
            self.offset = offset
            self.length = length

    class DummyAnalyzeTextResult:
        def __init__(self, categories_analysis, blocklist_matches=None):
            self.categories_analysis = categories_analysis
            self.blocklist_matches = blocklist_matches

    dummy_azure_response = DummyAnalyzeTextResult(
        categories_analysis=[
            DummyCategoryResult("Hate", 4),
            DummyCategoryResult("Violence", 1)
        ],
        blocklist_matches=[
            DummyBlocklistMatch("myblocklist", "badword", 15, 7)
        ]
    )

    original_text_example = "This text contains a badword and some hate."
    normalized_result = NormalizedModerationResult().from_azure_content_safety_response(
        original_text_example, dummy_azure_response
    )
    print(normalized_result.model_dump_json(indent=2))
