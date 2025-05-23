# Python Project

This is a Python project template with a basic structure for development and AWS SAM deployment, featuring ChatGPT integration.

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
```

2. Activate the virtual environment:

- Windows:

```bash
.\venv\Scripts\activate
```

- Unix/MacOS:

```bash
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Project Structure

- `src/`: Contains the main source code
- `tests/`: Contains unit tests
- `requirements.txt`: Lists project dependencies
- `template.yaml`: AWS SAM template
- `sam-requirements.txt`: Dependencies for SAM deployment
- `deploy.bat`: Windows batch deployment script
- `deploy.ps1`: PowerShell deployment script
- `samconfig.toml`: SAM deployment configuration

## Development

- Run tests: `pytest`
- Format code: `black src tests`
- Lint code: `flake8 src tests`

## AWS SAM Deployment

1. Install required tools:

```bash
# Install AWS CLI
pip install awscli

# Install AWS SAM CLI
pip install aws-sam-cli
```

2. Configure AWS credentials:

```bash
aws configure
```

3. Deploy using one of these methods:

### Option 1: Using Batch File (Recommended for Windows)

```bash
deploy.bat
```

### Option 2: Using PowerShell

If you want to use the PowerShell script, you'll need to adjust the execution policy first:

```powershell
# Run PowerShell as Administrator and execute:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\deploy.ps1
```

### Option 3: Manual Deployment

```bash
# Build the application
sam build

# Deploy the application (you'll be prompted for the OpenAI API key)
sam deploy --guided
```

## API Authentication

The API supports two authentication methods:

### 1. API Key Authentication

After deployment, you'll receive:

- API Endpoint URL
- API Key

Include the API key in the `x-api-key` header:

```bash
curl -X POST {API_ENDPOINT} \
  -H "Content-Type: application/json" \
  -H "x-api-key: {API_KEY}" \
  -d '{"message": "What is the capital of France?"}'
```

### 2. IAM Authentication

The API also supports IAM authentication. After deployment, you'll receive:

- IAM Role ARN for testing

To use IAM authentication:

1. Configure AWS credentials:

```bash
aws configure
```

2. Make a signed request using AWS CLI:

```bash
aws apigateway test-invoke-method \
  --rest-api-id {api-id} \
  --resource-id {resource-id} \
  --http-method POST \
  --body '{"message": "What is the capital of France?"}'
```

## ChatGPT Integration

The Lambda function integrates with ChatGPT using the OpenAI API. Features:

- Uses GPT-3.5-turbo model
- Configurable temperature (0.7 by default)
- Maximum 500 tokens per response
- System prompt set to "You are a helpful assistant"

To use the API:

1. Send a POST request with a JSON body containing a "message" field
2. The response will contain ChatGPT's response in the "response" field

Example request:

```bash
curl -X POST {API_ENDPOINT} \
  -H "Content-Type: application/json" \
  -H "x-api-key: {API_KEY}" \
  -d '{"message": "What is the capital of France?"}'
```

Example response:

```json
{
  "response": "The capital of France is Paris.",
  "input": "What is the capital of France?"
}
```

## Local Testing with SAM

1. Start the API locally:

```bash
sam local start-api
```

2. Test the local API:

```bash
curl -X POST http://127.0.0.1:3000/hello \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the capital of France?"}'
```

## Deployment Configuration

The deployment is configured using:

- `samconfig.toml`: Contains deployment settings
- `deploy.bat`: Windows batch deployment script
- `deploy.ps1`: PowerShell deployment script

You can modify these files to:

- Change the stack name
- Update the AWS region
- Modify deployment parameters
- Add additional deployment options
