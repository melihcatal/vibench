import boto3

def select_platform_resource():
    # Initialize a session using Amazon SageMaker
    sagemaker_client = boto3.client('sagemaker')
    
    # Specify the name of the model
    model_name = 'my-sagemaker-model'
    
    # Describe the model to get its details
    response = sagemaker_client.describe_model(ModelName=model_name)
    
    # Extract the model details
    model_details = response['ModelArn']
    
    print(f'Selected model: {model_details}')
    
if __name__ == '__main__':
    select_platform_resource()