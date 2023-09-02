#!/bin/bash

if [ $# -ne 3 ]; then
    echo "Usage: $0 <conversation_id> <container_id> <date>"
    echo "Example: $0 2bahudkd2j a189b56e5326 2023-09-01"
    echo "<container_id> can be found by 'docker ps | grep polis-math'"
    exit 1
fi

CONVERSATION_ID="${1:-2bahudkd2j}"
CONTAINER_ID="${2:-math}"
DATE=$3

WORKING_DIR=20230701-ideathon-generative-ai/${DATE}
SNAPSHOT=${CONVERSATION_ID}-${DATE}
mkdir -p ${WORKING_DIR}

function remote_export() {
    ssh polis2023 docker exec -i ${CONTAINER_ID} clojure -M:run export -Z ${CONVERSATION_ID} -f exports/${SNAPSHOT}.zip
}

function get_file() {
    ssh polis2023 unzip -p /home/ubuntu/polis2023/math/exports/${SNAPSHOT}.zip ${SNAPSHOT}/$1 | cat > ${WORKING_DIR}/$1
}


remote_export
get_file comments.csv
get_file votes.csv
python3 pre-processor.py ${WORKING_DIR}
python3 re-calculate-agrees-disagrees.py ${WORKING_DIR}
wc -l ${WORKING_DIR}/*
