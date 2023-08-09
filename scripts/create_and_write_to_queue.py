import json
import gzip
import localstack_client.session as boto3

QUEUE_NAME = "login-queue"

def send_messages():
    # Initialize an SQS client
    sqs = boto3.client("sqs")

    # Create a new SQS queue
    queue_url = sqs.create_queue(QueueName=QUEUE_NAME)["QueueUrl"]
    print(f"queue_url: [{queue_url}]")

    # Open and read the gzipped JSON file
    with gzip.open("/tmp/data/sample_data.json.gz", "r") as f:
        data = json.load(f)

    # Ensure that the loaded data contains 100 records
    assert len(data) == 100

    # Send each record as a message to the SQS queue
    for record in data:
        sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(record))

    return

def main():
    # Call the send_messages function to send records to SQS
    send_messages()

# Execute the main function if the script is run directly
if __name__ == "__main__":
    main()
