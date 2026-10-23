from typing import List, Dict, Optional, Union
from pydantic import BaseModel


class CategoryAnalysis(BaseModel):
    category: str
    severity: int


class BlocklistMatch(BaseModel):
    blocklistName: str
    blocklistItemText: str
    blocklistItemId: str


class ModerationResponse(BaseModel):
    categories_analysis: List[CategoryAnalysis]
    blocklists: Optional[List[BlocklistMatch]] = None
    error: Optional[str] = None
    message: Optional[str] = None


class ModerationRequest(BaseModel):
    text: str
    categories: Optional[List[str]] = None
    output_type: str = "FourSeverityLevels"


def normalize_response(response: Dict) -> ModerationResponse:
    categories_analysis = []
    if response.get("categories_analysis"):
        for analysis in response["categories_analysis"]:
            categories_analysis.append(
                CategoryAnalysis(category=analysis.category, severity=analysis.severity)
            )

    blocklists = None
    if response.get("blocklists"):
        blocklists = []
        for match in response["blocklists"]:
            blocklists.append(
                BlocklistMatch(
                    blocklistName=match.blocklistName,
                    blocklistItemText=match.blocklistItemText,
                    blocklistItemId=match.blocklistItemId,
                )
            )

    return ModerationResponse(
        categories_analysis=categories_analysis,
        blocklists=blocklists,
        error=response.get("error"),
        message=response.get("message"),
    )
