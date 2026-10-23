from model_client import bedrock_client, inference_profile_arn, model_id, project_arn


def select_platform_resource():
    if project_arn():
        return {"projectArn": project_arn()}
    if inference_profile_arn():
        return {"inferenceProfileArn": inference_profile_arn()}
    client = bedrock_client()
    return {"foundationModelId": model_id(), "region": client.meta.region_name}
