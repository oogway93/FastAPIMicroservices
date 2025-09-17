#!/bin/bash

cp ./requirements.txt ./auth_service/
cp ./requirements.txt ./accounts_service/

cp ./.env ./auth_service/app
cp ./.env ./accounts_service/app