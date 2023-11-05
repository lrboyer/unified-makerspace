import json
import boto3
from boto3.dynamodb.conditions import Key
import os
import time
from typing import Tuple


class SubmitQuizFunction():
    """
    This class wraps the function of the lambda so we can more easily test
    it with moto. In production, we will continue to pass the stood-up
    dynamodb table to the handler itself. However, when initializing this class,
    we can choose to instead initialize it with a mocked version of the
    dynamodb table.
    """

    def __init__(self, quiz_list_table, quiz_progress_table, users_table, dynamodbclient):
        if dynamodbclient is None:
            self.dynamodbclient = boto3.client('dynamodb')
        else:
            self.dynamodbclient = dynamodbclient

        self.USERS_TABLE_NAME = os.environ["USERS_TABLE_NAME"]
        if users_table is None:
            dynamodbresource = boto3.resource('dynamodb')
            self.users = dynamodbresource.Table(self.USERS_TABLE_NAME)
        else:
            self.users = users_table

        self.QUIZ_LIST_TABLE_NAME = os.environ["QUIZ_LIST_TABLE_NAME"]
        if quiz_list_table is None:
            dynamodbresource = boto3.resource('dynamodb')
            self.quiz_list = dynamodbresource.Table(self.QUIZ_LIST_TABLE_NAME)
        else:
            self.quiz_list = quiz_list_table

        self.QUIZ_PROGRESS_TABLE_NAME = os.environ["QUIZ_PROGRESS_TABLE_NAME"]
        if quiz_progress_table is None:
            dynamodbresource = boto3.resource('dynamodb')
            self.quiz_progress = dynamodbresource.Table(
                self.QUIZ_PROGRESS_TABLE_NAME)
        else:
            self.quiz_progress = quiz_progress_table

    def does_quiz_exist(self, quiz_id):
        """
            true if the quiz is in the quiz list
        """
        quiz_list_response = self.quiz_list.query(
            KeyConditionExpression=Key('quiz_id').eq(quiz_id)
        )
        return quiz_list_response['Count'] != 0

    def get_username(self, email):
        """
            Will get an email passed in ex: "lrboyer@clemson.edu"

            Needs to return the username

            input: a string like: "lrboyer@clemson.edu"
            return: a string of just the username: "lrboyer"
        """
        return None

    def get_quiz_state(self, score):
        """
            Will get a score ex: "2 / 10" or "4 / 4"

            Needs to return 1 for all correct ("5 / 5") or 0 for not all correct ("9 / 10")

            input: a string like of the quiz score "9 / 10" or "3 / 3"
            return: 1 if all questions are correct and a 0 if otherwise
        """
        return None

    def add_quiz_info(self, quiz_info):
        """
            Steps for adding quiz info:
                1. Check if quiz_id exist in quiz_list
                    - if not -> add quiz_id to quiz_list
                2. Insert quiz_info into quiz_progress_table
        """

        if not self.does_quiz_exist(quiz_info['quiz_id']):
            quiz_list_response = self.quiz_list.put_item(
                Item={
                    'quiz_id': quiz_info['quiz_id']
                }
            )

        timestamp = int(time.time())
        username = self.get_username(quiz_info['email'])
        state = self.get_quiz_state(quiz_info['score'])

        # dict for entry into the quiz_progress table
        quiz_progress_item = {
            'quiz_id': quiz_info['quiz_id'],
            'username': username,
            'timestamp': timestamp,
            'state': state
        }

        quiz_progress_table_response = self.quiz_progress.put_item(
            Item=quiz_progress_item
        )

        return quiz_progress_table_response['ResponseMetadata']['HTTPStatusCode']

    def handle_submit_quiz_request(self, request, context):
        HEADERS = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': os.environ["DOMAIN_NAME"],
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }
        if (request is None):
            return {
                'headers': HEADERS,
                'statusCode': 400,
                'body': json.dumps({
                    "Message": "Failed to provide parameters"
                })
            }

        # Get all of the quiz information from the json file
        quiz_info = json.loads(request["body"])
        # Call Function
        response = self.add_quiz_info(quiz_info)
        # Send response
        return {
            'headers': HEADERS,
            'statusCode': response
        }


submit_quiz_function = SubmitQuizFunction(None, None, None, None)


def handler(request, context):
    # Register quiz information from the makerspace/register console
    # Since this will be hit in prod, it will go ahead and hit our prod
    # dynamodb table
    return submit_quiz_function.handle_submit_quiz_request(
        request, context)
