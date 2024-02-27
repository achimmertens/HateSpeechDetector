import requests
from requests.exceptions import RequestException
import datetime

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
# The before_date is set to tomorrow to ensure we get the latest posts
before_date = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S')

payload = {
    "jsonrpc": "2.0",
    "method": "condenser_api.get_discussions_by_author_before_date",
    "params": {
        "author": "achimmertens",
        "start_permlink": "",
        "before_date": before_date,
        "limit": "10"
    },
    "id": 1
}

# The URL for the POST request
url = "https://api.hive.blog"

# Perform the POST request
try:
    response = requests.post(url, json=payload, proxies=proxies, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        print("Request successful!")
        # show response.json title and body content:
        content = response.json()["result"]
        for post in content:
            print(f"Title: {post['title']}")
            body = post['body']
            # remove carriage returns and newlines in body
            body = body.replace("\r", "").replace("\n", "")
            print(f"Body: {body[:200]}...")  # Truncate body for display purposes
            print()
    else:
        print(f"Request failed with status code: {response.status_code}")
except RequestException as e:
    print(f"An error occurred: {e}")
