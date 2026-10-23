import boto3

# Configuration for AWS SageMaker
REGION = 'us-west-2'

# Initialize the SageMaker client
sagemaker_client = boto3.client('sagemaker', region_name=REGION)

def create_model(model_name, primary_container):
    """Create a new model in Amazon SageMaker"""
    response = sagemaker_client.create_model(
        ModelName=model_name,
        ExecutionRoleArn='arn:aws:iam::123456789012:role/SageMakerRole',
        PrimaryContainer=primary_container
    )
    return response

def deploy_model(model_name, endpoint_config_name, production_variants):
    """Deploy a model to an endpoint in Amazon SageMaker"""
    response = sagemaker_client.create_endpoint_config(
        EndpointConfigName=endpoint_config_name,
        ProductionVariants=production_variants
    )
    sagemaker_client.create_endpoint(
        EndpointName=endpoint_config_name
    )
    return response
