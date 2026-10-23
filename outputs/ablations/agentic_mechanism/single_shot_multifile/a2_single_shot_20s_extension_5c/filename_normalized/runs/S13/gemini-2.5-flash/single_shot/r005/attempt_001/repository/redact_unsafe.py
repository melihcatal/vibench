import os
from google.cloud import dlp_v2
from safety_client import load_google_dlp_client
from safety_models import RedactionResult

def redact_unsafe(text: str, project_id: str) -> RedactionResult:
    client = load_google_dlp_client()

    # The type of info the inspect() and redact() methods will look for.
    info_types = [
        {"name": "EMAIL_ADDRESS"},
        {"name": "PHONE_NUMBER"},
        {"name": "CREDIT_CARD_NUMBER"},
        {"name": "IP_ADDRESS"},
        {"name": "US_SOCIAL_SECURITY_NUMBER"}
    ]

    # The inspect_config contains the info_types and likelihood.
    inspect_config = {
        "info_types": info_types,
        "min_likelihood": dlp_v2.Likelihood.POSSIBLE
    }

    # The redact_config specifies how to redact. Here we replace with a fixed string.
    # For this task, we will just use a character mask or replacement.
    # More advanced redaction would use `ReplaceConfig` or `RedactImageConfig`.
    # For simplicity here, we use a basic character replacement for text.
    redaction_config = dlp_v2.DeidentifyConfig(
        info_type_transformations=dlp_v2.DeidentifyConfig.InfoTypeTransformations(
            transformations=[
                dlp_v2.DeidentifyConfig.InfoTypeTransformations.InfoTypeTransformation(
                    info_types=info_types,
                    primitive_transformation=dlp_v2.PrimitiveTransformation(
                        character_mask_config=dlp_v2.PrimitiveTransformation.CharacterMaskConfig(
                            masking_character="*"
                        )
                    ),
                )
            ]
        )
    )

    parent = f"projects/{project_id}"

    response = client.deidentify_content(
        request={
            "parent": parent,
            "deidentify_config": redaction_config,
            "inspect_config": inspect_config,
            "item": {"value": text},
        }
    )
    
    redacted_text = response.item.value
    findings = []
    if response.overview and response.overview.transformed_bytes:
        # DLP's deidentify_content doesn't return detailed findings about what was redacted for text transformation.
        # To get findings, we would typically run an inspect_content separately.
        # For this exercise, we will assume that if text was transformed, something was found.
        # A more complete implementation would use inspect_content first.
        inspect_response = client.inspect_content(request={
            "parent": parent,
            "inspect_config": inspect_config,
            "item": {"value": text}
        })
        if inspect_response.result and inspect_response.result.findings:
            for finding in inspect_response.result.findings:
                findings.append(f"{finding.info_type.name} detected with likelihood {dlp_v2.Likelihood(finding.likelihood).name}")

    return RedactionResult(original_text=text, redacted_text=redacted_text, detected_issues=findings)
