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
#### 1. How will you read messages from the queue?

A: To read messages from the queue, I have used the boto3 library, which is the AWS SDK for Python. Specifically, we will use the boto3.client to create an SQS client that can connect to the SQS service provided by Localstack.

#### 2. What type of data structures should be used?
   
A: Dictionaries, Lists and Tuples are used to build this application.
   * Dictionaries have been used to parsing and manupulating JSON messages.
   * Lists have been used to sort the order for database operations.
   * Tuples was used to fetches the rows from database.
   
#### 3. How will you mask the PII data so that duplicate values can be identified?
A: I used a consistent hashing method to mask PII data in a way that allows for the identification of duplicate values. For this application, I used SHA-256 hash function, which ensures that the same input will always produce the same output, allowing us to identify duplicate values based on their hash values. 

#### 4. What will be your strategy for connecting and writing to Postgres?
A: To connect to and write data to Postgres, I used the psycopg2 library. The strategy involves establishing a connection to the database, preparing the data, and then executing the appropriate SQL commands to insert the data.

#### 5. Where and how will your application run?
This application will run on local machine using Docker to simulate AWS services (Localstack) and the Postgres database. Python scripts will interact with Localstack SQS queue and the database. Docker Compose will manage the setup of containers defined in docker-compose.yml.

### Questions:
#### 1. How would you deploy this application in production?
A: To deploy this application into production, we need to follow several steps as below:
* Containerize the application components into docker containers for consistency across environments.
* To manage and scale containers in production we can use platforms like Kubernetes or Docker Swarm, etc.
* We need to use cloud infrastructure for hosting databases and message queues ensuring scalability and security.
* Setup an CI/CD pipeline for automated development, testing and deployment into production environment.
* We need to implement security measures such as encryption, access controls and network policies to protect sensitive information.

#### 2. What other components would you want to add to make this production ready?
A: Most importantly, I would add Logging and monitoring into this application to track the logs and performance of the application which is crucial in any production application, using tools such as ELK or grafana.

#### 3. How can this application scale with a growing dataset.
A: Data Partitioning can be implemented for this application for the growing dataset into smaller chunks to distribute the data across multiple database nodes. Also, we could implement load balancing mechanism to distribute evenly across multiple application instances which ensures optimal resource utilization.

#### 4. How can PII be recovered later on?
A: While masking the PII, we can store the original values (before masking) securely in a separate location, with restricted access controls, encrypted storage, which would allow us to recover the PII data whenever required.

#### 5. What are the assumptions you made?
A: Below assumptions were made while building this application:
* It's assumed that the JSON data structure received from the SQS queue follows a predefined schema and does not vary significantly.
* The database schema for the user_logins table was assumed to be stable and predefined but in a other scenario, schema changes may occur over time, requiring versioning and migrations.
* The masking technique which was used (SHA-256 hashing) assumes that irreversible masking is sufficient for protecting PII. 
