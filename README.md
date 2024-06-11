# ETL-SQS-PSQL
 ETL off a SQS Queue

 This application will read the data from AWS SQS Queue and Transform the data to Mask PII information and write it to Postgres Database. 

 ## Steps to execute this application
 ### Install below required softwares or applications to run this applications
 1. Install Docker
 2. Install Docker Compose
 3. Install Postgres Database
 4. Install awscli-local

### Execute the application files as below:
1. Clone the repository into your local
2. Open Terminal
3. Go to the project directory
4. Run docker-compose up -d in CLI
5. Run awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue to read JSON data from AWS SQS Queue.
6. Run python script using command: python create-table.py  - This script will create the postgres user_logins table.
7. Run python script using command: python read_sqs.py      - This script would read the data from queue and transform the data to mask PII information and load the data into Postgres table
8. Finally, Run Python Script to retrevie the data from Postgres using command: python Select-table.py

### Key Pointers:
1. How will you read messages from the queue?
 To read messages from the queue, I have used the boto3 library, which is the AWS SDK for Python. Specifically, we will use the boto3.client to create an SQS client that can connect to the SQS service provided by Localstack.

2. What type of data structures should be used?
   Dictionaries, Lists and Tuples are used to build this application.
   > Dictionaries have been used to parsing and manupulating JSON messages.
   > Lists have been used to sort the order for database operations.
   > Tuples was used to fetches the rows from database.
   
3. How will you mask the PII data so that duplicate values can be identified?
   I used a consistent hashing method to mask PII data in a way that allows for the identification of duplicate values. For this application, I used SHA-256 hash function, which ensures that the same input will always produce the same output, allowing us to identify duplicate values based on their hash values. 
