from quiz.quiz import QuizFunction
from responses import mock
import pytest
import os
import json
import boto3
from moto import mock_dynamodb2

from test_utils.test_functions import *

test_submit_quiz_pass = {
    "httpMethod": "POST",
    "body": json.dumps({
        "quiz_id": "3dPrinter",
        "username": "smjohn492",
        "email": "smjohn492@clemson.edu",
        "score": "10 / 10",
    })
}

test_submit_quiz_fail_1 = {
    "httpMethod": "POST",
    "body": json.dumps({
        "quiz_id": "3dPrinter",
        "username": "smjohn492",
        "email": "smjohn492@clemson.edu",
        "score": "8 / 10",
    })
}

test_submit_quiz_fail_2 = {
    "httpMethod": "POST",
    "body": json.dumps({
        "quiz_id": "3dPrinter",
        "username": "leejohn",
        "email": "leejohn@clemson.edu",
        "score": "4 / 10",
    })
}


@mock_dynamodb2
def test_submit_quiz_new_id_pass():
    client = create_dynamodb_client()
    quiz_list_table = create_test_quiz_list_table(client)
    quiz_progress_table = create_test_quiz_progress_table(client)

    response = QuizFunction(quiz_list_table, quiz_progress_table, client).handle_quiz_request(test_submit_quiz_pass, None)
    assert response['statusCode'] == 200
    
@mock_dynamodb2
def test_submit_quiz_existing_id_fail():
    client = create_dynamodb_client()
    quiz_list_table = create_test_quiz_list_table(client)
    quiz_progress_table = create_test_quiz_progress_table(client)

    response1 = QuizFunction(quiz_list_table, quiz_progress_table, client).handle_quiz_request(test_submit_quiz_fail_1, None)
    assert response1['statusCode'] == 200
    
    response2 = QuizFunction(quiz_list_table, quiz_progress_table, client).handle_quiz_request(test_submit_quiz_fail_2, None)
    assert response2['statusCode'] == 200
    
    
#NEED TO CREATE TEST CASES FOR TESTING THE GET QUIZZES