import boto3
import os

client = boto3.client('sagemaker')

response = client.create_model(
    ModelName='spotify_recommender',
    PrimaryContainer={
        'Image': os.environ['ecr_training_image'],
        'Mode': 'SingleModel',
        'Environment': {
            'environment': os.environ['environment']
        },
    },
    ExecutionRoleArn=os.environ['sagemaker_execution_role_arn'],
    VpcConfig={
        'Subnets': [
            os.environ['subnet_1'],
            os.environ['subnet_2']        
            ]
    }
)