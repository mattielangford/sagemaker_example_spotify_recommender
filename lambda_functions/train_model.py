import boto3
import os

client = boto3.client('sagemaker')

response = client.create_training_job(
    TrainingJobName='spotify_recommender',
    AlgorithmSpecification={
        'TrainingImage': os.environ['ecr_training_image']
    },
    RoleArn=os.environ['sagemaker_execution_role_arn'],
    ResourceConfig={
        'InstanceType': 'ml.m4.xlarge',
        'InstanceCount': 1
    },
    VpcConfig={
        'SecurityGroupIds': [
            os.environ['vpc'],
        ],
        'Subnets': [
            os.environ['subnet_1'],
            os.environ['subnet_2']
        ]
    },
    StoppingCondition={
        'MaxRuntimeInSeconds': 3600,
        'MaxWaitTimeInSeconds': 60
    },
    Environment={
        'environment': os.environ['environment']
    },
    RetryStrategy={
        'MaximumRetryAttempts': 3
    }
)