import boto3

def select_platform_resource():
    # Initialize a session using Amazon SageMaker
    sagemaker_client = boto3.client('sagemaker')
    
    # Specify the name of the model
    model_name = 'my-sagemaker-model'
    
    # Describe the model to get its details
    response = sagemaker_client.describe_model(ModelName=model_name)
    
    # Extract and return the model ARN
    model_arn = response['ModelArn']
    return model_arn

if __name__ == '__main__':\n    model_arn = select_platform_resource()
    print(f'Selected model ARN: {model_arn}')
