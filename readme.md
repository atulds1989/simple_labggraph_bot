## A Simple chagtbot using langGraph and langSmith

- The Python script (`data.py`) utilizes the Faker library to generate fake user data for a grocery store. The generated data includes user details, such as name, address, phone number and an order with associated items, total cost and a unique order ID.

- The Python script (`order_backend.py`) serves as a Kafka producer, generating fake user data and sending it to a Kafka topic [**order_details**].

- The Python script (`transaction.py`) acts as a Kafka consumer, listening to a specified Kafka topic for incoming messages containing fake user data representing orders. Upon receiving an order message, it processes the data and sends a confirmation message to another Kafka topic.

- The Python script (`email_notification.py`) acts as a Kafka consumer, listening to a specified Kafka topic for incoming messages containing order confirmation data. Upon receiving a confirmation message, it extracts the customer email and order ID, simulating the process of sending an email to the customer.

- The Python script (`analytics.py`) acts as a Kafka consumer, listening to a specified Kafka topic for incoming messages containing order confirmation data. Upon receiving a confirmation message, it extracts the total cost of the order and updates the analytics, tracking the total number of orders and revenue.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)

## Prerequisites

Before running the script, ensure you have the following prerequisites installed:

- Python 3.x Installed.
- Required Python packages listed in requirements.txt (install using pip install -r requirements.txt)

## Getting Started

To create a project from scratch use following steps -

1. Clone the repository to your local machine.
    ```bash
    git clone https://github.com/your-username/kafka-python-event-driven-app-demo.git
    cd Kakfa-Python-Event-Driven-App-Demo
    ```

2. To run Zookeeper and kafka services, run the Docker Compose configuration provided, you can follow these steps:

    i.   Save the given `docker-compose.yml` file to a directory of your choice.
    ii.  Open a terminal or command prompt, navigate to the directory where the `docker-compose.yml` file is located.
    iii. Run the following command to start the services:
    ```bash
    docker-compose up -d
    ```
    The `-d` flag is used to run the containers in the background.

    iv.  Wait for the containers to be downloaded (if not already available) and started. You can check the status of the running containers using:
    ```bash
    docker-compose ps
    ```

    You should see the status of the zookeeper and kafka containers as "Up."

    Your Kafka and Zookeeper services should now be running. The configuration exposes Zookeeper on port 22181 and Kafka on port 29092. You can use these ports to connect to your Kafka instance. Change the ports according to your requirements.

    To stop the services when you are done, you can run:
    ```bash
    docker-compose down
    ```


3. Create Python Virtual Environment using below command (The recommended python version is 3.11.0).
    ```bash
    python -m venv venv
                OR
    conda activate -p venv python==3.11
    ```

4. Activate Virtual Environment

    ```bash
    .venv/bin/activate 
            OR
    .\venv\Scripts\activate
            OR
    source ./venv/bin/activate
    ```

- if you have used conda to create the virtual environment, use the following command to activate the virtual environment.

    ```bash
    conda activate venv
    ```

5. Install dependencies using below command
    ```bash
    pip install -r requirements.txt
    ```

6. Set up environment variables in a `config.py` file.

    - `ORDER_TOPIC`: "order_details"
    - `SLEEP_TIME` : 4
    - `ORDER_CONFIRMED_TOPIC` : "order_confirmed"

6. If you want to generate the fake data for the grocery store . Go inside the **Kakfa-Python-Event-Driven-App-Demo** directory and run the script.

    This Python script performs the following tasks:

        Generates fake user data and adds an email address based on the user's name. Returns a dictionary with user details, order information, items, and email.

7. If you want to generate the fake data and sending it to a Kafka topic. Go inside the **Kakfa-Python-Event-Driven-App-Demo** directory and run the script. This will continuously produce fake user data and send it to the specified Kafka topic until interrupted by a keyboard interrupt.
    ```bash
    python order_backend.py
    ```

8. To run the `transaction.py` to consumes order messages, processes the data and sends confirmation messages to another Kafka topic until interrupted by a keyboard interrupt. Go inside the **Kakfa-Python-Event-Driven-App-Demo** directory and run the script.
    ```bash
    python transaction.py
    ```


9. To send an order confirmation mail to the customer. Go inside the **Kakfa-Python-Event-Driven-App-Demo** directory and run the script. This script continuously consumes order confirmation messages, extracts the necessary information, and simulates sending an email to the customer until interrupted by a keyboard interrupt.
    ```bash
    python email_notification.py
    ```

10. To track the total number of orders and revenue. Go inside the **Kakfa-Python-Event-Driven-App-Demo** directory and run the script. This script continuously consumes order confirmation messages, extracts the total cost, and updates analytics for total orders and revenue until interrupted by a keyboard interrupt.
    ```bash
    python analytics.py
    ```


`Note`:
Ensure you have the Kafka server running. If not, please run the docker-compose file.