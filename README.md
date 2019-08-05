# Application Overview

The Application overview demonstrates a simple start.

## Requirements 
- It's necessary has docker and docker-compose installed.

## Run the apps locally

- Just run the command below to start the containers  one with the application 
and another with postgres database and will create a networking between them. 
    - `docker-compose up -d`
- The container with application will running on port `9997`
    - `http://localhost:8000/graphql`
- For stop application 
    - `docker-compose down`

