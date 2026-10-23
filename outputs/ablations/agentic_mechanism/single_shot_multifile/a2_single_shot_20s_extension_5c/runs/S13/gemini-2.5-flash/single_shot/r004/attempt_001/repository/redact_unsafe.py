import os
from google.cloud import dlp_v2
from safety_models import RedactionResult, RedactionSpan

def redact_unsafe(text: str, project_id: str) -> RedactionResult:
    dlp_client = dlp_v2.DlpServiceClient()
    parent = f"projects/{project_id}"

    custom_info_type = dlp_v2.CustomInfoType(
        info_type=dlp_v2.InfoType(name="UNSAFE_WORDS_CUSTOM"),
        dictionary=dlp_v2.CustomInfoType.Dictionary(
            word_list=dlp_v2.CustomInfoType.Dictionary.WordList(
                words=["badword", "illegalterm", "hatephrase", "profanity", "violence"] # Example unsafe words
            )
        )
    )
    
    inspect_config = dlp_v2.InspectConfig(
        info_types=[
            dlp_v2.InfoType(name="EMAIL_ADDRESS"),
            dlp_v2.InfoType(name="PHONE_NUMBER"),
            dlp_v2.InfoType(name="CREDIT_CARD_NUMBER"),
        ],
        custom_info_types=[custom_info_type],
        min_likelihood=dlp_v2.Likelihood.POSSIBLE,
        include_quote=True,
    )
    
    item = dlp_v2.ContentItem(value=text)
    
    inspect_response = dlp_client.inspect_content(
        request=dlp_v2.InspectContentRequest(
            parent=parent,
            inspect_config=inspect_config,
            item=item
        )
    )

    redaction_spans = []
    redacted_text_list = list(text)

    findings = sorted(inspect_response.result.findings, key=lambda f: f.location.byte_range.start, reverse=True)

    for finding in findings:
        start = finding.location.byte_range.start
        end = finding.location.byte_range.end
        original_span = text[start:end]
        
        replacement_char = "*"
        redacted_span_str = replacement_char * (end - start)
        redacted_text_list[start:end] = list(redacted_span_str)

        redaction_spans.append(RedactionSpan(
            start=start,
            end=end,
            original_text=original_span,
            redacted_text=redacted_span_str
        ))
    
    final_redacted_text = "".join(redacted_text_list)

    return RedactionResult(original_text=text, redacted_text=final_redacted_text, spans=redaction_spans)