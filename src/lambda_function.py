import os
import json
import httpx
from openai import OpenAI

def get_openai_client():
    api_key = "placeholder" # Set in Lambda environment variables
    proxy = os.environ.get("HTTPS_PROXY")
    if proxy:
        # Use http_client as required by openai v1.x
        http_client = httpx.Client(proxies=proxy)
        return OpenAI(api_key=api_key, http_client=http_client)
    return OpenAI(api_key=api_key)

client = get_openai_client()

def handler(event, context):
    try:
        raw_body = event.get('body', '{}')

        # Fix: ensure raw_body is a string before parsing
        if isinstance(raw_body, str):
            body = json.loads(raw_body)
        elif isinstance(raw_body, dict):
            body = raw_body
        else:
            body = {}

        message = body.get('message', '').strip()

        if not message:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "Message is required"})
            }

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}]
        )

        chat_response = response.choices[0].message.content

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"response": chat_response})
        }

    except Exception as exc:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(exc)})
        }
