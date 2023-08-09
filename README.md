# Fetch #
## Data Engineering Take Home: ETL off a SQS Queue ##

This project is the solution for the Data Engineering assignment given by Fetch.

# Have the following installed on your PC #

Ubuntu -- ``apt-get -y install make``

Windows -- ``choco install make``

Mac -- ``brew install make``

python3

pip3 -- ``python -m ensurepip --upgrade`` or ``run make pip-install`` in root

awslocal -- ``pip install awscli-local`` or run ``make pip install`` in root

docker and docker-compose

## To run the code
1. Clone this repo.
``bash
git clone https://github.com/Moiz2803/Fetch.git
``

2. Go into the cloned repo.
``bash
cd Fetch
``

3. Run the `make` command to install dependencies.
``bash
make pip-install
``

4. Run the `make` command to configure the aws shell.
``bash
make aws-configure
``

5. Pull and start docker containers.
``bash
make start
``

6. Run Python code to perform the ETL process.
``bash
make perform-etl
``

## Verifying messages loaded in Postgres
- To validate the messages loaded in Postgres
``bash
psql -d postgres -U postgres -p 5432 -h localhost -W
``
- Credentials and database information
    - **username**=`postgres`
    - **password**=`postgres`
    - **database**=`postgres`

- If `psql` binary is not installed on Ubuntu based distros, install it using the below command.
``bash
apt install postgresql-client
``

## Decrypting masked PIIs
- The `ip` and `device_id` fields are masked using base64 encryption.
- To recover the encrypted fields, we can use the below command.
``bash
echo -n "<sample_base64_encrypted_string>" | base64 --decrypt
``

# Regarding the questions. # 

``I would take the following actions in order to deploy this application in production:

Deployment Method:



Create a cloud infrastructure for hosting the application components, such as AWS, Azure, or Google Cloud.

For simple deployment and scaling, containerize the application using Docker or another containerization tool.

To manage and scale the application containers, use a platform for container orchestration like Kubernetes.

Utilising a Continuous Integration/Continuous Deployment (CI/CD) pipeline for automated deployment and updates, deploy the application containers to production.

Enhancing Production-Readiness Components



Monitoring and logging: To track the application's health and performance metrics, integrate monitoring tools like Prometheus or New Relic. To gather and analyse logs, use centralised logging solutions (like the ELK stack).

I would take the following actions in order to deploy this application in production:

Deployment Method:



Create a cloud infrastructure for hosting the application components, such as AWS, Azure, or Google Cloud.

For simple deployment and scaling, containerize the application using Docker or another containerization tool.

To manage and scale the application containers, use a platform for container orchestration like Kubernetes.

Utilising a Continuous Integration/Continuous Deployment (CI/CD) pipeline for automated deployment and updates, deploy the application containers to production.

Enhancing Production-Readiness Components



Monitoring and logging: To track the application's health and performance metrics, integrate monitoring tools like Prometheus or New Relic. To gather and analyse logs, use centralised logging solutions (like the ELK stack).

I would take the following actions in order to deploy this application in production:

Deployment Method:



Create a cloud infrastructure for hosting the application components, such as AWS, Azure, or Google Cloud.

For simple deployment and scaling, containerize the application using Docker or another containerization tool.

To manage and scale the application containers, use a platform for container orchestration like Kubernetes.

Utilising a Continuous Integration/Continuous Deployment (CI/CD) pipeline for automated deployment and updates, deploy the application containers to production.

Enhancing Production-Readiness Components



Monitoring and logging: To track the application's health and performance metrics, integrate monitoring tools like Prometheus or New Relic. To gather and analyse logs, use centralised logging solutions (like the ELK stack).

Security: Implement security measures such as encryption of sensitive data at rest and in transit. Use identity and access management (IAM) roles to ensure secure access to resources.

Load Balancing: Set up load balancing to distribute incoming traffic and ensure high availability.

Database Scaling: Implement strategies for database scaling, such as using Amazon RDS with read replicas or sharding the database, to handle a growing dataset.

Automated Backups: Regularly back up the database to prevent data loss in case of failures.


Growing Dataset Scaling:


Increase the number of worker nodes to process messages from the SQS queue concurrently by using horizontal scaling.

Use partitioning or sharding techniques to distribute data across a number of database nodes.

Use caching techniques (like Redis) to speed up response times and lessen the load on the database.``


``Recovery of Masked PII:

The base64 encryption method offered allows for the recovery of the masked PII (Personal Identifiable Information). The base64_encode function in the code uses base64 encoding to encode the original PII values. To get back the initial values:

Obtain the masked PII values from the logs or database.
To decode the masked value, use the base64 decoding command as described in the README file.

Assumptions Made:

Data Integrity: I assumed that the masked PII values would be stored securely and would not be compromised, as recovering the original values would undermine the data privacy measures.

Key Management: I assumed that the encryption keys used for masking and unmasking PII would be securely managed to prevent unauthorized access.

Base64 Encoding: I assumed that the provided base64 encoding method would be used consistently for both masking and unmasking PII.

Access Control: I assumed that only authorized personnel with appropriate access rights would be able to recover the masked PII.

Data Recovery: I assumed that the process of recovering masked PII would be subject to strict auditing and monitoring to prevent misuse.

It's important to note that while base64 encoding provides a level of obfuscation, it's not a secure encryption method for sensitive data. In a real-world scenario, more robust encryption techniques should be used to protect sensitive information.``




