zip -r lambda_code.zip ./* -x update-code.sh
aws lambda update-function-code --function-name devops-task-lambda-function --zip-file fileb://lambda_code.zip --region eu-west-2
rm -rvf lambda_code.zip
