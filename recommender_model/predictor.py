import boto3
import pandas as pd
from io import StringIO
from constants import BUCKET_NAME, SONG_TITLE
from recommender import RecommendSongs
import os
import json
import sys
import signal
import traceback
import flask

prefix = '/opt/ml/'
model_path = os.path.join(prefix, 'model')

client = boto3.client('s3', 'us-east-1')

def get_csv(s3_client, object_key):
    csv_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=object_key)['Body']
    csv_string = csv_obj.read().decode('utf-8')
    return pd.read_csv(StringIO(csv_string))

def predict(data):
    test_song = data[SONG_TITLE].values[0]
    train_data = get_csv(client, 'spotify_dataset.csv')
    results = RecommendSongs(music_data=train_data.append(data), song=test_song)
    return str(results.predictions.values.tolist())

app = flask.Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping(): 
    return flask.Response(response='\n', status=200, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def transformation():
    if flask.request.content_type == 'application/json':
        test_row = flask.request.get_json()['data']
        predictions = predict(pd.read_json(test_row)))
        return flask.Response(response=predictions, status=200, mimetype='text/plain')
    else:
        return flask.Response(response='This predictor only supports json data', status=415, mimetype='text/plain')