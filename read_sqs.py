import boto3
import json
import hashlib
from botocore.config import Config
import psycopg2
from datetime import datetime

def read_sqs_messages():
    my_config = Config(
        region_name='us-east-1',
        signature_version='v4',
        retries={
            'max_attempts': 10,
            'mode': 'standard'
        },
    )

    sqs = boto3.client(
        'sqs',
        endpoint_url='http://localhost:4566',
        aws_access_key_id='dummy',
        aws_secret_access_key='dummy',
        config=my_config
    )

    queue_url = 'http://localhost:4566/000000000000/login-queue'

    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,
        VisibilityTimeout=30,
        WaitTimeSeconds=0
    )

    messages = response.get('Messages', [])
    return messages

def mask_pii(data):
    if 'device_id' in data:
        data['device_id'] = hashlib.sha256(data['device_id'].encode()).hexdigest()
    if 'ip' in data:
        data['ip'] = hashlib.sha256(data['ip'].encode()).hexdigest()
    return data

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], name + a + '_')
        elif isinstance(x, list):
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def connect_to_postgres():
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='qaz123',
        host='localhost',
        port='5432'
    )
    return conn

def insert_into_postgres(conn, data):
    columns = data.keys()
    # Define the order of columns in the table
    columns_order = ['user_id', 'device_type', 'ip', 'device_id', 'locale', 'app_version']
    table_columns = ['user_id', 'device_type', 'masked_ip', 'masked_device_id', 'locale', 'app_version', 'create_date']
    
    # Arrange the values in the order of the columns in the table
    values = [data[column] for column in columns_order]
    
    # Add current date
    current_date = datetime.today().date().strftime('%Y-%m-%d')
    values.append(current_date)
    
    # Construct INSERT statement with column names
    insert_statement = f"INSERT INTO user_logins ({', '.join(table_columns)}) VALUES ({', '.join(['%s'] * len(values))})"

    with conn.cursor() as cursor:
        cursor.execute(insert_statement, values)
        conn.commit()

if __name__ == "__main__":
    conn = connect_to_postgres()
    messages = read_sqs_messages()
    for message in messages:
        body = message['Body']
        try:
            parsed_data = json.loads(body)
            masked_data = mask_pii(parsed_data)
            flattened_data = flatten_json(masked_data)
            insert_into_postgres(conn, flattened_data)
            print("Data inserted successfully:", flattened_data)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
        except Exception as e:
            print(f"Error processing data: {e}")
    conn.close()
