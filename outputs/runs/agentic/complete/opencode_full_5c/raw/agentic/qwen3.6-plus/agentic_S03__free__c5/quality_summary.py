from google.cloud import language_v1
from translation_models import TranslationQualitySummary, TranslationQualityIssue


GOOGLE_NL_API_ENDPOINT = "language.googleapis.com"
GOOGLE_NL_MODEL = "language-v1"


def analyze_translation_quality(
    translations: list, target_language: str = "es"
) -> dict:
    client = language_v1.LanguageServiceClient()

    issues = []
    total_score = 0.0
    segment_count = len(translations)

    for item in translations:
        text = item.get("translated_text", "")
        if not text:
            issues.append(
                TranslationQualityIssue(
                    segment=item.get("original", ""),
                    issue_type="empty_translation",
                    severity="critical",
                    description="Translation returned empty result",
                )
            )
            continue

        document = language_v1.Document(
            content=text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
            language=target_language,
        )

        sentiment = client.analyze_sentiment(
            request={"document": document}
        ).document_sentiment
        entities = client.analyze_entities(request={"document": document}).entities

        score = (sentiment.score + 1) / 2.0
        total_score += score

        if sentiment.magnitude > 1.5 and sentiment.score < -0.3:
            issues.append(
                TranslationQualityIssue(
                    segment=text,
                    issue_type="negative_sentiment",
                    severity="warning",
                    description=f"Strong negative sentiment detected (score: {sentiment.score:.2f})",
                )
            )

        for entity in entities:
            if (
                entity.type_ == language_v1.Entity.Type.LOCATION
                and entity.salience > 0.8
            ):
                issues.append(
                    TranslationQualityIssue(
                        segment=text,
                        issue_type="high_entity_salience",
                        severity="info",
                        description=f"Location entity '{entity.name}' has high salience ({entity.salience:.2f})",
                    )
                )

    overall_score = total_score / segment_count if segment_count > 0 else 0.0

    summary = TranslationQualitySummary(
        overall_score=round(overall_score, 3),
        issues=issues,
        segment_count=segment_count,
    )

    return {
        "overall_quality_score": summary.overall_score,
        "segment_count": summary.segment_count,
        "issue_count": len(summary.issues),
        "issues": [
            {
                "segment": issue.segment,
                "issue_type": issue.issue_type,
                "severity": issue.severity,
                "description": issue.description,
            }
            for issue in summary.issues
        ],
        "provider": "google-cloud-natural-language",
        "model": GOOGLE_NL_MODEL,
    }
