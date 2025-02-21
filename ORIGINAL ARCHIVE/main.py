# [HUMBLENESS NOTE BOOK]
# [=] Improved the login where it logs in via an in-program input via user_token = '' instead of copy and pasting it
# [+] added a logs channel with spacing for easier debugging

import discord
import asyncio
import aiohttp
import os
import colorama
import ctypes
import fade
from colorama import Fore
from discord.ext import commands

intents = discord.Intents.default()
client = discord.Client(intents=intents, self_bot=True)

# Removed Original Token Prompt Command And Moved To Line 423

text = """
                                            .▄▄ · ▄▄▄ .▄▄▌  ·▄▄▄▄▄▄▄·       ▄▄▄▄▄
                                            ▐█ ▀. ▀▄.▀·██•  ▐▄▄·▐█ ▀█▪▪     •██  
                                            ▄▀▀▀█▄▐▀▀▪▄██▪  ██▪ ▐█▀▀█▄ ▄█▀▄  ▐█.▪
                                            ▐█▄▪▐█▐█▄▄▌▐█▌▐▌██▌.██▄▪▐█▐█▌.▐▌ ▐█▌·
                                             ▀▀▀▀  ▀▀▀ .▀▀▀ ▀▀▀ ·▀▀▀▀  ▀█▄▀▪ ▀▀▀ 
"""
title = Fore.YELLOW+f"""                    
                                                      [IMPROVED BY EGO]
                                                       [Prefix: {Fore.WHITE},cmds{Fore.YELLOW}]{Fore.RESET}"""
                                                      
                                                      

os.system("cls")
os.system('title Ravers Selfbot [@humbleness]')
faded_text = fade.fire(text)
print(faded_text)
print(title)
print(Fore.YELLOW+f"""\n\n                                        Logs Will Be Printed Below Including {Fore.RED}Error Logs{Fore.YELLOW}: \n\n{Fore.RESET}""")

owners = {804666654604263425}  # Your / Users UID
user_id = None
guild_id = None
channel_id = None
count = 0
delay = 0.5  # Delay of 1 second
spam_enabled = False
spam_message = None
auto_react_emojis = []
react_target_id = None
ar_target_id = None
ar_message = None
ar_channel_id = None
is_logged_out = False
admins = set()
active_commands = set()
stop_flag = False

# Redundant But Still Usable
async def get_user_id():
    user = await client.fetch_user("@me")
    return user.id

async def change_channel_name(channel, new_name):
    try:
        await channel.edit(name=new_name)
        print(Fore.GREEN+f"""[LOG] Changed Name Of Group Chat To {new_name}{Fore.RESET}""")
    except discord.Forbidden:
        print(Fore.GREEN+f"""[LOG] Changing The Name Of Group Chat{channel.name} Failed Due To Permissions.{Fore.RESET}""")
    except Exception as e:
        print(Fore.RED+f"""[LOG] An Error Occurred While Changing The Name Of Group Chat  {channel.name}: {e} {Fore.RESET}""")

async def spam_change_name():
    global count
    while spam_enabled:
        if count > 10000:
            count = 1
        if channel_id:
            channel = client.get_channel(channel_id)
            if isinstance(channel, discord.GroupChannel):
                with open("gcc.txt", "r") as file:
                    base_name = file.read().strip()
                new_name = f"{base_name} {count}"
                await change_channel_name(channel, new_name)
                count += 1
                await asyncio.sleep(delay)

async def create_group_chat(target_id, additional_user_ids):
    headers = {
        'Authorization': user_token,
        'Content-Type': 'application/json'
    }
    json_data = {
        'recipients': [str(target_id)] + [str(uid) for uid in additional_user_ids]
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post('https://discord.com/api/v9/users/@me/channels', headers=headers, json=json_data) as response:
            if response.status == 200:
                print(Fore.GREEN+f"""[LOG] Group Chat Created Successfully With {target_id} {Fore.RESET}""")
            else:
                error_details = await response.text()
                print(Fore.RED+f"""[LOG] Failed To Create Group Chat With {target_id}: {response.status} {Fore.RESET}""")
                print(Fore.RED+f"""[LOG] Error Details: {error_details} {Fore.RESET}""")

async def spam_create_group_chats(target_id):
    with open("userids.txt", "r") as file:
        additional_user_ids = [int(line.strip()) for line in file.readlines()]
    while spam_enabled:
        for uid in additional_user_ids:
            await create_group_chat(target_id, [uid])
            await asyncio.sleep(delay)

async def update_counter():
    global count
    with open("gcc_counter.txt", "w") as file:
        file.write(str(count))

async def load_counter():
    global count
    if os.path.exists("gcc_counter.txt"):
        with open("gcc_counter.txt", "r") as file:
            count = int(file.read().strip())
    else:
        count = 1

@client.event
async def on_ready():
    global user_id
    user_id = await get_user_id()
    print(Fore.GREEN+f"""[LOG] Current User = {client.user} {Fore.RESET}""")
    client.loop.create_task(spam_change_name())

# SFW COMMANDS
               
async def send_kiss_image(channel):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.waifu.pics/sfw/kiss') as response:
            if response.status == 200:
                data = await response.json()
                image_url = data.get('url')
                if image_url:
                    await channel.send(image_url)
                else:
                    await channel.send('No Image URL Found.')
            else:
                await channel.send('Failed To Retrieve Image.')    


async def send_lick_image(channel):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.waifu.pics/sfw/lick') as response:
            if response.status == 200:
                data = await response.json()
                image_url = data.get('url')
                if image_url:
                    await channel.send(image_url)
                else:
                    await channel.send('No Image URL Found.')
            else:
                await channel.send('Failed To Retrieve Image.')
                
async def send_cuddle_image(channel):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.waifu.pics/sfw/cuddle') as response:
            if response.status == 200:
                data = await response.json()
                image_url = data.get('url')
                if image_url:
                    await channel.send(image_url)
                else:
                    await channel.send('No Image URL Found.')
            else:
                await channel.send('Failed To Retrieve Image.')

async def send_bonk_image(channel):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.waifu.pics/sfw/bonk') as response:
            if response.status == 200:
                data = await response.json()
                image_url = data.get('url')
                if image_url:
                    await channel.send(image_url)
                else:
                    await channel.send('No Image URL Found.')
            else:
                await channel.send('Failed To Retrieve Image.')          
                
# NSFW COMMANDS 

async def send_mommy_image(channel):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.waifu.pics/nsfw/waifu') as response:
            if response.status == 200:
                data = await response.json()
                image_url = data.get('url')
                if image_url:
                    await channel.send(image_url)
                else:
                    await channel.send('No Image URL Found.')
            else:
                await channel.send('Failed To Retrieve Image.')

async def send_neko_image(channel):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.waifu.pics/nsfw/neko') as response:
            if response.status == 200:
                data = await response.json()
                image_url = data.get('url')
                if image_url:
                    await channel.send(image_url)
                else:
                    await channel.send('No Image URL Found.')
            else:
                await channel.send('Failed To Retrieve Image.')

async def send_trap_image(channel):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.waifu.pics/nsfw/trap') as response:
            if response.status == 200:
                data = await response.json()
                image_url = data.get('url')
                if image_url:
                    await channel.send(image_url)
                else:
                    await channel.send('No Image URL Found.')
            else:
                await channel.send('Failed To Retrieve Image.') 

async def send_bj_image(channel):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.waifu.pics/nsfw/blowjob') as response:
            if response.status == 200:
                data = await response.json()
                image_url = data.get('url')
                if image_url:
                    await channel.send(image_url)
                else:
                    await channel.send('No Image URL Found.')
            else:
                await channel.send('Failed To Retrieve Image.')    

@client.event
async def on_message(message):
    global user_id, channel_id, count, spam_enabled, spam_message, auto_react_emojis, react_target_id, ar_target_id, ar_message, ar_channel_id, is_logged_out

    if user_id is None:
        return
    if is_logged_out:
        return

    if auto_react_emojis and message.author.id == react_target_id:
        try:
            for emoji in auto_react_emojis:
                await message.add_reaction(emoji)
        except discord.HTTPException as e:
            print(f"Failed To Add Reactions: {e}")

    if ar_target_id and message.author.id == ar_target_id:
        try:
            await message.channel.send(ar_message)
        except discord.HTTPException as e:
            print(f"Failed To Send Auto Response: {e}")

    if message.author.id == user_id or message.author.id in admins:
        if message.content.startswith(',cgc'):
            args = message.content.split()
            if len(args) == 2:
                try:
                    target_id = int(args[1])
                    with open("userids.txt", "r") as file:
                        additional_user_ids = [int(line.strip()) for line in file.readlines()]
                    await create_group_chat(target_id, additional_user_ids)
                except ValueError:
                    await message.channel.send("Invalid ID Format.")
                except FileNotFoundError:
                    await message.channel.send("userids.txt File Not Found.")
        elif message.content.startswith(',uwu'):
            await message.channel.send("https://p19-pu-sign-useast8.tiktokcdn-us.com/tos-useast5-p-0068-tx/3b381378c83048d69ac9a6facd3cf63e_1712412347~tplv-photomode-zoomcover:720:720.jpeg?lk3s=b59d6b55&nonce=93358&refresh_token=74b449c56df1d2328d0eeb6ccf95ab06&x-expires=1719198000&x-signature=V7F9GFb6WuvFQ19tYH8F3RUAzu4%3D&shp=b59d6b55&shcp=-")
            # BROKEN
        elif message.content.startswith('!RAINBOW'):
            args = message.content.split()
            if len(args) == 2:
                try:
                    target_id = int(args[1])
                    if target_id < 1000000000000000000:
                        channel_id = None
                        guild_id = None
                        user_id = target_id
                        await message.add_reaction('🌈')
                    else:
                        user_id = None
                        channel_id = None
                        guild_id = target_id
                        await message.add_reaction('🌈')
                except ValueError:
                    pass
            #         
        elif message.content.startswith(',fill'):
            spam_enabled = True
            with open("spam.txt", "r") as file:
                spam_message = file.read()
            for _ in range(600000):
                await message.channel.send(spam_message)
                await asyncio.sleep(delay)
        elif message.content.startswith(',setemoji'):
            args = message.content.split()
            if len(args) > 1:
                auto_react_emojis = args[1:]
                await message.channel.send(f'Auto-react Emojis Set To: {", ".join(auto_react_emojis)}')
                print(Fore.GREEN+f"""[LOG] Auto-React Has Been Ran{Fore.RESET}""")
        elif message.content.startswith(',react'):
            if message.content.startswith(',reactstop'):
                react_target_id = None
                await message.channel.send("Auto reaction stopped.")
                print(Fore.GREEN+f"""[LOG] Auto Reaction Has Stopped{Fore.RESET}""")
            else:
                if len(message.mentions) == 1:
                    target_user = message.mentions[0]
                    react_target_id = target_user.id
                    await message.channel.send(f'Auto Reaction Target Set To: {target_user.name}')
        elif message.content.startswith(',AR'):
            if message.content.startswith(',ARstop'):
                ar_target_id = None
                ar_message = None
                ar_channel_id = None
                await message.channel.send("Auto Respond Stopped.")
                print(Fore.GREEN+f"""[LOG] Auto respond Has Stopped{Fore.RESET}""")
            else:
                if len(message.mentions) == 1:
                    target_user = message.mentions[0]
                    ar_target_id = target_user.id
                    ar_channel_id = message.channel.id
                    try:
                        with open("ar.txt", "r") as file:
                            ar_message = file.read()
                        await message.channel.send(f'Auto Respond Target Set To: {target_user.name}')
                    except FileNotFoundError:
                        await message.channel.send("Error: ar.txt File Not Found.")
        elif message.content.startswith(',logout'):
            is_logged_out = True
            await message.channel.send(f"{message.author.mention} Logging Out...")
            await client.logout()
        elif message.content == ',cmds':
            misc_list = [
                ',cmds : Show Available Commands',
                ',logout : Logout The bot',
                ',credit : Show Credits',
            ]
            chatpacking_list = [
                ',gcc : Start changing group chat name with names from gcc.txt file',
                ',stopgc : Stop changing group chat name'
                ',fill : Spam message from spam.txt file 600000 times',
                ',setemoji <emojis> : Set auto-react emojis',
                ',react <@user> : Set auto reaction target user',
                ',reactstop : Stop auto reactions',
                ',AR <@user> : Set auto respond target user and message from AR.txt file',
                ',ARstop : Stop auto respond',
                ',cgc <target_id> : Create group chat with target ID and additional user IDs from file',
                ',edate : A Lovely Letter For Your Special One',
            ]
            random_list = [
                ',kiss : SFW GIF [For Trolling And Devious Acts]',
                ',lick : SFW GIF [For Trolling And Devious Acts]',
                ',hug : SFW GIF [For Trolling And Devious Acts]',
                ',abuse : SFW GIF [For Trolling And Devious Acts]',
                '\n', 
                ',mommy : NSFW GIF [Not My Fault If You Get Termed]',
                ',neko : NSFW GIF [Not My Fault If You Get Termed]',
                ',trap : NSFW GIF [Not My Fault If You Get Termed]',
                ',bj : NSFW GIF [Not My Fault If You Get Termed]',
                ',spiderdick : NSFW GIF [Not My Fault If You Get Termed]',
            ]
            
            print(Fore.GREEN+f"""[LOG] ,cmds Has Been Run{Fore.RESET}""")
            response = '```ini\n[Selfbot Misc Commands:]\n{}```'.format('\n'.join(misc_list))
            await message.channel.send(response)

            response = '```ini\n[Selfbot Chatpack Commands:]\n{}```'.format('\n'.join(chatpacking_list))
            await message.channel.send(response)
            
            response = '```ini\n[Selfbot Random Commands:]\n{}```'.format('\n'.join(random_list))
            await message.channel.send(response)
        elif message.content.startswith(',server'):
            await message.channel.send("https://discord.gg/molly")
        elif message.content.startswith(',gcc'):
            try:
                with open("gcc.txt", "r") as file:
                    base_name = file.read().strip()
                if isinstance(message.channel, discord.GroupChannel):
                    channel_id = message.channel.id
                    spam_enabled = True
                    asyncio.create_task(spam_change_name())
                else:
                    await message.channel.send("This Command Can Only Be Used In A Group Chat.")
            except FileNotFoundError:
                await message.channel.send("gcc.txt File Not Found.")
        elif message.content.startswith(',stopgc'):
            spam_enabled = False
            await message.channel.send("Stopped Changing Group Chat Name.")
            
            #SFW API COMMANDS  
        elif message.content.startswith(',kiss'):
            await send_kiss_image(message.channel)  
        elif message.content.startswith(',lick'):
            await send_lick_image(message.channel)  
        elif message.content.startswith(',hug'):
            await send_cuddle_image(message.channel)  
        elif message.content.startswith(',abuse'):
            await send_bonk_image(message.channel)  

            #NSFW API COMMANDS  
        elif message.content.startswith(',mommy'):
            await send_mommy_image(message.channel)
        elif message.content.startswith(',neko'):
            await send_neko_image(message.channel)  
        elif message.content.startswith(',trap'):
            await send_trap_image(message.channel) 
        elif message.content.startswith(',bj'):
            await send_bj_image(message.channel) 
        elif message.content.startswith(',spiderweb'):
            await send_sw_image(message.channel)      

        elif message.content.startswith(',stream'):
            new_status = message.content[8:].strip()
            if new_status:
                await client.change_presence(activity=discord.Streaming(name=new_status, url='https://www.twitch.tv/owobotplays'))
                await message.channel.send(f"Streaming Status Changed To: **{new_status}**")
            else:
                await message.channel.send("Please Provide A Status Message.")
                return

        elif message.content.startswith(',edate'):
               # await message.channel.send("@everyone")
                await message.channel.send("can we honestly e date? you’re so beautiful. You always make me laugh, you always make me smile. You literally make me want to become a better person... I really enjoy every moment we spend together. My time has no value unless its spent with you. I tell everyone of my irls how awesome you are. Thank you for being you. Whenever you need someone to be there for you, know that i’ll always be right there by your side. I love you so much. I don’t think you ever realize how amazing you are sometimes. Life isn’t as fun when you’re not around. You are truly stunning. I want you to be my soulmate. I love the way you smile, your eyes are absolutely gorgeous. If I had a star for everytime you crossed my mind i could make the entire galaxy. Your personality is as pretty as you are and thats saying something. I love you, please date me. I am not even calling it e dating anymore because I know we will meet soon enough heart OK I ADMIT IT I LOVE YOU OK i hecking love you and it breaks my heart when i see you play with someone else or anyone commenting in your profile i just want to be your girlfriend and put a heart in my profile linking to your profile and have a walltext of you commenting cute things i want to play video games talk in discord all night and watch a movie together but you just seem so uninsterested in me it hecking kills me and i cant take it anymore i want to remove you but i care too much about you so please i’m begging you to eaither love me back or remove me and never contact me again it hurts so much to say this because i need you by my side but if you dont love me then i want you to leave because seeing your icon in my friendlist would kill me everyday of my pathetic life.")
                return

        elif message.content.startswith(',jews'):
                await message.channel.send("YOUR ALL FUCKING JEWS. GO FUCK YOURSELF")
                await message.channel.send("https://www.gtvflyers.com/wp-content/uploads/2023/08/Every-Single-Aspect-of-Disney-is-Jewish-1.jpg")
                return

        elif message.content.startswith(',spiderdick'):
                await message.channel.send("Top 10 Most Useless Backflips")
                await message.channel.send("https://media.discordapp.net/attachments/919335494473621564/1100693907605557309/spiderman.gif?ex=667a7a15&is=66792895&hm=c13c551563f7ba4a0876ce29ee10836ec996ba714b14c7a74d0c7c8dbcf4868d&")
                return

        elif message.content.startswith(',credit'):
                await message.channel.send("Original Source Code ; Unknown")
                await message.channel.send("Rewritten And Improved By ; @humbleness")
                return

@client.event
async def on_disconnect():
    if not is_logged_out:
        await client.login(user_token)
        await client.connect()

@client.event
async def on_message_edit(before, after):
    await on_message(after)

@client.event
async def on_message_delete(message):
    await on_message(message)

# Enter Your Token Here
user_token = ''

client.run(user_token, bot=False)