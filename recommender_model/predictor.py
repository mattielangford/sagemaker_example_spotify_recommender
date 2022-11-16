import boto3
import pandas as pd
from io import StringIO
from recommender import RecommendSongs
import os
import flask

BUCKET_NAME = os.environ['MODEL_BUCKET']
OBJ_KEY = os.environ['MODEL_DATA_KEY']

client = boto3.client('s3', 'us-east-1')

def get_model_data(s3_client):
    csv_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=OBJ_KEY)['Body']
    csv_string = csv_obj.read().decode('utf-8')
    return pd.read_csv(StringIO(csv_string))


app = flask.Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping(): 
    return flask.Response(response='\n', status=200, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def transformation():
    if flask.request.content_type == 'application/json':
        model_data = get_model_data(client)

        test_row = flask.request.get_json()['data']
        predictions = RecommendSongs(model_data, test_row).predictions
        return flask.Response(response=predictions.to_dict(), status=200, mimetype='application/json')
    else:
        return flask.Response(response='This predictor only supports json data', status=415, mimetype='text/plain')
