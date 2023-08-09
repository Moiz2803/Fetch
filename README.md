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
