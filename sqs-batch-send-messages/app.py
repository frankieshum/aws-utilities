import boto3
import json
import sys
import uuid

MESSAGE_BODY = '{"test":"message"}'
QUEUE_URL = 'https://sqs.{region}.amazonaws.com/{account_id}/{queue_name}'
SEND_MESSAGE_BATCH_MAX_MESSAGES = 10

client = boto3.client('sqs')

def batch_send_messages(number_of_messages: int):
    for batch_size in calculate_batch_sizes(number_of_messages):
        entries = [
            {
                'Id': str(uuid.uuid4()),
                'MessageBody': MESSAGE_BODY
            } for _ in range(batch_size)
        ]
        print(f'Sending batch of {batch_size} messages')
        response = client.send_message_batch(
            QueueUrl=QUEUE_URL,
            Entries=entries
        )

        if 'Failed' in response:
            print(f'Failed to send {len(response["Failed"])} messages:')
            for failed_entry in response['Failed']:
                print(json.dumps(failed_entry, indent=4))
            
    print('Finished sending messages')

def calculate_batch_sizes(number_of_messages):
    for _ in range(number_of_messages, 0, -SEND_MESSAGE_BATCH_MAX_MESSAGES):
        if number_of_messages >= SEND_MESSAGE_BATCH_MAX_MESSAGES:
            number_of_messages -= 10
            yield SEND_MESSAGE_BATCH_MAX_MESSAGES
        else:
            yield number_of_messages

if __name__ == '__main__':
    args = sys.argv
    print(args)
    if len(args) > 1 and not args[1].isdigit():
        print('Number of messages to send must be numeric')
        sys.exit()
    batch_send_messages(int(args[1]) if len(args) > 1 else 1)
