import requests
from requests.exceptions import RequestException

# Set up the proxies for the session
proxies = {
    "http": "http://sia-lb.telekom.de:8080",
    "https": "http://sia-lb.telekom.de:8080",
}

# Set up the headers for the request
headers = {
    "Content-Type": "application/json",
}

# The payload for the POST request
payload = {
    "jsonrpc": "2.0",
    "method": "condenser_api.get_discussions_by_created",
    "params": {"tag": "hiveio", "limit": "10"},
    "id": 1
}

# The URL for the POST request
url = "https://api.openhive.network"

# Perform the POST request
try:
    response = requests.post(url, json=payload, proxies=proxies, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        print("Request successful!")
        # Process the response if needed
        print(response.json())
    else:
        print(f"Request failed with status code: {response.status_code}")
except RequestException as e:
    print(f"An error occurred: {e}")
