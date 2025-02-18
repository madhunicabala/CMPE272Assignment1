Objective 
	To create a serverless web application using AWS Lambda and DynamoDB.

Requirements
1.	Maintain a student record database using DynamoDB having student_id as key
2.	Perform CRUD operations to read, write, modify and delete entries in the student record database using AWS lambda function.
3.	Deploy and Test Application in AWS environment.

Setup/Application prerequisites
•	AWS Lambda for serverless compute
•	DynamoDB for data storage
•	API Gateway for REST API endpoints
•	AWS IAM for security and permissions

Setting up AWS Account and Environment 
i.	Create an account in AWS https://aws.amazon.com/console/.

ii.	Create a database using dynamoDB application in AWS. For this use case, create a table named StudentRecords with the primary key  n          (aka partition key) as student_id. Please refer to section 1.1 for dynamo DB table outputs.

iii.	Create a AWS lambda function by choosing appropriate architecture (x86 / arm) and preferred language as python 3.x. Here the backend         Lambda function parses the incoming request data and responds to the client.

iv.	Create and set the execution role to inherit appropriate permissions / policies from AWS policy templates. This will create a simple         lambda function which can be customised for our use case requirements.

v.	Create a REST API gateway, set the API endpoint as regional and then you create a resource under the path / and keep CORS enabled.           Typically, API resources are organized in a resource tree according to the application logic.

vi.	Create methods such as GET/POST/PUT, choose create method under /<<resource_name>> , choose method type and turn on aws
        lambda proxy integration.

vii.	In order to deploy API, choose/ create new stage and choose deploy. Make a note of the API’s invoke URL.

viii.	Use either the CURL command or Postman to test the API.
