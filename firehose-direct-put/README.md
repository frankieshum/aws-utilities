# Firehose direct PUT utility app

## Set up

Create a python virtual env:
`python -m venv .venv`

Activate virtual env:
`source .venv/Scripts/activate`

Install pip packages from requirements.txt:
`pip install -r requirements.txt`

(optional) Tweak event.json to specify event shape

Create .env file with env vars:
- FIREHOSE_STREAM_NAME (required; the name of the stream)
- NUMBER_OF_RECORDS (required; the number of records to send per app invocation)
- AWS_PROFILE (optional; the AWS profile to use for connecting to Firehose)

## Run
Make sure you're logged into AWS

Run: `python main.py`