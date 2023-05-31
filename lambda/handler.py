import json

import boto3 as boto3
import botocore.exceptions


def hello(event, context):
    body = {        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    return {"statusCode": 200, "body": json.dumps(body)}


def start_instances(event, context):
    try:
        ec2 = boto3.client('ec2')
        all_instances = ec2.describe_instances(
            Filters=[
                {
                    'Name': 'instance-state-name',
                    'Values': ['stopped']
                },
            ],
        )
        was_started = False
        for instance in all_instances['Reservations'][0]['Instances']:
            all_tags = instance['Tags']    # Get all tags for the instance
            for tag in all_tags:        # Find the tag with Key = Name
                if tag['Key'] == 'scheduler':
                    if tag['Value'] == 'true':
                        was_started = True
                        ec2.start_instances(InstanceIds=[instance['InstanceId']], DryRun=True)
                        print('Started instance: ' + instance['InstanceId'])
        if not was_started:
            print('No instances to start')

    except botocore.exceptions.ClientError as e:
        return e.response['Error']['Message']


def end_instances(event, context):
    try:
        ec2 = boto3.client('ec2')
        all_instances = ec2.describe_instances(
            Filters=[
                {
                    'Name': 'instance-state-name',
                    'Values': ['running']
                },
            ],
        )
        was_stopped = False
        for instance in all_instances['Reservations'][0]['Instances']:
            all_tags = instance['Tags']    # Get all tags for the instance
            for tag in all_tags:        # Find the tag with Key = Name
                if tag['Key'] == 'scheduler':
                    if tag['Value'] == 'true':
                        was_stopped = True
                        ec2.stop_instances(InstanceIds=[instance['InstanceId']], DryRun=True)
                        print('Stopped instance: ' + instance['InstanceId'])
        if not was_stopped:
            print('No instances to stop')
    except botocore.exceptions.ClientError as e:
        return e.response['Error']['Message']
