import boto3

EVENT_BUS_NAME = 'fs-event-bus'
EVENT_DETAIL = '{"test":"event"}'
PUT_EVENTS_MAX_ENTRIES = 10

client = boto3.client('events')

def batch_put_events(number_of_events: int):
    for batch_size in calculate_batch_sizes(number_of_events):
        entries = [
            {
                'EventBusName': EVENT_BUS_NAME,
                'Source': 'fs-eventbridge-util-app',
                'DetailType': 'test_event_created',
                'Detail': EVENT_DETAIL
            } for _ in range(batch_size)
        ]
        print(f'Sending batch of {batch_size} events')
        response = client.put_events(
            Entries=entries
        )

        if response['FailedEntryCount'] > 0:
            print(f'Failed entry count: {response["FailedEntryCount"]}')
            failed_entries = [e for e in response['Entries'] if e.get('ErrorCode')]
            print(failed_entries)
    print('Finished sending events')

def calculate_batch_sizes(number_of_events):
    for _ in range(number_of_events, 0, -PUT_EVENTS_MAX_ENTRIES):
        if number_of_events >= PUT_EVENTS_MAX_ENTRIES:
            number_of_events -= 10
            yield PUT_EVENTS_MAX_ENTRIES
        else:
            yield number_of_events


if __name__ == '__main__':
    batch_put_events(300)
