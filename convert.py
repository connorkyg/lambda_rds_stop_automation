import json


def convert_data(event, context):
    # Get event data from AWS SNS && Convert to JSON
    sns_message = event['Records'][0]['Sns']
    message_content = json.loads(sns_message['Message'])

    event_data = {
        "event_source": message_content.get('Event Source'),
        "event_id_docs": message_content.get('Event ID'),
        "event_time": message_content.get('Event Time'),
        "source_arn": message_content.get('Source ARN'),
        "source_id": message_content.get('Source ID'),
        "event_message": message_content.get('Event Message'),
        "event_id_value": sns_message['MessageAttributes'].get('EventID', {}).get('Value')
    }
    return event_data


def convert_msg_to_json(event, context):
    # Get event data from AWS SNS && Convert to JSON
    sns_message = event['Records'][0]['Sns']
    message_content = json.loads(sns_message['Message'])

    event_source = message_content['Event Source']
    event_id_docs = message_content['Event ID']
    event_time = message_content['Event Time']
    source_arn = message_content['Source ARN']
    source_id = message_content['Source ID']
    event_message = message_content['Event Message']
    event_id_value = sns_message['MessageAttributes']['EventID']['Value']

    # Message you want to send
    message = {
        "attachments": [
            {
                "fallback": "RDS Event Notification",
                "color": "#36a64f",
                "pretext": "RDS Event Notification",
                "title": event_source,
                "title_link": "https://console.aws.amazon.com/rds/",
                "text": "Details about the RDS event",
                "fields": [
                    {
                        "title": "Event Time",
                        "value": event_time,
                        "short": 'true'
                    },
                    {
                        "title": "Source ID",
                        "value": source_id,
                        "short": 'true'
                    },
                    {
                        "title": "Source ARN",
                        "value": source_arn,
                        "short": 'true'
                    },
                    {
                        "title": "Event Message",
                        "value": event_message,
                        "short": 'false'
                    },
                    {
                        "title": "Event ID",
                        "value": event_id_value,
                        "short": 'true'
                    },
                    {
                        "title": "Event ID Detail",
                        "value": event_id_docs,
                        "short": 'true'
                    }
                ],
                "footer": "AWS RDS Service",
                "footer_icon": "https://aws.amazon.com/favicon.ico"
            }
        ]
    }
    return message
