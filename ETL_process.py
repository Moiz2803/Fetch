import boto3
import json
import base64
import psycopg2
import configparser
import argparse
import sys
from datetime import datetime

class ETL_Process():
    """Class for Executing ETL Operations"""

    def __init__(self, endpoint_url, queue_name, wait_time, max_messages):
        """Constructor for Acquiring Postgres Credentials"""

        # Initialize the configuration parser
        config = configparser.ConfigParser()

        # Read the configuration file
        config.read('postgres.ini')

        # Retrieve configuration details
        self.__username = config.get('postgres', 'postgres')
        self.__password = config.get('postgres', 'postgres')
        self.__host = config.get('postgres', 'host')
        self.__database = config.get('postgres', 'database')

        # Obtain argument values
        self.__endpoint_url = endpoint_url
        self.__queue_name = queue_name
        self.__wait_time = wait_time
        self.__max_messages = max_messages

    def base64_encode(self, string_parameter, action="encode"):
        """Function for Base64 Encoding/Decoding"""

        # Determine if the action is encoding or decoding
        if action == "encode":
            ascii_string = string_parameter.encode('ascii')
            encoded_string = base64.b64encode(ascii_string).decode('utf-8')
            return encoded_string
        elif action == "decode":
            decoded_string = base64.b64decode(string_parameter).decode('utf-8')
            return decoded_string

    def get_messages(self):
        """Function to Retrieve Messages from SQS Queue"""

        # Initialize SQS Client
        sqs_client = boto3.client("sqs", endpoint_url=self.__endpoint_url)

        # Receive messages from the queue
        try:
            response = sqs_client.receive_message(
                QueueUrl=self.__endpoint_url + '/' + self.__queue_name,
                MaxNumberOfMessages=self.__max_messages,
                WaitTimeSeconds=self.__wait_time
            )
        except Exception as exceptions:
            # Print error encountered during parameter parsing
            print("Error - " + str(exceptions))

            # Exit the program
            sys.exit()

        # Retrieve messages from SQS
        messages = response['Messages']
        
        # Return the messages
        return messages

    def transform_data(self, messages):
        """Function for PII Data Transformation"""

        # Initialize an empty list for messages
        message_list = []

        try:
            # Check if the "messages" list is empty
            if len(messages) == 0:
                # Raise an IndexError
                raise IndexError("Message list is empty")
                
        except IndexError as index_error:
            # Print that the message list is empty
            print("Error - " + str(index_error))

            # Exit the program
            sys.exit()

        # Initialize a message counter variable
        message_count = 0

        # Iterate through the messages
        for message in messages:
            # Increment the message counter
            message_count += 1

            # Retrieve the "Body" of the message in JSON/Dictionary format
            message_body = json.loads(message['Body'])

            # Retrieve the "ip" and "device_id" from the message
            try:
                ip = message_body['ip']
                device_id = message_body['device_id']
            except Exception as exception:
                # Print that the message is invalid
                print("Error - Message " + str(message_count) + " is invalid - " + str(exception) + " is not available in the queue")

                # Move to the next message
                continue

            # Encode "ip" and "device_id"
            base64_ip = self.base64_encode(ip)
            base64_device_id = self.base64_encode(device_id)

            # Replace "ip" and "device_id" with the encoded values
            message_body['ip'] = base64_ip
            message_body['device_id'] = base64_device_id
            
            # Append data to the message list
            message_list.append(message_body)

        # Return the message list
        return message_list

    def load_data_postgre(self, message_list):
        """Function for Loading Data into Postgres"""

        # Check if the "message_list" is empty
        try:
            if len(message_list) == 0:
                # Raise a Type Error
                raise TypeError
        except TypeError as type_error:
            # Print that the "message_list" is empty
            print("Error - " + str(type_error))

            # Exit the program
            sys.exit()

        # Establish a connection to Postgres
        postgres_conn = psycopg2.connect(
            host=self.base64_encode(self.__host, action="decode"),
            database=self.base64_encode(self.__database, action="decode"),
            user=self.base64_encode(self.__username, action="decode"),
            password=self.base64_encode(self.__password, action="decode")
        )

        # Create a Cursor
        cursor = postgres_conn.cursor()

        # Iterate through the messages
        for message_json in message_list:
            # Replace 'None Type' values with 'None' string
            message_json['locale'] = 'None' if message_json['locale'] == None else message_json['locale']
            # Set 'create_date' field as the current date
            message_json['create_date'] = datetime.now().strftime("%Y-%m-%d")

            # Convert dictionary values to a list
            values = list(message_json.values())

            # Execute the insert query
            cursor.execute("INSERT INTO user_logins (user_id, app_version, device_type, masked_ip, locale, masked_device_id, create_date) VALUES (%s, %s, %s, %s, %s, %s, %s)", values)

            # Commit data to Postgres
            postgres_conn.commit()

        # Close the connection to Postgres
        postgres_conn.close()

        # Return from the function
        return

def main():
    """Main Function"""

    # Initialize the argument parser
    parser = argparse.ArgumentParser(
        prog="Extract Transform Load - Process",
        description="Program extracts data from SQS queue - \
                     Transforms PIIs in the data - \
                     Loads the processed data into Postgres",
        epilog="Please raise an issue for code modifications"
    )

    # Add arguments
    parser.add_argument('-e', '--endpoint-url
