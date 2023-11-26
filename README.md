# Data Pipeline Project

## Overview
- This is my first assignment in EEET2574 - Big Data for Engineering
- The origin structure: https://github.com/salcaino/sfucmpt733

## Tools & Technologies

- **Python 3.x:** The project is primarily written in Python to take advantage of its versatility and extensive ecosystem of libraries.

- **Apache Kafka:** Kafka is used as a distributed event streaming platform to facilitate the real-time ingestion of data from multiple sources.

- **Apache Cassandra:** Cassandra serves as the NoSQL database for storing and retrieving the processed data efficiently.

- **Jupyter Notebook:** Jupyter Notebooks are employed for data visualization and exploratory data analysis. They provide an interactive and user-friendly environment for data scientists and analysts.

- **Docker:** The project is containerized using Docker, enabling seamless deployment across different environments and simplifying dependencies management.

- **Visual Studio Code (VSCode):** VSCode is the integrated development environment (IDE) of choice for coding. It offers robust support for Python development and Docker integration.

- **Windows Terminal:** Windows Terminal provides a unified command-line interface for executing commands and managing the project.

## APIs
The project integrates with the following APIs:

- OpenWeather API: Used for retrieving weather data for inclusion in the data pipeline.

- IQAir API: Utilized to gather air quality information for integration into the data processing workflow.

- Faker: Faker is used for generating synthetic or fake data during the development and testing phases.


## Prerequisites

Before using the data pipeline, ensure the following prerequisites are met:
- Python 3.x installed
- Docker installed for containerization

## Getting Started

### Installation
Clone the repository to your local machine:

```bash
git clone https://github.com/DeathHunterX/Simple-datapipeline.git
cd Simple-datapipeline
```
### Configuration
Adjust the configuration settings in config.yaml to match your environment and data sources. This includes specifying source and destination URLs, API keys, Kafka and Cassandra connection details, and other relevant parameters.

## Usage
### Running the Pipeline
Execute the data pipeline with the following command:

```bash
docker network create kafka-network
docker network create cassandra-network
docker network ls

docker-compose -f cassandra/docker-compose.yml up -d
docker-compose -f kafka/docker-compose.yml up -d
docker ps -a

# WSL command
curl -X GET http://localhost:8083/connectors

# access to kafka-connect shell and run this command (this is a bug so you need to run it indirect)
./start-and-wait.sh

docker-compose -f owm-producer/docker-compose.yml up -d
docker-compose -f faker-producer/docker-compose.yml up -d
docker-compose -f iqair-producer/docker-compose.yml up -d


docker-compose -f consumers/docker-compose.yml up -d

# run it to access Cassandra
docker exec -it cassandra bash
cqlsh
desc keyspace;
use kafkapipeline;
desc tables;
select * from weatherreport;
select * from fakerdata;

docker-compose -f data-vis/docker-compose.yml up -d
```

Output:
- Kafka:
    http://localhost:9000   (username: admin; password: bigbang)

- Data Visualization:
    http://localhost:8888



## License
This project is licensed under the MIT License. Feel free to use, modify, and distribute the code as needed.





