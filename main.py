import pyttsx3
import keyboard

from audio import record_and_transcribe
from model import GPTAgent
from schedule import Schedule


def text_to_speech(text):
    engine = pyttsx3.init()

    # Set the voice to Microsoft Zira
    voices = engine.getProperty('voices')
    for voice in voices:
        if "Zira" in voice.name:
            engine.setProperty('voice', voice.id)
            break

    engine.say(text)
    engine.runAndWait()


def main():
    ghost = "files/schedule.txt"
    model = GPTAgent(ghost)

    # Schedule()  # it will create a transcript.txt file with the schedule of the event

    # introduction to the event
    question = 'Introduce yourself and the event, just introduce the event and yourself, dont mention about any ' \
               'speakers, say good morning the event happens in the morning '
    print("Starting....")
    answer = model(question)
    print("Answer:", answer)
    with open('transcript.txt', 'r') as file:
        content = file.read()
        parts = content.split('$$$')
    answer = answer + parts[0]
    trigger = input("Press 'a' to play answer")
    if trigger == 'a':
        text_to_speech(answer)  # it will convert the answer to audio and play it

    try:
        for i in range(1, len(parts)):
            question = record_and_transcribe()
            print("Question:", question)
            context = 'write thank you note for the speaker, include 2 line summary of the talk provided, just thank ' \
                      'the speaker with information he spoke about dont add any assumptions or new information, ' \
                      'and dont invite the next speaker '
            answer = model(question + context)
            print("Answer:", answer + parts[i])
            trigger = input("Press 'a' to play answer")
            if trigger == 'a':
                text_to_speech(answer + parts[i])  # it will convert the answer to audio and play it

    except KeyboardInterrupt:
        # break
        print("Bye!")


#
if __name__ == '__main__':
    main()
