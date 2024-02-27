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
# export http_proxy=http://sia-lb.telekom.de:8080
# export https_proxy=http://sia-lb.telekom.de:8080

# Der zu analysierende Text
#text_to_analyze = "I have helped some poor people in the street to get some food."

# Open the file "testToAnalyze.txt" and read the content into the variable "text_to_analyze".
with open("textToAnalyze.txt", "r") as file:
    text_to_analyze = file.read()

print("Folgender Text wird analysiert: ")
print(text_to_analyze)



# Upload a file with an "assistants" purpose
file = client.files.create(
    file=open("knowledge.txt", "rb"),
    purpose='assistants'
)


assistant = client.beta.assistants.create(
    name="Hate Speech Detector",
    instructions="You are an officer that checks, if there is love, charity or hate in the text. For examples look into knowledge.txt.",
    tools=[{"type": "retrieval"}],
    # model="gpt-4-1106-preview",
    model="gpt-4-turbo-preview",
    file_ids=[file.id]
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Does the following text contain love speech? If yes, answer with 'This text contains love speech'. If the text contains hate speech, answer with 'This text contains hate speech'  If you find love, please use exactly the following phrase in your answer: 'There is love in your text.'. If you find charity, based on the examples, use the phrase '!CHARY, this text is about charity'. If you are not sure, use 'I am not sure about to categorize this content.' Only use one of these four phrases to answer. Here is the text to analyze: "+text_to_analyze,
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


