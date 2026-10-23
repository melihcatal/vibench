"""
script_safety.py - Check narration scripts for unsafe content using Google Cloud Natural Language API.

Uses the google-cloud-language SDK to analyze narration scripts for
toxicity, harmful content, and safety classifications before synthesis.
Provides content moderation and risk scoring for generated audio scripts.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple

from google.cloud import language_v1
from google.cloud.language_v1.types import (
    ClassificationCategory,
    ClassificationModel,
    Document,
    EncodingType,
)


class SafetyLevel(str, Enum):
    SAFE = "SAFE"
    REVIEW = "REVIEW"
    BLOCK = "BLOCK"


@dataclass
class SafetyCategory:
    """A single safety classification result."""

    name: str
    confidence: float


@dataclass
class SafetyAnalysis:
    """Complete safety analysis result for a narration script."""

    overall_level: SafetyLevel
    categories: List[SafetyCategory] = field(default_factory=list)
    flagged_terms: List[str] = field(default_factory=list)
    risk_score: float = 0.0
    details: Optional[str] = None


KNOWN_UNSAFE_CATEGORIES = {
    "/Adult",
    "/Violence",
    "/Hate",
    "/Sensitive_Subject",
    "/Law & Government/Crime",
    "/Society/Religion & Spirituality/Controversial",
}

SAFETY_THRESHOLD_REVIEW = 0.5
SAFETY_THRESHOLD_BLOCK = 0.8


class ScriptSafetyChecker:
    """
    Analyzes narration scripts for unsafe content using Google Cloud Natural Language API.

    Provider: Google Cloud Natural Language API via google-cloud-language SDK.
    API endpoint: language.googleapis.com
    """

    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize Google Cloud Natural Language client.

        Args:
            credentials_path: Path to Google service account JSON file.
        """
        if credentials_path:
            from google.oauth2 import service_account

            credentials = service_account.Credentials.from_service_account_file(credentials_path)
            self.client = language_v1.LanguageServiceClient(credentials=credentials)
        else:
            self.client = language_v1.LanguageServiceClient()

    def classify_content(self, text: str) -> List[ClassificationCategory]:
        """
        Classify narration script content using Google Cloud content classification.

        Args:
            text: Narration script text to classify.

        Returns:
            List of ClassificationCategory with names and confidence scores.
        """
        document = Document(
            content=text,
            type_=Document.Type.PLAIN_TEXT,
        )

        response = self.client.classify_text(
            document=document,
            classification_model=ClassificationModel.V2,
        )

        return response.categories

    def check_safety(
        self,
        text: str,
        custom_blocked_terms: Optional[List[str]] = None,
    ) -> SafetyAnalysis:
        """
        Perform comprehensive safety analysis on a narration script.

        Uses Google Cloud Natural Language content classification combined
        with term-based filtering to determine content safety level.

        Provider: Google Cloud Natural Language API via google-cloud-language SDK.
        API endpoint: language.googleapis.com

        Args:
            text: Narration script text to analyze.
            custom_blocked_terms: Optional list of additional terms to block.

        Returns:
            SafetyAnalysis with overall safety level, categories, and risk score.
        """
        if not text or not text.strip():
            return SafetyAnalysis(
                overall_level=SafetyLevel.SAFE,
                risk_score=0.0,
                details="Empty text",
            )

        categories = self.classify_content(text)

        safety_categories: List[SafetyCategory] = []
        max_confidence = 0.0
        flagged_categories: List[str] = []

        for cat in categories:
            safety_categories.append(
                SafetyCategory(name=cat.name, confidence=cat.confidence)
            )
            max_confidence = max(max_confidence, cat.confidence)

            if cat.name in KNOWN_UNSAFE_CATEGORIES and cat.confidence >= SAFETY_THRESHOLD_REVIEW:
                flagged_categories.append(cat.name)

        flagged_terms: List[str] = []
        all_blocked = list(custom_blocked_terms or [])
        text_lower = text.lower()
        for term in all_blocked:
            if term.lower() in text_lower:
                flagged_terms.append(term)

        risk_score = max_confidence
        if flagged_categories:
            risk_score = min(1.0, risk_score + 0.3)
        if flagged_terms:
            risk_score = min(1.0, risk_score + 0.4)

        if risk_score >= SAFETY_THRESHOLD_BLOCK or len(flagged_terms) > 0:
            overall = SafetyLevel.BLOCK
        elif risk_score >= SAFETY_THRESHOLD_REVIEW or len(flagged_categories) > 0:
            overall = SafetyLevel.REVIEW
        else:
            overall = SafetyLevel.SAFE

        details = None
        if flagged_categories:
            details = f"Flagged categories: {', '.join(flagged_categories)}"
        if flagged_terms:
            term_note = f"Flagged terms: {', '.join(flagged_terms)}"
            details = f"{details}. {term_note}" if details else term_note

        return SafetyAnalysis(
            overall_level=overall,
            categories=safety_categories,
            flagged_terms=flagged_terms,
            risk_score=round(risk_score, 3),
            details=details,
        )

    def analyze_entities_for_context(
        self, text: str
    ) -> List[Tuple[str, str, float]]:
        """
        Extract entities from the script to provide context for safety analysis.

        Args:
            text: Narration script text.

        Returns:
            List of (entity_name, entity_type, salience) tuples.
        """
        document = Document(
            content=text,
            type_=Document.Type.PLAIN_TEXT,
        )

        response = self.client.analyze_entities(
            document=document,
            encoding_type=EncodingType.UTF8,
        )

        return [
            (entity.name, entity.type_.name, entity.salience)
            for entity in response.entities
        ]


def check_script_safety(
    text: str,
    blocked_terms: Optional[List[str]] = None,
    credentials_path: Optional[str] = None,
) -> SafetyAnalysis:
    """
    Check a narration script for unsafe content before synthesis.

    Provider: Google Cloud Natural Language API via google-cloud-language SDK.
    API endpoint: language.googleapis.com

    Args:
        text: Narration script text to analyze.
        blocked_terms: Optional additional terms to block.
        credentials_path: Path to Google service account JSON.

    Returns:
        SafetyAnalysis with safety level and details.
    """
    checker = ScriptSafetyChecker(credentials_path=credentials_path)
    return checker.check_safety(text, custom_blocked_terms=blocked_terms)


def is_script_safe(
    text: str,
    blocked_terms: Optional[List[str]] = None,
    credentials_path: Optional[str] = None,
) -> Tuple[bool, SafetyAnalysis]:
    """
    Quick safety check returning a boolean verdict.

    Args:
        text: Narration script text.
        blocked_terms: Optional additional blocked terms.
        credentials_path: Path to Google service account JSON.

    Returns:
        Tuple of (is_safe, SafetyAnalysis).
    """
    analysis = check_script_safety(text, blocked_terms, credentials_path)
    is_safe = analysis.overall_level == SafetyLevel.SAFE
    return is_safe, analysis


if __name__ == "__main__":
    creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    checker = ScriptSafetyChecker(credentials_path=creds)

    safe_text = "Welcome to today's weather forecast. It will be sunny and warm."
    result = checker.check_safety(safe_text)
    print(f"Safe text: {result.overall_level.value} (risk: {result.risk_score})")

    result2 = checker.check_safety(
        "This content is inappropriate and contains harmful material.",
        blocked_terms=["harmful", "inappropriate"],
    )
    print(f"Flagged text: {result2.overall_level.value} (risk: {result2.risk_score})")
