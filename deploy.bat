@echo off
echo Checking AWS CLI installation...
where aws >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo AWS CLI is not installed. Please install it first.
    exit /b 1
)

echo Checking SAM CLI installation...
where sam >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo AWS SAM CLI is not installed. Please install it first.
    exit /b 1
)

echo Building SAM application...
sam build --build-dir build

echo Deploying SAM application...
sam deploy ^
    --stack-name hello-world-app ^
    --region us-east-1 ^
    --capabilities CAPABILITY_IAM ^
    --no-fail-on-empty-changeset ^
    --build-dir build

echo.
echo Deployment completed successfully!
echo.

REM Get the API endpoint, API key, and IAM role
for /f "tokens=*" %%a in ('aws cloudformation describe-stacks --stack-name hello-world-app --query "Stacks[0].Outputs[?OutputKey=='HelloWorldApi'].OutputValue" --output text') do set API_ENDPOINT=%%a
for /f "tokens=*" %%a in ('aws cloudformation describe-stacks --stack-name hello-world-app --query "Stacks[0].Outputs[?OutputKey=='ApiKey'].OutputValue" --output text') do set API_KEY=%%a
for /f "tokens=*" %%a in ('aws cloudformation describe-stacks --stack-name hello-world-app --query "Stacks[0].Outputs[?OutputKey=='TestUserRole'].OutputValue" --output text') do set IAM_ROLE=%%a

echo API Endpoint: %API_ENDPOINT%
echo API Key: %API_KEY%
echo IAM Role ARN: %IAM_ROLE%
echo.
echo To test the API, you can use either method:
echo.
echo 1. Using API Key:
echo curl -X POST %API_ENDPOINT% -H "Content-Type: application/json" -H "x-api-key: %API_KEY%" -d "{\"name\": \"Alice\"}"
echo.
echo 2. Using IAM Authentication:
echo aws apigateway test-invoke-method --rest-api-id %API_ENDPOINT:~8,36% --resource-id {resource-id} --http-method POST --body "{\"name\": \"Alice\"}"
echo.
echo Note: Replace {resource-id} with the actual resource ID from API Gateway console. 