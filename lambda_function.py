import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
# Initilaise table to StudentRecords Table
dynamodb_table = dynamodb.Table('StudentRecords')

# Define API paths to execute GET / POST / DELETE methods accordingly
student_path = '/student'
students_path = '/students'

def lambda_handler(event, context):
    try:
        http_method = event.get('httpMethod')
        path = event.get('path')
        query_params = event.get('queryStringParameters', {})

        # GET request for a single student
        if http_method == 'GET' and path == student_path:
            if 'student_id' in query_params:
                student_id = query_params['student_id']
                response = dynamodb_table.get_item(Key={'student_id': student_id})

                # Check if student exists
                if 'Item' in response:
                    return {
                        'statusCode': 200,
                        'body': json.dumps(response['Item'])
                    }
                else:
                    return {
                        'statusCode': 404,
                        'body': json.dumps({'error': 'Student not found'})
                    }
            else:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Missing student_id parameter'})
                }
        elif http_method == 'GET' and path == students_path:
            # GET request for all students in the record
            response = dynamodb_table.scan()
            items = response.get('Items', [])
            return {
                'statusCode': 200,
                'body': json.dumps(items)
            }
        elif http_method == 'POST' and path == student_path:
             # POST request to add a new student
            if not event.get('body'):
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Request body is missing'})
                }
            request_body = json.loads(event['body'])
            student_id = str(request_body.get('student_id', ''))
            dynamodb_table.put_item(
                Item={
                     'student_id': student_id,
                     'student_name': request_body.get('student_name', ''),
                     'student_course': request_body.get('student_course', ''),
                     'student_email': request_body.get('student_email', '')
                }
            )
            return {
                'statusCode': 200,
                'body': json.dumps({
                'message': 'Student added successfully',
                'student': request_body  # Return original request body
                 })
            }
        elif http_method == 'PATCH' and path == student_path:
            # PUT request to update a student
            if not event.get('body'):
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Request body is missing'})
                }
            request_body = json.loads(event['body'])
            student_id = str(request_body.get('student_id', ''))
            update_key = request_body.get('update_key')
            update_value = request_body.get('update_value')
            if not all([student_id, update_key, update_value]):
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Missing required fields'})
                }
            response = dynamodb_table.update_item(
                Key={'student_id': student_id},
                UpdateExpression=f'SET {update_key} = :value',
                ExpressionAttributeValues={':value': update_value},
                ReturnValues='UPDATED_NEW'
            )

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Student record updated successfully',
                    'updated_attributes': response.get('Attributes', {})
                })
            }
        elif http_method == 'PUT' and path == student_path:
            # PUT request to update a student
            if not event.get('body'):
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Request body is missing'})
                }
            request_body = json.loads(event['body'])
            student_id = str(request_body.get('student_id', ''))
            if not student_id:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'student_id is required'})
                }
            response = dynamodb_table.update_item(
                Key={'student_id': student_id},
                UpdateExpression='SET student_name = :name, student_course = :course, student_email = :email',
                ExpressionAttributeValues={
                    ':name': request_body.get('student_name', ''),
                    ':course': request_body.get('student_course', ''),
                    ':email': request_body.get('student_email', '')
                },
                ReturnValues='UPDATED_NEW'
            )
            return {
                'statusCode': 200,
                'body': json.dumps({
                'message': 'Student record updated successfully',
                'updated_attributes': response.get('Attributes', {})
                })
            }
        # DELETE request to remove a student
        elif http_method == 'DELETE' and path == student_path:
            request_body = json.loads(event['body'])
            # Ensure request body exists
            if not event.get('body'):
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Request body is missing'})
                } 
            request_body = json.loads(event['body'])
            student_id = request_body.get('student_id')
            if not student_id:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'student_id is required'})
                }
            response = dynamodb_table.delete_item(
                Key={'student_id': student_id},
                ReturnValues='ALL_OLD'
            )
            return {
                'statusCode': 200,
                'body': json.dumps({
                'message': 'Student record deleted successfully',
                'deleted_item': response.get('Attributes', {})
                })
            }

        # Default response for unknown routes
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Invalid request'})
            }

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }
