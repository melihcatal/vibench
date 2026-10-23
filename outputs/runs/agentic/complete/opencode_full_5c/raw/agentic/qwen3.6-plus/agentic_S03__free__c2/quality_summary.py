import re
from typing import List, Optional
from translation_models import (
    QualitySummary,
    QualityIssue,
    TranslationResponse,
    normalize_language_code,
)
from translation_client import get_deepl_client, DEEPL_API_ENDPOINT


def analyze_length_ratio(
    source_text: str, translated_text: str, target_lang: str
) -> Optional[QualityIssue]:
    if not source_text or not translated_text:
        return None
    source_len = len(source_text)
    translated_len = len(translated_text)
    ratio = translated_len / source_len if source_len > 0 else 0
    lang_expansion = {
        "DE": 1.15,
        "FR": 1.15,
        "ES": 1.10,
        "IT": 1.10,
        "PT": 1.10,
        "RU": 1.20,
        "JA": 0.6,
        "ZH": 0.6,
        "KO": 0.7,
    }
    expected_max = lang_expansion.get(target_lang.upper(), 1.25)
    expected_min = lang_expansion.get(target_lang.upper(), 0.5)
    if ratio > expected_max * 1.3:
        return QualityIssue(
            issue_type="length_expansion",
            severity="warning",
            description=f"Translation length ratio {ratio:.2f} exceeds expected maximum {expected_max * 1.3:.2f} for {target_lang}",
        )
    if ratio < expected_min * 0.5:
        return QualityIssue(
            issue_type="length_contraction",
            severity="warning",
            description=f"Translation length ratio {ratio:.2f} is below expected minimum {expected_min * 0.5:.2f} for {target_lang}",
        )
    return None


def check_character_set_consistency(
    source_text: str, translated_text: str, target_lang: str
) -> Optional[QualityIssue]:
    target_lang_upper = target_lang.upper()
    if target_lang_upper in ("JA", "ZH", "KO"):
        cjk_pattern = re.compile(
            r"[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\uac00-\ud7af]"
        )
        if not cjk_pattern.search(translated_text):
            return QualityIssue(
                issue_type="missing_script",
                severity="error",
                description=f"Translation for {target_lang} contains no expected CJK characters",
            )
    elif target_lang_upper in ("RU", "UK", "BG"):
        cyrillic_pattern = re.compile(r"[\u0400-\u04ff]")
        if not cyrillic_pattern.search(translated_text):
            return QualityIssue(
                issue_type="missing_script",
                severity="error",
                description=f"Translation for {target_lang} contains no expected Cyrillic characters",
            )
    elif target_lang_upper in ("AR", "FA", "UR"):
        arabic_pattern = re.compile(r"[\u0600-\u06ff\u0750-\u077f]")
        if not arabic_pattern.search(translated_text):
            return QualityIssue(
                issue_type="missing_script",
                severity="error",
                description=f"Translation for {target_lang} contains no expected Arabic script characters",
            )
    return None


def check_untranslated_segments(
    source_text: str, translated_text: str
) -> Optional[QualityIssue]:
    if source_text.strip().lower() == translated_text.strip().lower():
        return QualityIssue(
            issue_type="untranslated",
            severity="error",
            description="Source and translated text are identical, translation may not have been applied",
        )
    return None


def generate_quality_summary(
    source_texts: List[str],
    translations: List[TranslationResponse],
) -> QualitySummary:
    client = get_deepl_client()
    issues = []
    total_chars = 0
    language_pair = ""
    for i, (source, translation) in enumerate(zip(source_texts, translations)):
        total_chars += translation.character_count
        if not language_pair:
            language_pair = f"{translation.source_lang}-{translation.target_lang}"
        length_issue = analyze_length_ratio(
            source, translation.translated_text, translation.target_lang
        )
        if length_issue:
            length_issue.segment_index = i
            issues.append(length_issue)
        script_issue = check_character_set_consistency(
            source, translation.translated_text, translation.target_lang
        )
        if script_issue:
            script_issue.segment_index = i
            issues.append(script_issue)
        untranslated_issue = check_untranslated_segments(
            source, translation.translated_text
        )
        if untranslated_issue:
            untranslated_issue.segment_index = i
            issues.append(untranslated_issue)
    error_count = sum(1 for issue in issues if issue.severity == "error")
    warning_count = sum(1 for issue in issues if issue.severity == "warning")
    penalty = (error_count * 0.15) + (warning_count * 0.05)
    overall_score = max(0.0, min(1.0, 1.0 - penalty))
    return QualitySummary(
        overall_score=round(overall_score, 2),
        issues=issues,
        character_count=total_chars,
        language_pair=language_pair,
    )
