# IMPORTS

import json
import logging
import requests

# VARIABLES

logger = logging.getLogger(__name__)
KAFKA_CONNECT_URL = "http://localhost:8083/connectors"
CONNECTOR_NAME = "stations"

# FUNCTIONS

def configure_connector():
    """Starts and configures the Kafka Connect connector"""
    logging.debug("Creating or updating kafka connect connector...")

    resp = requests.get(f"{KAFKA_CONNECT_URL}/{CONNECTOR_NAME}")
    if resp.status_code == 200:
        print("already connected")
        logging.debug("connector already created skipping recreation")
        return
    resp = requests.post(
        KAFKA_CONNECT_URL,
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "name": CONNECTOR_NAME,
            "config": {
               "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
               "key.converter": "org.apache.kafka.connect.json.JsonConverter",
               "key.converter.schemas.enable": "false",
               "value.converter": "org.apache.kafka.connect.json.JsonConverter",
               "value.converter.schemas.enable": "false",
               "batch.max.rows": "500",
               "connection.url": "jdbc:postgresql://localhost:5432/cta",
               "connection.user": "cta_admin",
               "connection.password": "chicago",
               "table.whitelist": "stations",
               "mode": "incrementing",
               "incrementing.column.name": "stop_id",
               "topic.prefix": "org.chicago.cta.",
               "poll.interval.ms": "6000",
           }
       }
       ),
    )

    ## Ensure a healthy response was given
    logging.info("connector created successfully")
    print(resp.status_code)
    resp.raise_for_status()
    
    if resp.status_code == 201:
        return

if __name__ == "__main__":
    configure_connector()