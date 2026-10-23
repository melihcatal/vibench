import os
from typing import List, Dict, Any
import boto3
from botocore.exceptions import ClientError
from security_models import SecretRotationStatus

def summarize_aws_secret_rotation_status(secret_arn: str, resource_type: str = "AWS::SecretsManager::Secret") -> SecretRotationStatus:
    """Summarizes the rotation status of an AWS Secrets Manager secret using AWS Config.

    This function checks AWS Config for compliance status related to the given secret. 
    It assumes relevant Config rules are in place for secret rotation. 
    E.g., `secretsmanager-secret-rotation-enabled`.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    config_client = boto3.client('config', region_name=region_name)
    secrets_manager_client = boto3.client('secretsmanager', region_name=region_name)

    is_compliant = True
    compliance_details: Dict[str, Any] = {}
    last_rotation_date: str = "N/A"

    try:
        # Get secret details for LastRotatedDate
        secret_desc = secrets_manager_client.describe_secret(SecretId=secret_arn)
        if 'LastRotatedDate' in secret_desc:
            last_rotation_date = secret_desc['LastRotatedDate'].isoformat()

        # Check AWS Config compliance for the secret
        response = config_client.get_compliance_details_by_resource(
            ResourceType=resource_type,
            ResourceId=secret_arn,
            ComplianceTypes=['COMPLIANT', 'NON_COMPLIANT']
        )

        if response['EvaluationResults']:
            for result in response['EvaluationResults']:
                if result['ComplianceType'] == 'NON_COMPLIANT':
                    is_compliant = False
                    compliance_details[result['ConfigRuleName']] = {
                        'compliance_type': result['ComplianceType'],
                        'annotation': result.get('Annotation')
                    }
                elif result['ComplianceType'] == 'COMPLIANT':
                    compliance_details[result['ConfigRuleName']] = {
                        'compliance_type': result['ComplianceType']
                    }
        else:
            # If no evaluation results, it might mean no rules apply or it's not evaluated yet
            is_compliant = False # Assume non-compliant if no positive compliance is found
            compliance_details["no_evaluation_results"] = "No AWS Config rules evaluated this resource or no results found."

    except ClientError as e:
        raise ValueError(f"Error summarizing secret rotation status for '{secret_arn}': {e}") from e
    except Exception as e:
        raise ValueError(f"An unexpected error occurred: {e}") from e

    return SecretRotationStatus(
        secret_id=secret_arn,
        is_compliant=is_compliant,
        compliance_details=compliance_details,
        last_rotation_date=last_rotation_date
    )
