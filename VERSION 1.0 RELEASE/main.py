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

text = """
                                            .▄▄ · ▄▄▄ .▄▄▌  ·▄▄▄▄▄▄▄·       ▄▄▄▄▄
                                            ▐█ ▀. ▀▄.▀·██•  ▐▄▄·▐█ ▀█▪▪     •██  
                                            ▄▀▀▀█▄▐▀▀▪▄██▪  ██▪ ▐█▀▀█▄ ▄█▀▄  ▐█.▪
                                            ▐█▄▪▐█▐█▄▄▌▐█▌▐▌██▌.██▄▪▐█▐█▌.▐▌ ▐█▌·
                                             ▀▀▀▀  ▀▀▀ .▀▀▀ ▀▀▀ ·▀▀▀▀  ▀█▄▀▪ ▀▀▀ 
"""
title = (
    Fore.YELLOW
    + f"""                    
                                                    [github.com/disbuted]
                                                       [Prefix: {Fore.WHITE},cmds{Fore.YELLOW}]{Fore.RESET}"""
)


os.system("cls")
os.system("title ⠀") # blank bar :3
faded_text = fade.fire(text)
print(faded_text)
print(title)
print(
    Fore.YELLOW
    + f"""\n\n                                        Logs Will Be Printed Below Including {Fore.RED}Error Logs{Fore.YELLOW}! \n\n{Fore.RESET}"""
)

owners = {804666654604263425}  # Your / Users UID
user_id = None
guild_id = None
channel_id = None
count = 0
delay = 0.5  # Delay of 1 second
auto_react_emojis = []
react_target_id = None
is_logged_out = False
admins = set()
active_commands = set()
stop_flag = False
last_confirmation = None
cmds_messages = []
ar_target_id = None
ar_message = None
ar_channel_id = None

async def get_user_id():
    user = await client.fetch_user("@me")
    return user.id

@client.event
async def on_ready():
    global user_id
    user_id = await get_user_id()
    print(Fore.GREEN + f"""[LOG] Current User = {client.user} {Fore.RESET}""")


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

    elif message.content.startswith(",fill"):
        spam_enabled = True
        with open("spam.txt", "r") as file:
            spam_message = file.read()
        for _ in range(600000):
            await message.channel.send(spam_message)
            await asyncio.sleep(delay)
    elif message.content.startswith(",setemoji"):
        args = message.content.split()
        if len(args) > 1:
            auto_react_emojis = args[1:]
            await message.channel.send(
                f'Auto-react Emojis Set To: {", ".join(auto_react_emojis)}'
            )
            print(
                Fore.GREEN + f"""[LOG] Auto-React Has Been Ran{Fore.RESET}"""
            )
            
    elif message.content.startswith(",react"):
        if message.content.startswith(",reactstop"):
            react_target_id = None
            await message.channel.send("Auto reaction stopped.")
            print(
                Fore.GREEN + f"""[LOG] Auto Reaction Has Stopped{Fore.RESET}"""
            )
        else:
            if len(message.mentions) == 1:
                target_user = message.mentions[0]
                react_target_id = target_user.id
                await message.channel.send(
                    f"Auto Reaction Target Set To: {target_user.name}"
                )
                
    elif message.content.startswith(",AR"):
        if message.content.startswith(",ARstop"):
            ar_target_id = None
            ar_message = None
            ar_channel_id = None
            await message.channel.send("Auto Respond Stopped.")
            print(
                Fore.GREEN + f"""[LOG] Auto respond Has Stopped{Fore.RESET}"""
            )
        else:
            if len(message.mentions) == 1:
                target_user = message.mentions[0]
                ar_target_id = target_user.id
                ar_channel_id = message.channel.id
                try:
                    with open("ar.txt", "r") as file:
                        ar_message = file.read()
                    await message.channel.send(
                        f"Auto Respond Target Set To: {target_user.name}"
                    )
                except FileNotFoundError:
                    await message.channel.send("Error: ar.txt File Not Found.")
                    print(Fore.RED + f"""[Error] ar.txt Has Not Been Found{Fore.RESET}""")

    elif message.content.startswith(",logout"):
        is_logged_out = True
        await message.channel.send(f"{message.author.mention} Logging Out...")
        print(Fore.GREEN + f"""[LOG] Logging Out Of {client.user} {Fore.RESET}""")
        
        await client.logout()

    global cmds_messages 

    if message.author != client.user:
        return  # ignore other people >:(

    if message.content == ",cmds":
        misc_list = [
            ",cmds : Show Available Commands",
            ",logout : Logout The bot",
            ",credit : Show Credits",
        ]
        chatpacking_list = [
            ",fill : Spam message from spam.txt file 600000 times",
            ",setemoji <emojis> : Set auto-react emojis",
            ",react <@user> : Set auto reaction target user",
            ",reactstop : Stop auto reactions",
            ",AR <@user> : Set auto respond target user and message from AR.txt file",
            ",ARstop : Stop auto respond",
            ",edate : A Lovely Letter For Your Special One",
        ]
        random_list = [
            ",delete <number> : Delete your last <number> messages",
            ",catboy : Credit to **focus** for the original msg",
            ",COMMAND <VAR HERE> : Quick Note :3",
            ",COMMAND <VAR HERE> : Quick Note :3",
            ",COMMAND <VAR HERE> : Quick Note :3",
            ",COMMAND <VAR HERE> : Quick Note :3",
        ]

      #print(Fore.GREEN + f"""[LOG] ,cmds Has Been Run{Fore.RESET}""") idk why i had this?

        for msg in cmds_messages:
            try:
                await msg.delete()
            except discord.NotFound:
                pass  

        cmds_messages.clear()  

        cmds_messages.append(
            await message.channel.send(
                f"```ini\n[Selfbot Misc Commands:]\n{'\n'.join(misc_list)}```"
            )
        )
        cmds_messages.append(
            await message.channel.send(
                f"```ini\n[Selfbot Chatpack Commands:]\n{'\n'.join(chatpacking_list)}```"
            )
        )
        cmds_messages.append(
            await message.channel.send(
                f"```ini\n[Selfbot Random Commands:]\n{'\n'.join(random_list)}```"
            )
        )

    elif message.content.startswith(",catboy"):
        # await message.channel.send("@everyone")
        await message.channel.send(
            "cums on the sleeping catboy I hope he wouldn't mind...\n>////<\nthe catboy wakes up\nhe then forces his little mouseboy to bed in a pronebone position bad mousy... you spilled some on my socks...\n~`//^// ~\nthe catboy puts it in ngaaah...!! ~\n-nyaaa...~ hah~ g-good... boy...~ purr\nohh... f-fuck... ~ I... I love you...! ~\n-unyaaa...~ you... too...!! ~ the catboy paces up each thrust\n-mrrps from pleasure cu- c-cumming...~\nsqueaks from climactic pleasure uuu...~ smooch"
        )
        return

    elif message.content.startswith(",stream"):
        new_status = message.content[8:].strip()
        if new_status:
            await client.change_presence(
                activity=discord.Streaming(
                    name=new_status, url="https://www.twitch.tv/owobotplays"
                )
            )  # some random twitch link (any can go here)
            await message.channel.send(
                f"Streaming Status Changed To: **{new_status}**"
            )
        else:
            await message.channel.send("Please Provide A Status Message.")
            return

    elif message.content.startswith(",edate"):
        # await message.channel.send("@everyone")
        await message.channel.send(
            "can we honestly e date? you’re so beautiful. You always make me laugh, you always make me smile. You literally make me want to become a better person... I really enjoy every moment we spend together. My time has no value unless its spent with you. I tell everyone of my irls how awesome you are. Thank you for being you. Whenever you need someone to be there for you, know that i’ll always be right there by your side. I love you so much. I don’t think you ever realize how amazing you are sometimes. Life isn’t as fun when you’re not around. You are truly stunning. I want you to be my soulmate. I love the way you smile, your eyes are absolutely gorgeous. If I had a star for everytime you crossed my mind i could make the entire galaxy. Your personality is as pretty as you are and thats saying something. I love you, please date me. I am not even calling it e dating anymore because I know we will meet soon enough heart OK I ADMIT IT I LOVE YOU OK i hecking love you and it breaks my heart when i see you play with someone else or anyone commenting in your profile i just want to be your girlfriend and put a heart in my profile linking to your profile and have a walltext of you commenting cute things i want to play video games talk in discord all night and watch a movie together but you just seem so uninsterested in me it hecking kills me and i cant take it anymore i want to remove you but i care too much about you so please i’m begging you to eaither love me back or remove me and never contact me again it hurts so much to say this because i need you by my side but if you dont love me then i want you to leave because seeing your icon in my friendlist would kill me everyday of my pathetic life."
        )
        return

    elif message.content.startswith(",credit"):
        await message.channel.send(f"```ini\n[Credits]```")
        await message.channel.send("https://github.com/disbuted")
        await message.channel.send("https://e-z/bio/£")
        return

    elif message.content.startswith(",delete"):
        global last_confirmation 

    if message.author != client.user:
        return  

    if message.content.startswith(",delete"):
        parts = message.content.split()

        if len(parts) < 2 or not parts[1].isdigit():
            return 

        number = int(parts[1])
        if number <= 0:
            return 

        deleted = 0
        async for msg in message.channel.history(limit=100):
            if msg.author == client.user:
                try:
                    await msg.delete()
                    deleted += 1
                    await asyncio.sleep(0.1)
                except discord.Forbidden:
                    print("Missing permissions to delete messages.")
                    break
                except discord.HTTPException:
                    break

                if deleted >= number:
                    break

        if last_confirmation is not None:
            try:
                await last_confirmation.delete()
            except discord.NotFound:
                pass

      #  last_confirmation = await message.channel.send(f"Deleted {deleted} messages.")

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

@client.event
async def on_message_delete(message):
    global cmds_messages

    if message in cmds_messages:
        for msg in cmds_messages:
            try:
                await msg.delete()
            except discord.NotFound:
                pass

        cmds_messages.clear()

user_token = ("")

client.run(user_token, bot=False)
