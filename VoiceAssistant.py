import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import requests
import random

# Initialize the recognizer
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-US')
            print(f"User said: {query}")
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return "None"
        except sr.RequestError:
            print("Could not request results; check your network connection.")
            return "None"
        return query

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_news():
    api_key = 'a96b88ff040540cf83e45ee950896004'  # Replace with your NewsAPI key
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        news_data = response.json()
        if 'articles' in news_data:
            articles = news_data['articles'][:5]  # Get top 5 news articles
            news = ""
            for i, article in enumerate(articles, 1):
                news += f"{i}. {article['title']}. "
            return news
        else:
            return "Sorry, I couldn't retrieve the news articles."
    else:
        return "Sorry, I couldn't fetch the news. Please check your API key and network connection."

def play_song():
    webbrowser.open('https://www.youtube.com/results?search_query=play+song')
    return "Playing a song on YouTube"

def tell_joke():
    jokes = [
        "Why don’t scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don’t skeletons fight each other? They don’t have the guts."
    ]
    return random.choice(jokes)

def introduction():
    intro = """
    Hello! I am your voice assistant. I can help you with the following tasks:
    1. Tell you the current time and date.
    2. Open YouTube or Google.
    3. Tell you a joke.
    4. Play a song.
    5. Read the latest news.
    6. Respond to greetings.
    Just say the command and I will assist you.
    """
    return intro

def respond(query):
    query = query.lower()
    
    if 'time' in query:
        time = datetime.datetime.now().strftime('%I:%M %p')
        response = f"The current time is {time}"
    
    elif 'date' in query:
        date = datetime.datetime.now().strftime('%B %d, %Y')
        response = f"Today's date is {date}"
    
    elif 'open youtube' in query:
        webbrowser.open('https://www.youtube.com')
        response = "Opening YouTube"
    
    elif 'open google' in query:
        webbrowser.open('https://www.google.com')
        response = "Opening Google"
    
    elif 'how are you' in query:
        response = "I am fine, thank you. How can I assist you today?"
    
    elif 'play a song' in query:
        response = play_song()
    
    elif 'tell me a joke' in query:
        response = tell_joke()
    
    elif 'latest news' in query:
        response = get_news()
    
    elif 'introduction' in query:
        response = introduction()
    
    elif 'exit' in query or 'quit' in query:
        response = "Goodbye!"
        speak(response)
        exit()
    
    else:
        response = "I'm sorry, I don't understand that command."
    
    return response

if __name__ == "__main__":
    speak(introduction())
    while True:
        query = listen()
        if query != "None":
            response = respond(query)
            print(f"Assistant: {response}")
            speak(response)
