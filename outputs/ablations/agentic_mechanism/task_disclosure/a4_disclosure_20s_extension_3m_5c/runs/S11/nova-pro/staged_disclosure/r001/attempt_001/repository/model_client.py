import boto3

class ModelClient:
    def __init__(self, region_name='us-west-2'):
        self.sagemaker_client = boto3.client('sagemaker', region_name=region_name)

    def list_models(self):
        response = self.sagemaker_client.list_models()
        return response['Models']

    def describe_model(self, model_name):
        response = self.sagemaker_client.describe_model(ModelName=model_name)
        return response

    def create_model(self, model_name, primary_container, execution_role_arn):
        response = self.sagemaker_client.create_model(
            ModelName=model_name,
            ExecutionRoleArn=execution_role_arn,
            Containers=[primary_container]
        )
        return response

    def delete_model(self, model_name):
        response = self.sagemaker_client.delete_model(ModelName=model_name)
        return response