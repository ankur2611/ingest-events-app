# Ingest Events App

## Overview

The Ingest Events App is designed to handle and process events. It provides an API endpoint to ingest events and applies various rules to these events.

## Features

- Ingest events via a RESTful API
- Apply rules to events
- Modular and testable code structure

## Prerequisites
- MongoDB
- Python3

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/ankur2611/ingest-events-app.git
   cd ingest-events-app
2. Create a virtual environment and activate it:

        python3 -m venv venv
        . venv/bin/activate

3. Install the required dependencies:

        pip install -r requirements.txt


## Usage
      
      DB Migration:
      Create a collection named "rules" under database "db_virtualness" in mongodb and insert below document.
      {
      	"_id" : ObjectId("66b2038202f51e6e4af96496"),
      	"rule_type" : "ingest",
      	"rule_set" : [
      		{
      			"desc" : "user first nft purchase",
      			"condition" : "verb == 'buy' and noun == 'nft'",
      			"action" : "check_first_nft_purchase"
      		},
      		{
      			"desc" : "volume of nft purchased in last hour",
      			"condition" : "verb == 'buy' and noun == 'nft'",
      			"action" : "check_nfts_volume"
      		},
      		{
      			"desc" : "nft not sold after 7 days of post",
      			"condition" : "verb == 'post' and noun == 'nft'",
      			"action" : "check_nfts_sold"
      		}]
      }
      All events will be inserted in "events" collection
        python3 main.py

        curl --location 'http://localhost:8080/api/v1/ingest-events' \
        --header 'Content-Type: application/json' \
        --data '{
            "userid": 8293,
            "verb": "post",
            "noun": "nft",
            "timestamp": 1722951763,
            "properties": {
                "mode": "netbank",
                "bank": "hdfc",
                "merchantid": 234,
                "value": 4500,
                "quantity": 1,
                "currency": "INR"
            }
        }'

## Running Tests

To run the tests, use the following command:

        python3 -m unittest discover -s tests

## Folder Structure

ingest-events-app/
├── app/
│   ├── controllers/v1
│   │   ├── ingest_controller.py
│   ├── logic/
│   │   ├── ingest_events.py
|   |-- db/
|   |   |---collection.py
|   |   |---events_collection.py
|   |   |---rules_collection.py
│   ├── routes/v1
│   │   ├── routes.py
│   ├── servicecalls
│   │   ├── notification_servicecalls.py
├── tests/
│   ├── test_ingest_events.py
│   ├── test_ingest_controller.py
├── requirements.txt
└── README.md
|-- .env
|-- main.py

