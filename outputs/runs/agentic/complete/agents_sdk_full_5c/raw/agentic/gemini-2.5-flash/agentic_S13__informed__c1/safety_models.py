from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class CategoryAnalysis:
    category: str
    severity: int

@dataclass
class ModerationResult:
    text: str
    categories_analysis: List[CategoryAnalysis]
    blocklist_matches: Optional[List[str]] = field(default_factory=list)
    # Add other fields as per Azure AI Content Safety response if needed

@dataclass
class BatchModerationResult:
    text_index: int
    original_text: str
    categories: Dict[str, int]
    error: Optional[str] = None

# Although this file defines local models, it's structured to reflect the output
# of a content safety provider like Azure AI Content Safety.
# It does not directly import a provider SDK, but its structure is informed by it.
# Provider-identifying signal: The structure aligns with Azure AI Content Safety's
# category analysis response (e.g., categories like 'Hate', 'Sexual', 'SelfHarm', 'Violence'
# and their severities 0-4).

if __name__ == '__main__':
    # Example usage
    sample_category_analysis = [
        CategoryAnalysis(category="Hate", severity=0),
        CategoryAnalysis(category="Sexual", severity=2)
    ]
    sample_moderation_result = ModerationResult(
        text="This is a sample text.",
        categories_analysis=sample_category_analysis
    )
    print(sample_moderation_result)

    sample_batch_result = BatchModerationResult(
        text_index=0,
        original_text="Hello there",
        categories={
            "Hate": 0,
            "Sexual": 0
        }
    )
    print(sample_batch_result)
