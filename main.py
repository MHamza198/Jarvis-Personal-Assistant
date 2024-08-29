import speech_recognition as sr
import pyttsx3
import webbrowser
import requests
import openai  
import time 
from song_library import get_song_url  

# API keys (replace with your own)
NEWS_API_KEY = 'PLACE YOUR API'
OPENAI_API_KEY = 'PLACE YOUR API'

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_news(category="general"):
    """
    Fetch top headlines for a given category (default: 'general').
    Categories include 'business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology'.
    """
    url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if data["status"] == "ok":
        headlines = [article['title'] for article in data['articles'][:5]]  # Get top 5 headlines
        return headlines
    else:
        return ["I couldn't fetch the news right now."]

def talk_to_ai(prompt):
    """
    Use OpenAI's GPT to have a conversation with Jarvis.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use GPT-3.5 Turbo or the latest available model
        messages=[
            {"role": "system", "content": "You are Jarvis, a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    return response['choices'][0]['message']['content'].strip()

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")   
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")    
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "play" in c.lower():
        song_name = c.lower().replace("play", "").strip()  # Extract the song name
        song_url = get_song_url(song_name)  # Get the song URL from the library
        if song_url:
            webbrowser.open(song_url)
            speak(f"Playing {song_name}")
        else:
            speak(f"Sorry, I don't have {song_name} in my library.")
    elif "news" in c.lower():
        category = "general"
        if "business" in c.lower():
            category = "business"
        elif "sports" in c.lower():
            category = "sports"
        elif "technology" in c.lower():
            category = "technology"
        elif "entertainment" in c.lower():
            category = "entertainment"

        headlines = get_news(category)
        for headline in headlines:
            speak(headline)
    elif "talk to ai" in c.lower():
        # Extract the user's message for AI
        prompt = c.lower().replace("talk to ai", "").strip()
        if prompt:
            response = talk_to_ai(prompt)
            speak(response)
            time.sleep(2)  # Wait for 2 seconds before allowing the next command
        else:
            speak("What would you like to ask the AI?")

if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        r = sr.Recognizer()
        
        print("Recognizing...")
        try:   
            with sr.Microphone() as source:
                print("Listening for the wake word...")
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source, timeout=5, phrase_time_limit=2)
            
            word = r.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Yeah")
                
                # Listen for the actual command after "Jarvis" is detected
                with sr.Microphone() as source:
                    print("Jarvis Active... listening for command")
                    audio = r.listen(source, timeout=5, phrase_time_limit=4)
                    command = r.recognize_google(audio)
                    
                    # Process the command
                    processCommand(command)
                    # Add a brief pause after processing a command
                    time.sleep(2)  # Wait for 2 seconds before allowing the next command
        
        except sr.WaitTimeoutError:
            print("Listening timed out, no speech detected. Waiting for the wake word...")
        
        except sr.UnknownValueError:
            print("Google could not understand audio")
        
        except sr.RequestError as e:
            print(f"Google error: {e}")
