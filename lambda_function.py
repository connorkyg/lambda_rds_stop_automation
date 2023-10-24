import aws_service
import slack
import convert
import json


def lambda_handler(event, context):
    webhook_url = aws_service.get_secrets(secret_name="slack-webhookURL-yk.kwon")['SLACK_WEBHOOK_URL']
    notifier = slack.SlackNotifier(webhook_url)

    # if received from Lambda invoke (EventBridge)
    if 'instanceId' in event:
        for region, instances in event['instanceId'].items():
            for instance_id in instances:
                response = aws_service.check_rds_state(instance_id, region)
                if response['statusCode'] == '200':
                    notifier.send(msg=f'Successed to stop {instance_id}')
                elif response['statusCode'] == '406':
                    notifier.send(msg=f'Failed to stop {instance_id}')

    # if received from SNS (RDS Event Subscription)
    if event['Records'][0]['Sns']:
        sns = event['Records'][0]['Sns']
        region = json.loads(sns['Message'])['Source ARN'].split(':')[3]
        instance_id = convert.convert_data(sns, context)['source_id']
        aws_service.check_rds_state(instance_id=instance_id, region=region)

        slack_msg = convert.convert_msg_to_json(sns, context)
        notifier.send(msg=slack_msg)
    else:
        raise ValueError(f'Unexpected event occurred: {event}')



