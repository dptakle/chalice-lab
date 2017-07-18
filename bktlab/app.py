from chalice import Chalice
import json
import sys
import boto3
import traceback

app = Chalice(app_name='bktlab')


@app.lambda_function(name='bktlab-worker')
def run_experiment(event, context):
    if 'bucket' in event and 'key' in event:
        r = put_some_stuff(event)
    else:
        r = {
                'error': 'missing stuff'
            }
    return r


@app.route('/')
def index():
    return {'answer': 42}


def put_some_stuff(event):
    stuff = {'x': 96}
    s3_client = get_api_client('s3')
    r = s3_client.put_object(
        Body=json.dumps(stuff),
        Bucket=event['bucket'],
        Key=event['key'],
        ContentType='application/octet-stream',
        ContentEncoding=''
    )

    return r


def get_api_client(aws_service):
    try:
        api_session = boto3.Session()
        api_client = api_session.client(aws_service)
        return api_client
    except Exception as x:
        print('Exception caught in get_api_client(): {}'.format(x))
        traceback.print_exc(file=sys.stdout)
        return None
