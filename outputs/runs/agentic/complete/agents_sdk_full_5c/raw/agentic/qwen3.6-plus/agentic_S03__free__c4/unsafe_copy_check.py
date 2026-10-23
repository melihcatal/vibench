"""
Check localized copy for unsafe content.
Uses Google Cloud Natural Language API for content moderation and safety
analysis of translated text.
Provider: Google Cloud Natural Language API (language.googleapis.com)
Model: Google Cloud NLP Content Classification and Moderation
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field

from google.cloud import language_v1
from google.api_core import client_info as google_client_info

from translation_client import get_google_translate_config
from translation_models import TranslationResponse


@dataclass
class SafetyFlag:
    """Individual safety/content flag."""
    category: str
    likelihood: str
    confidence: float
    text_segment: str
    recommendation: str


@dataclass
class SafetyCheckResult:
    """Result of safety check on translated copy."""
    is_safe: bool
    flags: List[SafetyFlag] = field(default_factory=list)
    overall_risk_score: float = 0.0
    analyzed_segments: int = 0


UNSAFE_CATEGORIES = {
    "hate_speech": {
        "keywords": ["hate", "discrimination", "slur", "racist", "bigot"],
        "min_likelihood": "POSSIBLE",
    },
    "violence": {
        "keywords": ["violence", "kill", "harm", "attack", "weapon"],
        "min_likelihood": "POSSIBLE",
    },
    "adult_content": {
        "keywords": ["explicit", "sexual", "adult", "pornography"],
        "min_likelihood": "POSSIBLE",
    },
    "self_harm": {
        "keywords": ["suicide", "self-harm", "cutting", "overdose"],
        "min_likelihood": "POSSIBLE",
    },
    "harassment": {
        "keywords": ["harass", "bully", "threaten", "intimidate"],
        "min_likelihood": "POSSIBLE",
    },
    "misinformation": {
        "keywords": ["false", "hoax", "conspiracy", "fake"],
        "min_likelihood": "POSSIBLE",
    },
}


LIKELIHOOD_SCORES = {
    "VERY_LIKELY": 1.0,
    "LIKELY": 0.8,
    "POSSIBLE": 0.5,
    "UNLIKELY": 0.2,
    "VERY_UNLIKELY": 0.0,
}


def create_nlp_client() -> language_v1.LanguageServiceClient:
    """
    Create a Google Cloud Natural Language API client.
    
    Uses google.cloud.language_v1 to connect to language.googleapis.com
    for content analysis and safety checking.
    
    Returns:
        Configured google.cloud.language_v1.LanguageServiceClient instance.
    """
    config = get_google_translate_config()
    
    client_info = google_client_info.ClientInfo(
        user_agent="unsafe-copy-checker/1.0"
    )
    
    client = language_v1.LanguageServiceClient(
        client_info=client_info,
    )
    
    return client


def analyze_text_safety(
    text: str,
    client: language_v1.LanguageServiceClient,
) -> Dict[str, Any]:
    """
    Analyze text for unsafe content using Google Cloud NLP API.
    
    Uses the google.cloud.language_v1 client to perform content classification
    and sentiment analysis via language.googleapis.com.
    
    Args:
        text: Text to analyze for safety.
        client: Google Cloud NLP client.
    
    Returns:
        Dict with safety analysis results including categories and scores.
    """
    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT,
        language="en",
    )
    
    try:
        sentiment = client.analyze_sentiment(
            request={"document": document}
        )
        
        classification = client.classify_text(
            request={"document": document}
        )
        
        sentiment_score = sentiment.document_sentiment.score
        sentiment_magnitude = sentiment.document_sentiment.magnitude
        
        categories = []
        for category in classification.categories:
            categories.append({
                "name": category.name,
                "confidence": category.confidence,
            })
        
        return {
            "sentiment_score": sentiment_score,
            "sentiment_magnitude": sentiment_magnitude,
            "categories": categories,
            "text_length": len(text),
        }
    
    except Exception as e:
        return {
            "sentiment_score": 0.0,
            "sentiment_magnitude": 0.0,
            "categories": [],
            "text_length": len(text),
            "error": str(e),
        }


def check_unsafe_copy(
    translation_response: TranslationResponse,
    custom_keywords: Optional[List[str]] = None,
) -> SafetyCheckResult:
    """
    Check translated copy for unsafe content across all segments.
    
    Uses Google Cloud Natural Language API (language.googleapis.com) via
    google.cloud.language_v1 to perform content analysis and safety checking.
    
    Args:
        translation_response: TranslationResponse with translated text to check.
        custom_keywords: Optional list of additional keywords to flag.
    
    Returns:
        SafetyCheckResult with safety flags and overall risk assessment.
    """
    client = create_nlp_client()
    
    if not translation_response.success or not translation_response.results:
        return SafetyCheckResult(
            is_safe=True,
            flags=[],
            overall_risk_score=0.0,
            analyzed_segments=0,
        )
    
    all_flags = []
    risk_scores = []
    
    for result in translation_response.results:
        translated_text = result.translated_text
        
        if not translated_text or not translated_text.strip():
            continue
        
        nlp_analysis = analyze_text_safety(translated_text, client)
        
        sentiment_score = nlp_analysis.get("sentiment_score", 0.0)
        
        if sentiment_score < -0.5:
            flag = SafetyFlag(
                category="negative_sentiment",
                likelihood="LIKELY" if sentiment_score < -0.7 else "POSSIBLE",
                confidence=abs(sentiment_score),
                text_segment=translated_text,
                recommendation="Review for potentially harmful tone",
            )
            all_flags.append(flag)
            risk_scores.append(abs(sentiment_score))
        
        for category, config in UNSAFE_CATEGORIES.items():
            text_lower = translated_text.lower()
            for keyword in config["keywords"]:
                if keyword in text_lower:
                    flag = SafetyFlag(
                        category=category,
                        likelihood="POSSIBLE",
                        confidence=0.5,
                        text_segment=translated_text,
                        recommendation=f"Contains keyword matching {category} category. Manual review required.",
                    )
                    all_flags.append(flag)
                    risk_scores.append(0.5)
        
        for cat in nlp_analysis.get("categories", []):
            if any(unsafe in cat["name"].lower() for unsafe in ["violence", "adult", "hate"]):
                flag = SafetyFlag(
                    category=f"nlp_classification_{cat['name']}",
                    likelihood="LIKELY" if cat["confidence"] > 0.7 else "POSSIBLE",
                    confidence=cat["confidence"],
                    text_segment=translated_text,
                    recommendation=f"NLP classification flagged content as {cat['name']}",
                )
                all_flags.append(flag)
                risk_scores.append(cat["confidence"])
    
    if custom_keywords:
        for result in translation_response.results:
            text_lower = result.translated_text.lower()
            for keyword in custom_keywords:
                if keyword.lower() in text_lower:
                    flag = SafetyFlag(
                        category="custom_keyword_match",
                        likelihood="POSSIBLE",
                        confidence=0.6,
                        text_segment=result.translated_text,
                        recommendation=f"Contains custom flagged keyword: '{keyword}'",
                    )
                    all_flags.append(flag)
                    risk_scores.append(0.6)
    
    overall_risk = sum(risk_scores) / len(risk_scores) if risk_scores else 0.0
    is_safe = overall_risk < 0.3
    
    return SafetyCheckResult(
        is_safe=is_safe,
        flags=all_flags,
        overall_risk_score=round(overall_risk, 3),
        analyzed_segments=len(translation_response.results),
    )


def safety_result_to_dict(result: SafetyCheckResult) -> Dict[str, Any]:
    """Convert SafetyCheckResult to dictionary for serialization."""
    return {
        "is_safe": result.is_safe,
        "flags": [
            {
                "category": f.category,
                "likelihood": f.likelihood,
                "confidence": f.confidence,
                "text_segment": f.text_segment,
                "recommendation": f.recommendation,
            }
            for f in result.flags
        ],
        "overall_risk_score": result.overall_risk_score,
        "analyzed_segments": result.analyzed_segments,
    }


if __name__ == "__main__":
    from translate_text import translate_text
    
    response = translate_text("This is a safe message for testing", target_language="es")
    if response.success:
        result = check_unsafe_copy(response)
        print(f"Safe: {result.is_safe}")
        print(f"Risk Score: {result.overall_risk_score}")
        for flag in result.flags:
            print(f"  [{flag.category}] {flag.recommendation}")
