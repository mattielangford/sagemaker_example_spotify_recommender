import boto3

client = boto3.client('sagemaker')

response = client.create_endpoint_config(
    EndpointConfigName='spotify_recommender_config',
    ProductionVariants=[
        {
            'VariantName': 'spotify_recommender_A',
            'ModelName': 'spotify_recommender',
            'InitialInstanceCount': 1,
            'InstanceType': 'ml.t2.medium',
        },
    ]
)

response = client.update_endpoint(
    EndpointName='spotify_recommender_inference',
    EndpointConfigName='spotify_recommender_config',
    RetainAllVariantProperties=True)
    