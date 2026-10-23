import os
import json
from typing import Dict, List, Any, Optional
import boto3
from botocore.exceptions import ClientError


def translate_compliance_notes(
    notes_text, target_language_code, source_language_code="auto"
):
    """
    Translate encryption or compliance notes for reviewers using AWS Translate.

    Args:
        notes_text: Text to translate
        target_language_code: Target language code (e.g., 'es', 'fr', 'de')
        source_language_code: Source language code or 'auto'

    Returns:
        dict with translation results
    """
    if isinstance(notes_text, str):
        notes_text = [notes_text]

    translate_client = boto3.client(
        "translate", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    translations = []

    try:
        for text in notes_text:
            if len(text) > 5000:
                chunks = [text[i : i + 5000] for i in range(0, len(text), 5000)]
                chunk_translations = []

                for chunk in chunks:
                    response = translate_client.translate_text(
                        Text=chunk,
                        SourceLanguageCode=source_language_code,
                        TargetLanguageCode=target_language_code,
                    )
                    chunk_translations.append(response.get("TranslatedText", ""))

                translated_text = " ".join(chunk_translations)
            else:
                response = translate_client.translate_text(
                    Text=text,
                    SourceLanguageCode=source_language_code,
                    TargetLanguageCode=target_language_code,
                )
                translated_text = response.get("TranslatedText", "")

            translations.append(
                {
                    "original": text[:500] + ("..." if len(text) > 500 else ""),
                    "translated": translated_text[:500]
                    + ("..." if len(translated_text) > 500 else ""),
                    "source_language": response.get(
                        "SourceLanguageCode", source_language_code
                    ),
                    "target_language": target_language_code,
                    "original_length": len(text),
                    "translated_length": len(translated_text),
                }
            )

        return {
            "translations": translations,
            "total_texts": len(notes_text),
            "source_language": source_language_code,
            "target_language": target_language_code,
            "provider": "aws_translate",
        }

    except ClientError as e:
        raise Exception(f"AWS Translate failed: {e}")


def translate_with_glossary(notes_text, target_language_code, glossary_name=None):
    """
    Translate compliance notes using a custom glossary for technical terms.

    Args:
        notes_text: Text to translate
        target_language_code: Target language code
        glossary_name: Optional custom glossary name

    Returns:
        dict with glossary-based translation results
    """
    translate_client = boto3.client(
        "translate", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    try:
        terminology_names = []
        if glossary_name:
            try:
                translate_client.describe_terminology(Name=glossary_name)
                terminology_names = [glossary_name]
            except ClientError:
                print(
                    f"Warning: Glossary '{glossary_name}' not found, proceeding without it"
                )

        response = translate_client.translate_text(
            Text=notes_text,
            SourceLanguageCode="auto",
            TargetLanguageCode=target_language_code,
            TerminologyNames=terminology_names,
        )

        return {
            "original": notes_text[:1000] + ("..." if len(notes_text) > 1000 else ""),
            "translated": response.get("TranslatedText", ""),
            "source_language": response.get("SourceLanguageCode", "auto"),
            "target_language": target_language_code,
            "glossary_used": glossary_name if terminology_names else None,
            "applied_terminologies": response.get("AppliedTerminologies", []),
            "provider": "aws_translate",
        }

    except ClientError as e:
        raise Exception(f"AWS Translate with glossary failed: {e}")


def batch_translate_compliance_documents(
    text_list, target_language_code, job_name=None
):
    """
    Batch translate multiple compliance documents.

    Args:
        text_list: List of texts to translate
        target_language_code: Target language code
        job_name: Optional job name

    Returns:
        dict with batch translation job info
    """
    if job_name is None:
        job_name = f"compliance_translation_{target_language_code}_{json.dumps(os.environ.get('TIMESTAMP', ''))}"

    s3_client = boto3.client(
        "s3", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    translate_client = boto3.client(
        "translate", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    bucket_name = os.environ.get("AWS_TRANSLATE_BUCKET", "compliance-translations")

    try:
        input_key = f"input/{job_name}.json"
        input_data = {
            "documents": [
                {"text": text, "id": f"doc_{i}"} for i, text in enumerate(text_list)
            ]
        }

        s3_client.put_object(
            Bucket=bucket_name,
            Key=input_key,
            Body=json.dumps(input_data, indent=2),
            ContentType="application/json",
        )

        input_uri = f"s3://{bucket_name}/{input_key}"
        output_uri = f"s3://{bucket_name}/output/{job_name}/"

        response = translate_client.start_text_translation_job(
            JobName=job_name,
            InputDataConfig={"S3Uri": input_uri, "ContentType": "application/json"},
            OutputDataConfig={"S3Uri": output_uri},
            DataAccessRoleArn=os.environ.get("AWS_TRANSLATE_ROLE_ARN", ""),
            SourceLanguageCode="auto",
            TargetLanguageCodes=[target_language_code],
        )

        return {
            "job_id": response.get("JobId"),
            "job_name": job_name,
            "job_status": response.get("JobStatus", "SUBMITTED"),
            "input_uri": input_uri,
            "output_uri": output_uri,
            "target_language": target_language_code,
            "document_count": len(text_list),
            "provider": "aws_translate",
        }

    except ClientError as e:
        raise Exception(f"Failed to start batch translation job: {e}")


def create_compliance_glossary(
    glossary_name, terms, source_language="en", target_language="es"
):
    """
    Create a custom glossary for compliance and encryption terms.

    Args:
        glossary_name: Name for the glossary
        terms: Dict of source_term -> target_term
        source_language: Source language code
        target_language: Target language code

    Returns:
        dict with glossary creation result
    """
    translate_client = boto3.client(
        "translate", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    default_terms = {
        "encryption": "cifrado",
        "decryption": "descifrado",
        "key management": "gestión de claves",
        "KMS": "Sistema de Gestión de Claves",
        "HSM": "Módulo de Seguridad de Hardware",
        "ciphertext": "texto cifrado",
        "plaintext": "texto plano",
        "authentication": "autenticación",
        "authorization": "autorización",
        "compliance": "cumplimiento",
        "audit": "auditoría",
        "PCI DSS": "PCI DSS",
        "HIPAA": "HIPAA",
        "GDPR": "GDPR",
        "rotation": "rotación",
        "cryptographic": "criptográfico",
        "algorithm": "algoritmo",
        "symmetric": "simétrico",
        "asymmetric": "asimétrico",
    }

    if terms:
        default_terms.update(terms)

    csv_content = "SourceText,TargetText\n"
    for source, target in default_terms.items():
        csv_content += f'"{source}","{target}"\n'

    s3_client = boto3.client(
        "s3", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    bucket_name = os.environ.get("AWS_TRANSLATE_BUCKET", "compliance-translations")

    try:
        glossary_key = f"glossaries/{glossary_name}.csv"

        s3_client.put_object(
            Bucket=bucket_name,
            Key=glossary_key,
            Body=csv_content,
            ContentType="text/csv",
        )

        glossary_uri = f"s3://{bucket_name}/{glossary_key}"

        response = translate_client.import_terminology(
            Name=glossary_name,
            MergeStrategy="OVERWRITE",
            TerminologyData={"File": csv_content.encode("utf-8"), "Format": "CSV"},
        )

        return {
            "glossary_name": glossary_name,
            "terms_count": len(default_terms),
            "source_language": source_language,
            "target_language": target_language,
            "s3_uri": glossary_uri,
            "arn": response.get("TerminologyProperties", {}).get("Arn", ""),
            "provider": "aws_translate",
        }

    except ClientError as e:
        raise Exception(f"Failed to create compliance glossary: {e}")


def analyze_translation_quality(
    original_text, translated_text, source_lang="en", target_lang="es"
):
    """
    Analyze translation quality for compliance notes.

    Args:
        original_text: Original text
        translated_text: Translated text
        source_lang: Source language
        target_lang: Target language

    Returns:
        dict with quality analysis
    """
    comprehend_client = boto3.client(
        "comprehend", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    try:
        original_entities = comprehend_client.detect_entities(
            Text=original_text[:5000], LanguageCode=source_lang
        )

        translated_entities = comprehend_client.detect_entities(
            Text=translated_text[:5000], LanguageCode=target_lang
        )

        original_key_phrases = comprehend_client.detect_key_phrases(
            Text=original_text[:5000], LanguageCode=source_lang
        )

        translated_key_phrases = comprehend_client.detect_key_phrases(
            Text=translated_text[:5000], LanguageCode=target_lang
        )

        entity_preservation = len(translated_entities.get("Entities", [])) / max(
            1, len(original_entities.get("Entities", []))
        )

        key_phrase_overlap = calculate_phrase_overlap(
            [p["Text"] for p in original_key_phrases.get("KeyPhrases", [])],
            [p["Text"] for p in translated_key_phrases.get("KeyPhrases", [])],
        )

        return {
            "original_length": len(original_text),
            "translated_length": len(translated_text),
            "length_ratio": len(translated_text) / max(1, len(original_text)),
            "entity_preservation_rate": entity_preservation,
            "key_phrase_overlap": key_phrase_overlap,
            "original_entities": len(original_entities.get("Entities", [])),
            "translated_entities": len(translated_entities.get("Entities", [])),
            "original_key_phrases": len(original_key_phrases.get("KeyPhrases", [])),
            "translated_key_phrases": len(translated_key_phrases.get("KeyPhrases", [])),
            "quality_score": (entity_preservation + key_phrase_overlap) / 2,
            "provider": "aws_comprehend",
        }

    except ClientError as e:
        raise Exception(f"Translation quality analysis failed: {e}")


def calculate_phrase_overlap(original_phrases, translated_phrases):
    """Calculate overlap between original and translated key phrases."""
    if not original_phrases or not translated_phrases:
        return 0.0

    original_set = set(phrase.lower() for phrase in original_phrases)
    translated_set = set(phrase.lower() for phrase in translated_phrases)

    intersection = original_set.intersection(translated_set)
    union = original_set.union(translated_set)

    return len(intersection) / len(union) if union else 0.0


if __name__ == "__main__":
    test_note = "Key rotation must be performed every 90 days for PCI DSS compliance. Encryption keys should be stored in AWS KMS with appropriate access controls."

    translation = translate_compliance_notes(test_note, "es")
    print(f"Translation result: {json.dumps(translation, indent=2)}")
