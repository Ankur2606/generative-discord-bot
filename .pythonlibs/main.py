# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot

import os
import discord
import openai
# app_id = 1036577213493030972
# pub_key = 4674bed8b8ab40d453b43ab382f6179563ae6c72deb16af009d19d2f027954f7

file = "prompt.txt"

with open(file, "r") as f:
  chat = f.read() 

openai.api_key = os.getenv("OPENAI_API_KEY")
token = os.getenv("TOKEN")

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        global chat
        try:
          chat += f"{message.author}: {message.content}\n"
          print(f'Message from {message.author}: {message.content}')
          if self.user!= message.author:
              if self.user in message.mentions:
                response = openai.Completion.create(
                  model="text-davinci-003",
                  prompt = f"{chat}\nHarryGPT: ",
                  temperature=1,
                  max_tokens=256,
                  top_p=1,
                  frequency_penalty=0,
                  presence_penalty=0
                )
                channel = message.channel
                messageToSend = response.choices[0].text
                await channel.send(messageToSend)    
        except Exception as e:
          print(e)
          chat = ""


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)

