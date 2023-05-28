import json

import boto3 as boto3
import botocore.exceptions


def hello(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    return {"statusCode": 200, "body": json.dumps(body)}


def start_instances(event, context):
    try:
        ec2 = boto3.client('ec2')
        ec2.start_instances(InstanceIds=['i-0e9f1e0c4f5b2b5c9'], DryRun=True)
        return 'Success'

    except botocore.exceptions.ClientError as e:
        return e.response['Error']['Message']


def stop_instances(event, context):
    try:
        ec2 = boto3.client('ec2')
        ec2.stop_instances(InstanceIds=['i-0e9f1e0c4f5b2b5c9'], DryRun=True)
        return 'Success'

    except botocore.exceptions.ClientError as e:
        return e.response['Error']['Message']
