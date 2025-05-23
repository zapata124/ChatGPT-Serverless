"""
AWS Lambda function handler for ChatGPT integration.
"""
import json
import os
from typing import Any, Dict
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
import openai

# Initialize logger
logger = Logger()

# Initialize OpenAI client
openai.api_key = os.environ.get('OPENAI_API_KEY')

@logger.inject_lambda_context
def handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """
    Lambda function handler for ChatGPT integration.
    
    Args:
        event (Dict[str, Any]): Lambda event data
        context (LambdaContext): Lambda context object
        
    Returns:
        Dict[str, Any]: Response containing ChatGPT's response
    """
    try:
        # Log the incoming event
        logger.info("Received event", extra={"event": event})
        
        # Extract message from event body
        body = event.get('body', '{}')
        if isinstance(body, str):
            body = json.loads(body)
        
        message = body.get('message', '')
        if not message:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Message is required'
                })
            }
        
        # Call ChatGPT
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        # Extract the response
        chat_response = response.choices[0].message.content
        
        # Create response
        response = {
            'statusCode': 200,
            'body': json.dumps({
                'response': chat_response,
                'input': message
            })
        }
        
        logger.info("Sending response", extra={"response": response})
        return response
        
    except Exception as e:
        logger.exception("Error processing request")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        } 