import requests
import json


class SlackNotifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def _validate_message(self, msg):
        if not msg.get('attachments'):
            raise ValueError('The message is missing required fields.')

    def send(self, msg, additional_headers=None):
        try:
            # Validate the message structure.
            self._validate_message(msg)

            headers = {'Content-Type': 'application/json'}
            if additional_headers:
                headers.update(additional_headers)

            response = requests.post(
                self.webhook_url,
                data=json.dumps(msg),
                headers=headers,
                timeout=10  # setting a timeout to prevent hanging indefinitely
            )
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code

            return {
                'statusCode': 200,
                'body': json.dumps('Message sent successfully!')
            }
        except requests.exceptions.RequestException as e:
            raise ValueError(f'Error sending message to Slack: {str(e)}')

# Usage:
# notifier = SlackNotifier('YOUR_WEBHOOK_URL')
# notifier.send(your_message_dict)
