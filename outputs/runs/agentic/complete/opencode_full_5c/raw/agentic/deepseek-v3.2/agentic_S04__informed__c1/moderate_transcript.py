import boto3
from typing import List, Dict, Any, Optional
import json


def moderate_transcript_text(text: str, language_code: str = "en") -> Dict[str, Any]:
    """
    Moderate transcript text before publishing using Amazon Comprehend.

    Args:
        text: Transcript text to moderate
        language_code: Language code for analysis

    Returns:
        Moderation results with toxicity scores and flagged content
    """
    comprehend_client = boto3.client("comprehend")

    if len(text) > 5000:
        chunks = [text[i : i + 5000] for i in range(0, len(text), 5000)]
        results = []
        for chunk in chunks:
            result = moderate_transcript_text(chunk, language_code)
            results.append(result)

        return combine_moderation_results(results)

    try:
        response = comprehend_client.detect_toxic_content(
            TextSegments=[{"Text": text}], LanguageCode=language_code
        )

        result_list = response["ResultList"]
        if not result_list:
            return {
                "text": text,
                "is_toxic": False,
                "toxicity_score": 0.0,
                "labels": [],
                "moderation_passed": True,
            }

        result = result_list[0]
        labels = result["Labels"]

        max_toxicity = max((label["Score"] for label in labels), default=0.0)
        is_toxic = max_toxicity > 0.5

        toxic_labels = [
            {
                "name": label["Name"],
                "score": label["Score"],
                "is_toxic": label["Score"] > 0.5,
            }
            for label in labels
        ]

        return {
            "text": text,
            "is_toxic": is_toxic,
            "toxicity_score": max_toxicity,
            "labels": toxic_labels,
            "moderation_passed": not is_toxic,
            "raw_response": result,
        }

    except Exception as e:
        return {
            "text": text,
            "is_toxic": False,
            "toxicity_score": 0.0,
            "labels": [],
            "moderation_passed": True,
            "error": str(e),
        }


def moderate_transcript_segments(
    segments: List[Dict[str, Any]], language_code: str = "en"
) -> List[Dict[str, Any]]:
    """
    Moderate transcript segments individually.

    Args:
        segments: List of transcript segments
        language_code: Language code for analysis

    Returns:
        Segments with added moderation results
    """
    moderated_segments = []

    for segment in segments:
        text = segment.get("text", "")

        moderation_result = moderate_transcript_text(text, language_code)

        moderated_segment = {
            **segment,
            "moderation": moderation_result,
            "requires_review": moderation_result.get("is_toxic", False),
            "moderation_score": moderation_result.get("toxicity_score", 0.0),
        }

        moderated_segments.append(moderated_segment)

    return moderated_segments


def check_content_safety(transcript_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check content safety of entire transcript.

    Args:
        transcript_data: Transcript data from poll_transcription_job

    Returns:
        Content safety analysis
    """
    text = transcript_data.get("transcript", "")

    moderation_result = moderate_transcript_text(text)

    segments = transcript_data.get("speakers", [])
    segment_moderation = []

    if segments:
        for segment in segments:
            segment_text = segment.get("text", "")
            seg_mod = moderate_transcript_text(segment_text)
            segment_moderation.append(
                {
                    "speaker": segment.get("speaker_label", "unknown"),
                    "start_time": segment.get("start_time"),
                    "moderation": seg_mod,
                }
            )

    toxic_segments = [
        seg for seg in segment_moderation if seg["moderation"].get("is_toxic", False)
    ]

    return {
        "overall_moderation": moderation_result,
        "segment_moderation": segment_moderation,
        "toxic_segment_count": len(toxic_segments),
        "requires_human_review": len(toxic_segments) > 0
        or moderation_result.get("is_toxic", False),
        "summary": {
            "total_segments": len(segments),
            "toxic_segments": len(toxic_segments),
            "max_toxicity_score": moderation_result.get("toxicity_score", 0.0),
            "recommendation": "REVIEW_REQUIRED"
            if len(toxic_segments) > 0
            else "SAFE_TO_PUBLISH",
        },
    }


def combine_moderation_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Combine multiple moderation results.

    Args:
        results: List of moderation results

    Returns:
        Combined moderation result
    """
    if not results:
        return {
            "text": "",
            "is_toxic": False,
            "toxicity_score": 0.0,
            "labels": [],
            "moderation_passed": True,
        }

    all_labels = []
    max_toxicity = 0.0

    for result in results:
        max_toxicity = max(max_toxicity, result.get("toxicity_score", 0.0))
        all_labels.extend(result.get("labels", []))

    is_toxic = max_toxicity > 0.5

    unique_labels = {}
    for label in all_labels:
        name = label["name"]
        if name not in unique_labels or label["score"] > unique_labels[name]["score"]:
            unique_labels[name] = label

    return {
        "text": " ".join([r.get("text", "") for r in results]),
        "is_toxic": is_toxic,
        "toxicity_score": max_toxicity,
        "labels": list(unique_labels.values()),
        "moderation_passed": not is_toxic,
        "combined_from_multiple": True,
        "segment_count": len(results),
    }


def get_moderation_report(transcript_data: Dict[str, Any]) -> str:
    """
    Generate a human-readable moderation report.

    Args:
        transcript_data: Transcript data

    Returns:
        Formatted moderation report
    """
    safety_check = check_content_safety(transcript_data)

    report_lines = []
    report_lines.append("=== TRANSCRIPT MODERATION REPORT ===")
    report_lines.append("")

    overall = safety_check["overall_moderation"]
    report_lines.append(
        f"Overall Toxicity Score: {overall.get('toxicity_score', 0.0):.3f}"
    )
    report_lines.append(
        f"Requires Human Review: {safety_check['requires_human_review']}"
    )
    report_lines.append("")

    if safety_check["toxic_segment_count"] > 0:
        report_lines.append(
            f"TOXIC SEGMENTS FOUND: {safety_check['toxic_segment_count']}"
        )
        report_lines.append("")

        for i, segment in enumerate(safety_check["segment_moderation"]):
            if segment["moderation"].get("is_toxic", False):
                report_lines.append(f"Segment {i + 1}:")
                report_lines.append(f"  Speaker: {segment.get('speaker', 'unknown')}")
                report_lines.append(f"  Start Time: {segment.get('start_time', 'N/A')}")
                report_lines.append(
                    f"  Toxicity Score: {segment['moderation'].get('toxicity_score', 0.0):.3f}"
                )

                toxic_labels = [
                    f"{label['name']} ({label['score']:.3f})"
                    for label in segment["moderation"].get("labels", [])
                    if label.get("is_toxic", False)
                ]
                if toxic_labels:
                    report_lines.append(f"  Toxic Labels: {', '.join(toxic_labels)}")
                report_lines.append("")

    summary = safety_check["summary"]
    report_lines.append("=== SUMMARY ===")
    report_lines.append(f"Total Segments: {summary['total_segments']}")
    report_lines.append(f"Toxic Segments: {summary['toxic_segments']}")
    report_lines.append(f"Maximum Toxicity: {summary['max_toxicity_score']:.3f}")
    report_lines.append(f"Recommendation: {summary['recommendation']}")

    return "\n".join(report_lines)
