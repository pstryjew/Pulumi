import json
import urllib.parse
import boto3
import time

s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    # Get the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    try:
        current_time = time.time()
        time_string = time.ctime(current_time)

        dynamodb.put_item(TableName='Pulumi_Objects', 
        Item={
            'ObjectKey': {'S' : key },
            'TimeStamp': {'S' : time_string},
            }
            )

        return
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
