import openai
import configparser
import time
import json

config = configparser.ConfigParser()
config.read('../setup.conf')

OPENAI_API_KEY = config['api']['key']
openai.api_key = OPENAI_API_KEY

client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Proxy-Einstellungen entfernt, da sie in einer Standard OpenAI-Client-Implementierung nicht unterstützt werden

# Texte aus der JSON-Datei einlesen
with open("textToAnalyze.json", "r", encoding='utf-8') as file:
    posts = json.load(file)

# Datei für die Wissensdatenbank hochladen (wenn benötigt)
file = client.files.create(
    file=open("knowledge.txt", "rb"),
    purpose='assistants'
)

# Assistant erstellen
assistant = client.beta.assistants.create(
    name="Hate Speech Detector",
    instructions="You are an officer that checks, if there is love, charity or hate in the text. For examples look into knowledge.txt.",
    tools=[{"type": "retrieval"}],
    model="gpt-4-turbo-preview",
    file_ids=[file.id]
)

# Thread für die Konversation erstellen
thread = client.beta.threads.create()

for post in posts:
    title = post['title']
    body = post['body']

    # Nachricht an den Assistant senden
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Does the following text contain love speech? If yes, answer with 'This text contains love speech'. If the text contains hate speech, answer with 'This text contains hate speech'. If you find love, please use exactly the following phrase in your answer: 'There is love in your text.'. If you find charity, based on the examples, use the phrase '!CHARY, this text is about charity'. If you are not sure, use 'I am not sure about to categorize this content.' Only use these four phrases to answer. Here is the text to analyze: Title: "+title+" Body: "+body,
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Please address the user as Jane Doe. The user has a premium account.",
    )

    print("Checking assistant status for post: ", title)
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        if run.status == "completed":
            print("Done for post: ", title)
            messages = client.beta.threads.messages.list(thread_id=thread.id)

            print("Messages for post: ", title)
            for message in messages:
                assert message.content[0].type == "text"
                print({"role": message.role, "message": message.content[0].text.value})

            break
        else:
            print("In progress...")
            time.sleep(5)

# Den Assistant am Ende löschen
client.beta.assistants.delete(assistant.id)
