"""
Tests for the Lambda function handler.
"""
import json
from src.lambda_function import handler

def test_lambda_handler_success():
    """Test successful Lambda handler execution."""
    # Test event with name in body
    event = {
        'body': json.dumps({'name': 'Alice'})
    }
    response = handler(event, {})
    
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body['message'] == 'Hello, Alice!'
    assert 'input' in body

def test_lambda_handler_default_name():
    """Test Lambda handler with default name."""
    # Test event with empty body
    event = {
        'body': '{}'
    }
    response = handler(event, {})
    
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body['message'] == 'Hello, World!'

def test_lambda_handler_error():
    """Test Lambda handler error handling."""
    # Test event with invalid JSON
    event = {
        'body': 'invalid json'
    }
    response = handler(event, {})
    
    assert response['statusCode'] == 500
    body = json.loads(response['body'])
    assert body['message'] == 'Internal server error'
    assert 'error' in body 