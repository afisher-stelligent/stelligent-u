import json

def lambda_handler(event, context):
    first_key = event.get('key1')
    second_key = event.get('key2')
    return {
        'statusCode': 200,
        'body': json.dumps(f'First Key is {first_key}')
        }