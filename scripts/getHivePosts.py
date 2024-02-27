import requests
from requests.exceptions import RequestException
import datetime
import re

# Set up the proxies for the session
proxies = {
    "http": "http://sia-lb.telekom.de:8080",
    "https": "http://sia-lb.telekom.de:8080",
}

# Set up the headers for the request
headers = {
    "Content-Type": "application/json",
}


def remove_text_inside_brackets(text):
    """
    This function removes any text inside brackets and any URLs.
    """
    # Remove text inside any brackets
    # The regex pattern finds text inside (), [] and {}
    no_brackets = re.sub(r"\[.*?\]|\(.*?\)|\{.*?\}", "", text)
    # Remove URLs
    # The regex pattern finds strings that look like URLs
    no_urls = re.sub(r'http[s]?://\S+', '', no_brackets)
    return no_urls.strip()





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
        "limit": "1"
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
            # safe body to file with the name textToAnalyze.txt
            # remove all
            clean_text = remove_text_inside_brackets(body)
            with open("textToAnalyze.txt", "w") as file:
                file.write(clean_text)
            print(f"Body: {clean_text[:200]}...")  # Truncate body for display purposes
            print()
    else:
        print(f"Request failed with status code: {response.status_code}")
except RequestException as e:
    print(f"An error occurred: {e}")
