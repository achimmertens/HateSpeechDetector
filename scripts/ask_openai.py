import openai
import configparser
import requests
import time

config = configparser.ConfigParser()
config.read('../setup.conf')

# API-Key aus der Konfigurationsdatei extrahieren
OPENAI_API_KEY = config['api']['key']
openai.api_key = OPENAI_API_KEY
# print(openai.api_key)  # Zum Testen, ob der Key korrekt geladen wurde
client = openai.OpenAI(api_key=OPENAI_API_KEY)
# Konfiguration für Proxies
proxies = {
    'http': 'http://sia-lb.telekom.de:8080',
    'https': 'http://sia-lb.telekom.de:8080'
}
# Setzen Sie die Proxies für die OpenAI-Bibliothek
# openai.Request.request_session.proxies = proxies

# Der zu analysierende Text
text_to_analyze = "Hier steht der Text, der überprüft werden soll."


assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview",
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?",
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user as Jane Doe. The user has a premium account.",
)

print("checking assistant status. ")
while True:
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    if run.status == "completed":
        print("done!")
        messages = client.beta.threads.messages.list(thread_id=thread.id)

        print("messages: ")
        for message in messages:
            assert message.content[0].type == "text"
            print({"role": message.role, "message": message.content[0].text.value})

        client.beta.assistants.delete(assistant.id)

        break
    else:
        print("in progress...")
        time.sleep(5)


