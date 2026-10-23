from security_client import get_sns_client
from security_models import RotationSummary
import os
import json

def publish_rotation_summary(summary: RotationSummary, topic_arn: str) -> str:
    """Publishes a secret rotation summary to an AWS SNS topic.

    Args:
        summary: The RotationSummary object containing the details of the rotation.
        topic_arn: The ARN of the SNS topic to publish to.

    Returns:
        The MessageId of the published message.
    """
    client = get_sns_client(region_name=os.environ.get('AWS_REGION', 'us-east-1'))
    try:
        message = json.dumps({
            'secret_id': summary.secret_id,
            'status': summary.status,
            'message': summary.message,
            'rotated_at': summary.rotated_at
        })
        response = client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=f"Secret Rotation Summary for {summary.secret_id}"
        )
        return response['MessageId']
    except Exception as e:
        raise RuntimeError(f"Error publishing rotation summary to SNS topic {topic_arn}: {e}")
