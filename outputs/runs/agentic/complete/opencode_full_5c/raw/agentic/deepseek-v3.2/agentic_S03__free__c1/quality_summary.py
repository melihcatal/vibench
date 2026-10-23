import os
from typing import Dict, List, Any
from dataclasses import dataclass
from translation_client import get_translation_client


@dataclass
class QualityIssue:
    """Represents a translation quality issue."""

    issue_type: str
    description: str
    severity: str  # low, medium, high
    location: str
    suggestion: str


def quality_summary(
    source_text: str,
    translated_text: str,
    source_lang: str = "en",
    target_lang: str = "es",
) -> Dict[str, Any]:
    """Summarize translation quality issues using Google Cloud Natural Language API."""
    try:
        from google.cloud import language_v1

        client = language_v1.LanguageServiceClient()

        issues = []

        document = language_v1.Document(
            content=translated_text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
            language=target_lang,
        )

        try:
            sentiment_response = client.analyze_sentiment(
                request={"document": document}
            )
            sentiment_score = sentiment_response.document_sentiment.score

            if sentiment_score < -0.5:
                issues.append(
                    QualityIssue(
                        issue_type="negative_sentiment",
                        description="Translation has strongly negative sentiment",
                        severity="medium",
                        location="entire_text",
                        suggestion="Consider rephrasing to maintain neutral or positive tone",
                    )
                )
        except Exception:
            pass

        try:
            entities_response = client.analyze_entities(request={"document": document})
            entity_names = [entity.name for entity in entities_response.entities]

            source_doc = language_v1.Document(
                content=source_text,
                type_=language_v1.Document.Type.PLAIN_TEXT,
                language=source_lang,
            )
            source_entities = client.analyze_entities(request={"document": source_doc})
            source_entity_names = [entity.name for entity in source_entities.entities]

            missing_entities = set(source_entity_names) - set(entity_names)
            if missing_entities:
                issues.append(
                    QualityIssue(
                        issue_type="missing_entities",
                        description=f"Missing entities from source: {', '.join(list(missing_entities)[:3])}",
                        severity="high",
                        location="various",
                        suggestion="Ensure all named entities are properly translated or preserved",
                    )
                )
        except Exception:
            pass

        length_ratio = len(translated_text) / len(source_text) if source_text else 1.0
        if length_ratio < 0.5:
            issues.append(
                QualityIssue(
                    issue_type="translation_too_short",
                    description="Translation is significantly shorter than source",
                    severity="medium",
                    location="entire_text",
                    suggestion="Check for missing content or overly concise translation",
                )
            )
        elif length_ratio > 2.0:
            issues.append(
                QualityIssue(
                    issue_type="translation_too_long",
                    description="Translation is significantly longer than source",
                    severity="medium",
                    location="entire_text",
                    suggestion="Check for redundant phrasing or unnecessary additions",
                )
            )

        return {
            "issues": [issue.__dict__ for issue in issues],
            "issue_count": len(issues),
            "has_critical_issues": any(issue.severity == "high" for issue in issues),
            "quality_score": max(0, 100 - (len(issues) * 10)),
        }

    except Exception as e:
        print(f"Quality analysis error: {e}")
        return {
            "issues": [],
            "issue_count": 0,
            "has_critical_issues": False,
            "quality_score": 50,
            "error": str(e),
        }
