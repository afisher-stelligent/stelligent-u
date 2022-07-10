import boto3
from operator import itemgetter

client = boto3.client('ec2', region_name='us-west-1')
response = client.describe_images(
    Filters=[
        {
            'Name': 'description',
            'Values': [
                'Microsoft Windows Server 2012*',
            ]
        },
    ],
    Owners=[
        'amazon'
    ]
)
# Sort on Creation date Desc
image_details = sorted(response['Images'],key=itemgetter('CreationDate'),reverse=True)
ami_id = image_details[0]['ImageId']
print(ami_id)
