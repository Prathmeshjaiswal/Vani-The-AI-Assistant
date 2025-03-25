from AppOpener import close,open as appopen
from webbrowser import open as webopen
from pywhatkit import search,playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

classes = []

useragent = "Mozilla/5.0 (windows NT 10.0; win64;x64) AppleWebkit/537.36"
client = Groq(api_key=GroqAPIKey)

professional_responses =[
    "Your satisfaction is my top priority sir; feel free to reach out to if there is anything else i can help you with.",
    "I am at you service for any additional questions or support you may need  please dont hesitate to ask."
]

messages =[]

SystemChatBot = [{"role":"system","content":f"Hello i am {os.environ['Username']}, you are a content writer. you have to write content like letter."}]

def GoogleSearch(Topic):
    search(Topic)
    return True


# def Content(Topic):
#     def OpenNotepad(File):
#         default_text_editor = 'notepad.exe'
#         subprocess.Popen([default_text_editor,File])

    # def ContentWriterAI(prompt):
    #     messages.append({"role":"user","content":f"{prompt}"})

    #     completion = client.chat.completions.create(
    #         model = "mixtral-8x7b-32768",
    #         messages= SystemChatBot + messages,
    #         max_tokens = 2048,
    #         temperature=0.7,
    #         top_p = 1,
    #         stream=True,
    #         stop =None
    #     )

    #     Answer = ""

    #     for chunk in completion:
    #         if chunk.choices[0].delta.content:
    #             Answer += chunk.choices[0].delta.content

    #     Answer = Answer.replace("</s>","")
    #     messages.append({"role":"assistant","content":Answer})
    #     return Answer
    
    # Topic:str = Topic.replace("Content","")
    # ContentByAI= ContentWriterAI(Topic)

    # with open(rf"Data\{Topic.lower().replace('','')}.txt","w",encoding="utf-8") as file:
    #     file.write(ContentByAI)
    #     file.close()

    # OpenNotepad(rf"Data\{Topic.lower().replace('','')}.txt")
    # return True


def YouTubeSearch(Topic):
    Url4search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4search)
    return True


def PlayYoutube(query):
    playonyt(query)
    return True


def OpenApp(app,sess=requests.session()):
    try:
        appopen(app,match_closest=True,output=True,throw_error=True)
        return True
    except:
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html,'html.parser')
            links=soup.find_all('a',{'jsname':'UWckNb'})
            return [link.get('href' for link in links)]
        
        def search_google(query):
            url =f"https://www.google.com/search?q={query}"
            headers = {"User-Agent":useragent}
            response = sess.get(url,headers = headers)

            if response.status_code == 200:
                return response.text
            else:
                print("Fialed to retrive search results...")
                return None
        
        html = search_google(app)

        if html:
            link = extract_links(html)[0]
            webopen(link)

        return True
    

def CloseApp(app):
        if 'chrome' in app:
            pass
        else:
            try:
                close(app,match_closest=True,output=True,throw_error=True)
                return True
            except:
                return False

def System(command):
        def mute():
            keyboard.press_and_release("volume mute")
        def unmute():
            keyboard.press_and_release("volume mute")
        def volume_up():
            keyboard.press_and_release("volume up")
        def volume_down():
            keyboard.press_and_release("volume down")
        
        if command =="mute":
            mute()
        elif command =="unmute":
            unmute()    
        elif command =="Volume up":
            volume_up()
        elif command =="volume down":
            volume_down()
        return True

async def TranslateAndExecute(commands: list[str]):
        funcs = []

        for command in commands:
            if command.startswith("open"):
                if "open it" in command:
                    pass
                if "open file" in command:
                    pass
                else:
                    fun = asyncio.to_thread(OpenApp,command.removeprefix("open"))
                    funcs.append(fun)

            elif command.startswith("general"):
                pass

            elif command.startswith("realtime"):
                pass

            elif command.startswith("close"):
                fun = asyncio.to_thread(CloseApp,command.removeprefix("close"))
                funcs.append(fun)

            elif command.startswith("play"):
                fun = asyncio.to_thread(PlayYoutube,command.removeprefix("play"))
                funcs.append(fun)
            
            elif command.startswith("content"):
                fun = asyncio.to_thread(Content,command.removeprefix("content"))
                funcs.append(fun)

            elif command.startswith("google search"):
                fun = asyncio.to_thread(GoogleSearch,command.removeprefix("google search"))
                funcs.append(fun)

            elif command.startswith("youtube search"):
                fun = asyncio.to_thread(YouTubeSearch,command.removeprefix("youtube search"))
                funcs.append(fun)

            elif command.startswith("system"):
                fun = asyncio.to_thread(System,command.removeprefix("system"))
                funcs.append(fun)

            else:
                print(f"No functionality found for {command}")
        results = await asyncio.gather(*funcs)

        for result in results:
            if isinstance(result,str):
                yield result
            else:
                yield result

async def Automation(commands: list[str]):
        async for result in TranslateAndExecute(commands):
            pass
        
        return True

# if __name__ == "__main__":
        # asyncio.run(Content(["leave application"]))
