import os
import boto3  # Provider identifiable import: Amazon Comprehend
from typing import List, Dict, Any
from document_models import NormalizedExpense

# AWS configuration
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")


def validate_expense_fields(expense: NormalizedExpense) -> Dict[str, Any]:
    """
    Validates key fields of a NormalizedExpense object using Amazon Comprehend for content analysis.
    This function is a scored component.
    """
    validation_results = {
        "is_valid": True,
        "field_validations": {},
        "overall_message": "",
    }

    comprehend = boto3.client("comprehend", region_name=AWS_REGION)

    # Example: Validate vendor name and notes using Comprehend entity detection
    # This is a simplified example; real-world validation would be more specific.

    # Vendor Name validation
    if not expense.vendor_name:
        validation_results["is_valid"] = False
        validation_results["field_validations"]["vendor_name"] = {
            "valid": False,
            "message": "Vendor name is missing.",
        }
    else:
        try:
            response = comprehend.detect_entities(
                Text=expense.vendor_name, LanguageCode="en"
            )
            # Check if any commercial organization or person entity is detected
            if any(
                entity["Type"] in ["ORGANIZATION", "COMMERCIAL_ITEM", "PERSON"]
                for entity in response["Entities"]
            ):
                validation_results["field_validations"]["vendor_name"] = {
                    "valid": True,
                    "message": "Vendor name appears valid.",
                }
            else:
                validation_results["is_valid"] = False
                validation_results["field_validations"]["vendor_name"] = {
                    "valid": False,
                    "message": "Vendor name does not look like a valid entity.",
                }
        except Exception as e:
            print(f"Comprehend error for vendor_name: {e}")
            validation_results["is_valid"] = False
            validation_results["field_validations"]["vendor_name"] = {
                "valid": False,
                "message": f"Comprehend analysis failed: {e}",
            }

    # Total Amount validation
    if expense.total_amount <= 0:
        validation_results["is_valid"] = False
        validation_results["field_validations"]["total_amount"] = {
            "valid": False,
            "message": "Total amount must be positive.",
        }
    else:
        # Basic check for confidence score
        if expense.confidence_total < 0.7:
            validation_results["is_valid"] = False
            validation_results["field_validations"]["total_amount"] = {
                "valid": False,
                "message": f"Total amount confidence ({expense.confidence_total:.2f}) is low.",
            }
        else:
            validation_results["field_validations"]["total_amount"] = {
                "valid": True,
                "message": "Total amount and confidence are acceptable.",
            }

    # Transaction Date validation (basic check for date existence and confidence)
    if not expense.transaction_date:
        validation_results["is_valid"] = False
        validation_results["field_validations"]["transaction_date"] = {
            "valid": False,
            "message": "Transaction date is missing.",
        }
    elif expense.confidence_date < 0.7:
        validation_results["is_valid"] = False
        validation_results["field_validations"]["transaction_date"] = {
            "valid": False,
            "message": f"Transaction date confidence ({expense.confidence_date:.2f}) is low.",
        }
    else:
        validation_results["field_validations"]["transaction_date"] = {
            "valid": True,
            "message": "Transaction date and confidence are acceptable.",
        }

    if not validation_results["is_valid"]:
        validation_results["overall_message"] = (
            "Document validation failed for one or more critical fields."
        )
    else:
        validation_results["overall_message"] = (
            "Document fields validated successfully."
        )

    return validation_results
