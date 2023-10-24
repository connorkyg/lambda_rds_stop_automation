import json
import boto3
from botocore.exceptions import ClientError


def get_secrets(secret_name, region: str = 'ap-northeast-2', output: str = 'json'):
    """
    Get Slack Webhook URL
    :return: WebhookURL
    """
    # Create a Secrets Manager client
    session = boto3.session.Session(
        region_name=region
    )
    client = session.client(
        service_name='secretsmanager'
    )

    try:
        response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = response['SecretString']
    secret_dict = json.loads(secret)
    return secret_dict


def check_rds_state(instance_id, region):
    rds = boto3.client('rds', region_name=region)
    response = rds.describe_db_instances(DBInstanceIdentifier=instance_id)
    instance_status = response['DBInstances'][0]['DBInstanceStatus']
    if instance_status == 'available':
        rds.stop_db_instance(DBInstanceIdentifier=instance_id)
        return {
            'statusCode': 200,
            'body': f"Stopped RDS instance: {instance_id}"
        }
    else:
        return {
            'statusCode': 406,
            'body': f"Failed to stop RDS instance: {instance_id}"
                    f"Current status: {instance_status}"
        }
    print(instance_id)