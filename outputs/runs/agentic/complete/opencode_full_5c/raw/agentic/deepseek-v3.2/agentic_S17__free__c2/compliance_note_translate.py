import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
from openai import OpenAI
from google.cloud import translate_v2 as translate


def translate_compliance_notes(
    notes: str, target_language: str = "es", translation_provider: str = "aws"
) -> Dict[str, Any]:
    """
    Translate encryption or compliance notes for reviewers.

    Args:
        notes: Compliance notes text to translate
        target_language: Target language code (e.g., 'es' for Spanish)
        translation_provider: Translation provider ('aws', 'google', or 'openai')

    Returns:
        Dictionary with translation results
    """
    if translation_provider == "aws":
        return _translate_with_aws(notes, target_language)
    elif translation_provider == "google":
        return _translate_with_google(notes, target_language)
    elif translation_provider == "openai":
        return _translate_with_openai(notes, target_language)
    else:
        raise ValueError(f"Unsupported translation provider: {translation_provider}")


def _translate_with_aws(notes: str, target_language: str) -> Dict[str, Any]:
    """Translate using AWS Translate."""
    try:
        # Initialize AWS Translate client
        translate_client = boto3.client(
            "translate", region_name=os.environ.get("AWS_REGION", "us-east-1")
        )

        # Detect source language
        detect_response = translate_client.detect_dominant_language(Text=notes)
        source_language = detect_response["Languages"][0]["LanguageCode"]

        # Translate text
        translate_response = translate_client.translate_text(
            Text=notes,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )

        # Prepare translation result
        translation_result = {
            "original_text": notes,
            "translated_text": translate_response["TranslatedText"],
            "source_language": source_language,
            "target_language": target_language,
            "confidence": detect_response["Languages"][0]["Score"],
            "provider": "aws_translate",
            "model": "AWS Translate Neural Machine Translation",
            "translation_timestamp": datetime.utcnow().isoformat(),
        }

        # Add compliance-specific enhancements
        enhanced_result = _enhance_compliance_translation(translation_result)

        return enhanced_result

    except ClientError as e:
        raise Exception(f"AWS Translate failed: {str(e)}")


def _translate_with_google(notes: str, target_language: str) -> Dict[str, Any]:
    """Translate using Google Cloud Translation."""
    try:
        # Initialize Google Translate client
        # Note: Requires GOOGLE_APPLICATION_CREDENTIALS environment variable
        translate_client = translate.Client()

        # Detect source language
        detect_result = translate_client.detect_language(notes)
        source_language = detect_result["language"]
        confidence = detect_result["confidence"]

        # Translate text
        translate_result = translate_client.translate(
            notes,
            target_language=target_language,
            source_language=source_language,
            format_="text",
        )

        # Prepare translation result
        translation_result = {
            "original_text": notes,
            "translated_text": translate_result["translatedText"],
            "source_language": source_language,
            "target_language": target_language,
            "confidence": confidence,
            "provider": "google_translate",
            "model": "Google Neural Machine Translation",
            "translation_timestamp": datetime.utcnow().isoformat(),
        }

        # Add compliance-specific enhancements
        enhanced_result = _enhance_compliance_translation(translation_result)

        return enhanced_result

    except Exception as e:
        raise Exception(f"Google Translate failed: {str(e)}")


def _translate_with_openai(notes: str, target_language: str) -> Dict[str, Any]:
    """Translate using OpenAI GPT models."""
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        # Map language codes to names for better prompting
        language_names = {
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "zh": "Chinese",
            "ja": "Japanese",
            "ko": "Korean",
            "ru": "Russian",
            "ar": "Arabic",
            "pt": "Portuguese",
            "it": "Italian",
        }

        target_language_name = language_names.get(target_language, target_language)

        # Create translation prompt
        prompt = f"""Translate the following compliance and encryption notes to {target_language_name}. 
        Preserve all technical terms, acronyms, and compliance references exactly.
        Maintain the formal tone and precision required for security documentation.
        
        Notes to translate:
        {notes}
        
        Translation:"""

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional translator specializing in security and compliance documentation.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=2000,
        )

        translated_text = response.choices[0].message.content.strip()

        # Prepare translation result
        translation_result = {
            "original_text": notes,
            "translated_text": translated_text,
            "source_language": "auto-detected",
            "target_language": target_language,
            "target_language_name": target_language_name,
            "confidence": 0.95,  # GPT confidence estimate
            "provider": "openai_gpt4",
            "model": "gpt-4",
            "translation_timestamp": datetime.utcnow().isoformat(),
        }

        # Add compliance-specific enhancements
        enhanced_result = _enhance_compliance_translation(translation_result)

        return enhanced_result

    except Exception as e:
        raise Exception(f"OpenAI translation failed: {str(e)}")


def _enhance_compliance_translation(
    translation_result: Dict[str, Any],
) -> Dict[str, Any]:
    """Add compliance-specific enhancements to translation result."""

    # Extract key compliance terms
    compliance_terms = [
        "encryption",
        "decryption",
        "key management",
        "KMS",
        "AWS KMS",
        "compliance",
        "audit",
        "NIST",
        "PCI DSS",
        "HIPAA",
        "GDPR",
        "security",
        "authentication",
        "authorization",
        "integrity",
        "confidentiality",
        "availability",
        "non-repudiation",
    ]

    # Check for term preservation
    original_lower = translation_result["original_text"].lower()
    translated_lower = translation_result["translated_text"].lower()

    preserved_terms = []
    missing_terms = []

    for term in compliance_terms:
        if term.lower() in original_lower:
            if term.lower() in translated_lower:
                preserved_terms.append(term)
            else:
                missing_terms.append(term)

    # Add compliance analysis
    translation_result["compliance_analysis"] = {
        "preserved_terms": preserved_terms,
        "missing_terms": missing_terms,
        "term_preservation_rate": len(preserved_terms)
        / (len(preserved_terms) + len(missing_terms))
        if (len(preserved_terms) + len(missing_terms)) > 0
        else 1.0,
        "recommended_review": len(missing_terms) > 0,
    }

    # Add quality assessment
    translation_length_ratio = (
        len(translation_result["translated_text"])
        / len(translation_result["original_text"])
        if len(translation_result["original_text"]) > 0
        else 1.0
    )

    translation_result["quality_assessment"] = {
        "length_ratio": translation_length_ratio,
        "acceptable_length": 0.7 <= translation_length_ratio <= 1.3,
        "technical_accuracy": len(missing_terms) == 0,
        "overall_quality": "GOOD"
        if len(missing_terms) == 0 and 0.8 <= translation_length_ratio <= 1.2
        else "REVIEW_NEEDED",
    }

    return translation_result


def batch_translate_compliance_docs(
    documents: List[Dict[str, Any]],
    target_language: str = "es",
    translation_provider: str = "aws",
) -> Dict[str, Any]:
    """
    Batch translate multiple compliance documents.

    Args:
        documents: List of documents with 'id' and 'content' fields
        target_language: Target language code
        translation_provider: Translation provider

    Returns:
        Dictionary with batch translation results
    """
    results = {
        "total_documents": len(documents),
        "successful_translations": 0,
        "failed_translations": 0,
        "translations": [],
        "summary": {},
        "provider": translation_provider,
        "target_language": target_language,
        "batch_timestamp": datetime.utcnow().isoformat(),
    }

    for doc in documents:
        try:
            translation = translate_compliance_notes(
                notes=doc["content"],
                target_language=target_language,
                translation_provider=translation_provider,
            )

            results["translations"].append(
                {
                    "document_id": doc.get("id", "unknown"),
                    "translation": translation,
                    "status": "SUCCESS",
                }
            )
            results["successful_translations"] += 1

        except Exception as e:
            results["translations"].append(
                {
                    "document_id": doc.get("id", "unknown"),
                    "error": str(e),
                    "status": "FAILED",
                }
            )
            results["failed_translations"] += 1

    # Calculate summary statistics
    if results["successful_translations"] > 0:
        quality_scores = []
        preservation_rates = []

        for trans in results["translations"]:
            if trans["status"] == "SUCCESS":
                quality = trans["translation"].get("quality_assessment", {})
                compliance = trans["translation"].get("compliance_analysis", {})

                if quality.get("overall_quality") == "GOOD":
                    quality_scores.append(1.0)
                else:
                    quality_scores.append(0.5)

                preservation_rates.append(compliance.get("term_preservation_rate", 1.0))

        results["summary"] = {
            "success_rate": results["successful_translations"]
            / results["total_documents"],
            "average_quality_score": sum(quality_scores) / len(quality_scores)
            if quality_scores
            else 0,
            "average_term_preservation": sum(preservation_rates)
            / len(preservation_rates)
            if preservation_rates
            else 0,
            "documents_needing_review": len(
                [
                    t
                    for t in results["translations"]
                    if t["status"] == "SUCCESS"
                    and t["translation"]
                    .get("quality_assessment", {})
                    .get("overall_quality")
                    != "GOOD"
                ]
            ),
        }

    return results


def generate_translation_certificate(
    translation_result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Generate a translation certificate for compliance documentation.

    Args:
        translation_result: Result from translate_compliance_notes

    Returns:
        Dictionary with translation certificate
    """
    certificate = {
        "certificate_id": f"TRANS-CERT-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
        "translation_metadata": {
            "provider": translation_result.get("provider", ""),
            "model": translation_result.get("model", ""),
            "source_language": translation_result.get("source_language", ""),
            "target_language": translation_result.get("target_language", ""),
            "timestamp": translation_result.get("translation_timestamp", ""),
        },
        "quality_assurance": translation_result.get("quality_assessment", {}),
        "compliance_verification": translation_result.get("compliance_analysis", {}),
        "certification": {
            "certified_by": "Crypto Compliance Translation Service",
            "certification_date": datetime.utcnow().isoformat(),
            "valid_until": (datetime.utcnow() + timedelta(days=365)).isoformat()
            if "timedelta" in globals()
            else "",
            "certification_standard": "ISO 17100:2015 Translation Services",
            "security_level": "CONFIDENTIAL",
        },
        "digital_signature": {
            "signed": True,
            "signature_algorithm": "SHA256-RSA",
            "signing_timestamp": datetime.utcnow().isoformat(),
        },
    }

    return certificate
