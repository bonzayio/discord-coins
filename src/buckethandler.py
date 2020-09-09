import boto3
from botocore.errorfactory import ClientError
from botocore.config import Config

import os
import json
from datetime import datetime


def get_timestamp_now() -> int:
    """Gets a timestamp of the current time.

    Returns:
        int: Timestamp
    """
    now = datetime.now()

    return int(datetime.timestamp(now))


class BucketHandler:
    def __init__(self):
        self._setup_s3()

    def _setup_s3(self) -> None:
        standard_config = Config(region_name='us-east-1',
                                 retries={
                                     'max_attempts': 10,
                                     'mode': 'standard'
                                 })

        if not os.path.isfile('configuration/aws.json'):
            print('[ERROR] Couldn\'t locate the aws.json file. Exitting.')
            exit()

        # get access keys
        with open('configuration/aws.json', 'r') as json_file:
            data = json.load(json_file)
        self.bucket_name = data['bucket_name']
        if self.bucket_name == "":
            print('[ERROR] No bucket name specified in the aws.json file. Exitting.')
            exit()

        aws_access_key_id = data['aws_access_key_id']
        aws_secret_access_key = data['aws_secret_access_key']

        self.s3 = boto3.resource(
            's3',
            config=standard_config,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    def download_json(self,
                      filename_to_save: str,
                      target_file_name: str = None) -> None:
        """Downloads a json.
        Raises a `ClientError` if file not found.

        Args:
            filename_to_save (str): Name of the file (on your PC) you want to save
            target_file_name (str, optional): Name you want the file to be saved as (in the AWS bucket). Defaults to `filename_to_save`.
        """
        if target_file_name is None:
            target_file_name = filename_to_save
        self.s3.Object(
            self.bucket_name,
            filename_to_save).download_file(Filename=target_file_name)

    def upload_file(self,
                    filename_to_save: str,
                    target_file_name: str = None) -> None:
        """Uploads a file. If a file of the same name already exists, overwrites it.

        Args:
            filename_to_save (str): Name of the file (on your PC) you want to save
            target_file_name (str, optional): Name you want the file to be saved as (in the AWS bucket). Defaults to `filename_to_save`.
        """
        if target_file_name is None:
            target_file_name = filename_to_save

        self.s3.Object(self.bucket_name,
                       target_file_name).upload_file(Filename=filename_to_save)

    def add_coins(self, filename: str, coin_count: int) -> int:
        """Adds coins to a filename specified and logs the transaction.
        Raises a `ClientError` if file not found.

        Args:
            filename (str): Expected `coins/<USER_ID>`
            coin_count (int): How many coins to add

        Returns:
            int: Number of coins an user has after adding.
        """

        # make sure file has a dot
        if '.' not in filename:
            print(
                f'[INFO] [BUCKET] File {filename} doesnt end with any filetype. Adding JSON to it!'
            )
            filename = filename.strip() + '.json'
        # downloading and reading the data
        data = {}
        total_coins = 0
        transactions = []

        try:
            self.download_json(filename, 'temp.json')

            with open('temp.json') as json_file:
                data = json.load(json_file)
            total_coins = data['coin_count']
            transactions = data['transactions']
        except ClientError:
            print(f'[INFO] [BUCKET] File {filename} not found. Creating it!')

        # adding coins to current count
        total_coins += coin_count
        transactions.append({str(get_timestamp_now()): f'+{coin_count}'})

        # overwriting values
        data['coin_count'] = total_coins
        data['transactions'] = transactions

        # saving data to temp so we can upload it
        with open('temp.json', 'w') as outfile:
            json.dump(data, outfile)
        self.upload_file('temp.json', filename)
        return total_coins

    def remove_coins(self, filename: str, coin_count: int) -> int:
        """Removes coins from a filename specified and logs the transaction.
        Raises a `ClientError` if file not found.

        Args:
            filename (str): Expected `coins/<USER_ID>`
            coin_count (int): How many coins to remove
        
        Returns:
            int: Number of coins an user has after removing.
        """
        # downloading and reading the data
        self.download_json(filename, 'temp.json')
        with open('temp.json') as json_file:
            data = json.load(json_file)
        total_coins: int = data['coin_count']
        transactions: list = data['transactions']

        # adding coins to current count
        total_coins -= coin_count
        transactions.append({str(get_timestamp_now()): f'-{coin_count}'})

        # overwriting values
        data['coin_count'] = total_coins
        data['transactions'] = transactions

        # saving data to temp so we can upload it
        with open('temp.json', 'w') as outfile:
            json.dump(data, outfile)
        self.upload_file('temp.json', filename)
        return total_coins

    def get_coins(self, filename: str) -> int:
        """Gets the current coin amount in the file specified.

        Args:
            filename (str): Expected `coins/<USER_ID>`

        Returns:
            int: Number of coins an user has
        """
        try:
            self.download_json(filename, 'temp.json')
        except ClientError:
            return 0
        with open('temp.json') as json_file:
            data = json.load(json_file)
        total_coins: int = data['coin_count']
        return total_coins
