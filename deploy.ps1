# Deployment script for AWS SAM application

# Check if AWS CLI is installed
if (-not (Get-Command aws -ErrorAction SilentlyContinue)) {
    Write-Error "AWS CLI is not installed. Please install it first."
    exit 1
}

# Check if SAM CLI is installed
if (-not (Get-Command sam -ErrorAction SilentlyContinue)) {
    Write-Error "AWS SAM CLI is not installed. Please install it first."
    exit 1
}

# Set environment variables
$env:AWS_SAM_BUILD_DIR = "build"
$env:STACK_NAME = "hello-world-app"
$env:REGION = "us-east-1"  # Change this to your preferred region

# Create build directory if it doesn't exist
if (-not (Test-Path $env:AWS_SAM_BUILD_DIR)) {
    New-Item -ItemType Directory -Path $env:AWS_SAM_BUILD_DIR
}

Write-Host "Building SAM application..."
sam build --build-dir $env:AWS_SAM_BUILD_DIR

Write-Host "Deploying SAM application..."
sam deploy `
    --stack-name $env:STACK_NAME `
    --region $env:REGION `
    --capabilities CAPABILITY_IAM `
    --no-fail-on-empty-changeset `
    --build-dir $env:AWS_SAM_BUILD_DIR

# Get the API endpoint
$apiEndpoint = aws cloudformation describe-stacks `
    --stack-name $env:STACK_NAME `
    --query "Stacks[0].Outputs[?OutputKey=='HelloWorldApi'].OutputValue" `
    --output text

Write-Host "`nDeployment completed successfully!"
Write-Host "API Endpoint: $apiEndpoint"
Write-Host "`nTest the API with:"
Write-Host "curl -X POST $apiEndpoint -H 'Content-Type: application/json' -d '{\"name\": \"Alice\"}'" 