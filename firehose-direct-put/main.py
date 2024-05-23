import boto3
import os
from dotenv import load_dotenv

load_dotenv()

FIREHOSE_STREAM_NAME = os.getenv('FIREHOSE_STREAM_NAME')
NUMBER_OF_RECORDS = int(os.getenv('NUMBER_OF_RECORDS'))
AWS_PROFILE = os.getenv('AWS_PROFILE')

if AWS_PROFILE:
    boto3.setup_default_session(profile_name=AWS_PROFILE)

firehose = boto3.client('firehose')

def put_records_to_firehose():
    with open('event.json') as file:
        event_json = file.read()
            
    records = [event_json.encode()]*NUMBER_OF_RECORDS
    
    print(f'Putting batch of {len(records)} records to Firehose')
    
    response = firehose.put_record_batch(
        DeliveryStreamName=FIREHOSE_STREAM_NAME,
        Records=[{'Data': record} for record in records]
    )
    
    if response['FailedPutCount'] > 0:
        error_responses = [record_response
                            for record_response
                            in response["RequestResponses"]
                            if 'ErrorCode' in record_response]
        print(f'Failed to put {response["FailedPutCount"]} records to Firehose. Failed entries: {error_responses}')
        
    print(f'Finished putting batch of {len(records)} records to Firehose')

if __name__ == '__main__':
    put_records_to_firehose()
