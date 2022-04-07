import discord
from discord.ext import commands, tasks
from discord import Emoji
from time import sleep
import asyncio
import random
import youtube_dl
import json

token = "YOUR TOKEN"

def get_prefix(bot, ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
        return prefixes[str(ctx.guild.id)]

ytdl = youtube_dl.YoutubeDL()
musics = {}
bot = commands.Bot(command_prefix = get_prefix, description = "Epsi's trash python bot", case_insensitive=True)
statuslist = [";help", "Use ;invite to invite me to your server!", "Ping me if you forgot my prefix!", "DM Epsi#0001 if the bot isn't working"]

@bot.remove_command('help')

@bot.event
async def on_ready():
    print("Bot Running")
    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(f"ID: {bot.user.id}")
    print('------')
    status.start()

class Video:
    def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]

@bot.command()
async def play(ctx, url):
    print("someone played a song")
    client = ctx.guild.voice_client

    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
    else:
        channel = ctx.author.voice.channel
        video = Video(url)
        musics[ctx.guild] = []
        client = await channel.connect()
        embed = discord.Embed(title = "**Song added to queue**", description = f"Added {video.url} to queue.")
        embed.set_thumbnail(url = "https://i.ibb.co/JvLK8m2/pfp-casque.png")
        embed.add_field(name = "Requested by:", value = ctx.author.name, inline = True)
        await ctx.send(embed = embed)
        play_song(client, musics[ctx.guild], video)
@bot.command()
async def p(ctx, url):
    print("someone played a song")
    client = ctx.guild.voice_client

    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
    else:
        channel = ctx.author.voice.channel
        video = Video(url)
        musics[ctx.guild] = []
        client = await channel.connect()
        embed = discord.Embed(title = "**Song added to queue**", description = f"Added {video.url} to queue.")
        embed.set_thumbnail(url = "https://i.ibb.co/JvLK8m2/pfp-casque.png")
        embed.add_field(name = "Requested by:", value = ctx.author.name, inline = True)
        await ctx.send(embed = embed)
        play_song(client, musics[ctx.guild], video)
@bot.command()
async def leave(ctx):
    client = ctx.guild.voice_client
    await client.disconnect()
    musics[ctx.guild] = []
    embed = discord.Embed(title = "**Bot disconnected**", description = f"The bot was successfully disconnected from the VC.")
    embed.set_thumbnail(url = "https://i.ibb.co/JvLK8m2/pfp-casque.png")
    embed.add_field(name = "Author:", value = ctx.author.name, inline = True)
    await ctx.send(embed = embed)

@bot.command()
async def resume(ctx):
    client = ctx.guild.voice_client
    if client.is_paused():
        client.resume()
        prefix = get_prefix(bot, ctx)
        embed = discord.Embed(title = "**Song resumed**", description = "Song successfully resumed.")
        embed.set_thumbnail(url = "https://i.ibb.co/JvLK8m2/pfp-casque.png")
        embed.add_field(name = "Author:", value = ctx.author.name, inline = True)
        embed.set_footer(text = f"Type {prefix}pause to pause the song!")
        await ctx.send(embed = embed)

@bot.command()
async def pause(ctx):
    client = ctx.guild.voice_client
    if not client.is_paused():
        client.pause()
        prefix = get_prefix(bot, ctx)
        print(prefix)
        embed = discord.Embed(title = "**Song paused**", description = "Song successfully paused.")
        embed.set_thumbnail(url = "https://i.ibb.co/JvLK8m2/pfp-casque.png")
        embed.add_field(name = "Author:", value = ctx.author.name, inline = True)
        embed.set_footer(text = f"Type {prefix}resume to resume the song!")
        await ctx.send(embed = embed)

@bot.command()
async def skip(ctx):
    client = ctx.guild.voice_client
    client.stop()
    await ctx.send("Song successfully skipped. :white_check_mark:")
@bot.command()
async def s(ctx):
    client = ctx.guild.voice_client
    client.stop()
    await ctx.send("Song successfully skipped. :white_check_mark:")

def play_song(client, queue, song):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url, before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 2"))

    def next(_):
        if len (queue) > 0:
            new_song = queue[0]
            del queue[0]
            play_song(client, queue, new_song)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(source, after=next)




@tasks.loop(seconds = 30, count = 1000)
async def status():
    game = discord.Game(random.choice(statuslist))
    await bot.change_presence(status = discord.Status.online, activity = game)

#@bot.command()                              <- This command isn't working i'll eventually fix it
#async def changestatus(ctx, *args):
#    customstatus = "discord.Status." + str(args)
#    await bot.change_presence(status = customstatus, activity = game)
#    await ctx.send("Bot status successfully changed to" + args)

#@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("An argument is missing. :thinking:")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the required permissions to run this command. :thinking:")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("Whoops, looks like you can't use this command. :thinking:")
    elif isinstance(error.original, discord.Forbidden):
        await ctx.send("Looks like I don't have the required permissions for this command. :thinking:")
    else:
        print(error)

#Help command
@bot.command()
async def help(ctx):
    print("someone asked for help")
    helpfile = open('help.txt', 'r')
    helpmsg = helpfile.read()
    await ctx.send(helpmsg)
@bot.command()
async def cmds(ctx):
    print("someone asked for help")
    helpfile = open('help.txt', 'r')
    helpmsg = helpfile.read()
    await ctx.send(helpmsg)

#Banlist command
@bot.command()
async def banlist(ctx):
    ids = []
    bans = await ctx.guild.bans()
    for i in bans:
        ids.append(str(i.user.id))
    await ctx.send("Here is the banned users list:")
    await ctx.send("\n".join(ids))

#Prefix command

@bot.event
async def on_message(msg):
    mention = f'<@!{bot.user.id}>'
    if mention in msg.content:
        prefix = str(get_prefix(bot, msg))
        yeet = str(f"My prefix here is `{prefix}`. You can change it using the `{prefix}setprefix [prefix]` command. (requires admin). You can also use the `{prefix}resetprefix` command to reset my prefix to default (`;`)")
        embed = discord.Embed(title = "Epsibot Info", description = f"I got pinged!", color=0x000000)
        embed.set_thumbnail(url = "https://i.ibb.co/yqgjCm5/pfp-square.jpg")
        embed.add_field(name = "Prefix", value = str(yeet), inline = True)
        embed.add_field(name = "Requested by:", value = msg.author.name, inline = True)
        embed.set_footer(text = f"Use {prefix}help to see a list of commands!")
        await msg.channel.send(embed = embed)
    await bot.process_commands(msg)

@bot.command()
@commands.has_permissions(add_reactions = True)
async def react(ctx, emoji: Emoji):
    await ctx.message.delete()
    previousmessagelist = await ctx.channel.history(limit=1).flatten()
    print(previousmessagelist)
    previousmessage = previousmessagelist[0]
    await previousmessage.add_reaction(emoji)

#Changelog command
@bot.command()
async def changelog(ctx, *args):
    readlog = open("changelog.txt", "r")
    content = readlog.read()
    content_list = content.splitlines()
    readlog.close()
    embed = discord.Embed(title = content_list[0], description = "Epsibot Changelog", color=0x000000)
    embed.set_thumbnail(url = "https://i.ibb.co/yqgjCm5/pfp-square.jpg")
    embed.add_field(name = content_list[1], value = content_list[2], inline = True)
    embed.add_field(name = content_list[3], value = content_list[4], inline = True)
    embed.add_field(name = "Requested by:", value = ctx.author.name, inline = True)
    embed.set_footer(text = "This bot is still being developed")
    await ctx.send(embed = embed)


#Cooking command
@bot.command()
async def cook(ctx):
    await ctx.send("Send the dish you want to cook. *This command will be cancelled if no dish is entered within 10 seconds.*")

    def checkMessage(message):
        return message.author == ctx.message.author and ctx.message.channel == message.channel

    try:
        recipe = await bot.wait_for("message", timeout = 10, check = checkMessage)
    except:
        await ctx.send("Command cancelled. Please try again.")
        print("someone failed to cook smh")
        return
    message = await ctx.send(f"Your {recipe.content} is going to be prepared. Please confirm by click the ✅ reaction. Else, click the ❌ reaction.")
    await message.add_reaction("✅")
    await message.add_reaction("❌")


    def checkEmoji(reaction, user):
        return ctx.message.author == user and message.id == reaction.message.id and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌")

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout = 10, check = checkEmoji)
        if reaction.emoji == "✅":
            await ctx.send("Recipe successfully started.")
            await asyncio.sleep(random.randint(5,15))
            await ctx.send(f"Your {recipe.content} dish is ready! Thanks for using our services!")
            print(f"someone cooked some {recipe.content}.")
        else:
            await ctx.send("Recipe cancelled.")
            print("someone failed to cook smh")
    except:
        await ctx.send("Recipe cancelled.")
        print("someone failed to cook smh")

#Yo command
@bot.command()
async def yo(ctx):
    print("someone said yo")
    await ctx.send("yoo")

#Hi command
@bot.command()
async def hi(ctx):
    print("someone said hi")
    await ctx.send("hi")

#Bruh command
@bot.command()
async def bruh(ctx):
    print("someone said bruh")
    await ctx.send("https://tenor.com/view/bruh-bye-ciao-gif-5156041")


#Gamer command
@bot.command()
async def gamer(ctx):
    gamermeter1 = str("You are " + str(random.randint(0,100)))
    gamermeter2 = str("%")
    gamermeter3 = str(" epic gamer. :video_game:")
    print("someone is an epic gamer")
    await ctx.send(gamermeter1 + gamermeter2 + gamermeter3)
@bot.command()
async def howgamer(ctx):
    gamermeter1 = str("You are " + str(random.randint(0,100)))
    gamermeter2 = str("%")
    gamermeter3 = str(" epic gamer. :video_game:")
    await ctx.send(gamermeter1 + gamermeter2 + gamermeter3)

#Communist command
@bot.command()
async def communist(ctx):
    cmeter1 = str("You are " + str(random.randint(0,100)))
    cmeter2 = str("%")
    cmeter3 = str(" communist. :red_square:")
    print("someone is communist")
    await ctx.send(cmeter1 + cmeter2 + cmeter3)
    await ctx.send("https://media.tenor.com/images/33e4257056d8a1c64200d2d76ae74f6c/tenor.gif")
@bot.command()
async def howcommunist(ctx):
    cmeter1 = str("You are " + str(random.randint(0,100)))
    cmeter2 = str("%")
    cmeter3 = str(" communist. :red_square:")
    print("someone is communist")
    await ctx.send(cmeter1 + cmeter2 + cmeter3)
    await ctx.send("https://media.tenor.com/images/33e4257056d8a1c64200d2d76ae74f6c/tenor.gif")

#Invite command
@bot.command()
async def invite(ctx):
    print("someone asked for invite link")
    await ctx.send("Here is the invite link for this bot: https://discord.com/api/oauth2/authorize?client_id=780944129202061372&permissions=205385415&scope=bot")
@bot.command()
async def addbot(ctx):
    print("someone asked for invite link")
    await ctx.send("Here is the invite link for this bot: https://discord.com/api/oauth2/authorize?client_id=780944129202061372&permissions=205385415&scope=bot")

#Repeat command
@bot.command()
async def repeat(ctx, *args):
    if "@everyone" in args:
        args = "Don't even try"
        print("they tried to ping @everyone")
    if "@here" in args:
        args = "Don't even try"
        print("they tried to ping @here")
    await ctx.send("{}".format(" ".join(args)))
    print(f"someone asked the bot to repeat {args}")


#Decide command
@bot.command()
async def decide(ctx, *args):
    decisions = ["nah", "yea maybe", "oh hell no", "yup 100%", "of course smh","bruh are you really asking that", "nO", "hell yeah", "yEp", "bruh no"]
    await ctx.send(random.choice(decisions))
    print(f"someone asked the bot to 8ball {args}")
@bot.command(name = '8b')
async def _8b(ctx, *args):
    decisions = ["nah", "yea maybe", "oh hell no", "yup 100%", "of course smh","bruh are you really asking that", "nO", "hell yeah", "yEp", "bruh no"]
    await ctx.send(random.choice(decisions))
    print(f"someone asked the bot to 8ball {args}")
@bot.command(name = "8ball")
async def _8ball(ctx, *args):
    decisions = ["nah", "yea maybe", "oh hell no", "yup 100%", "of course smh","bruh are you really asking that", "nO", "hell yeah", "yEp", "bruh no"]
    await ctx.send(random.choice(decisions))
    print(f"someone asked the bot to 8ball {args}")


#Boldtext command
@bot.command()
async def boldtext(ctx, *text):
    boldChar = "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙"
    boldText = []
    for word in text:
        for char in word:
            if char.isalpha():
                index = ord(char) - ord("a")
                transformed = boldChar[index]
                boldText.append(transformed)
            else:
                boldText.append(char)
        boldText.append(" ")
    boldTextOutput = str(boldText)
    print(boldTextOutput)
    await ctx.send("".join(boldText))
@bot.command()
async def thicctext(ctx, *text):
    boldChar = "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙"
    boldText = []
    for word in text:
        for char in word:
            if char.isalpha():
                index = ord(char) - ord("a")
                transformed = boldChar[index]
                boldText.append(transformed)
            else:
                boldText.append(char)
        boldText.append(" ")
    boldTextOutput = str(boldText)
    print(boldTextOutput)
    await ctx.send("".join(boldText))

#Smalltext command
@bot.command()
async def smalltext(ctx, *text):
    smallChar = "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
    smallText = []
    for word in text:
        for char in word:
            if char.isalpha():
                index = ord(char) - ord("a")
                transformed = smallChar[index]
                smallText.append(transformed)
            else:
                smallText.append(char)
        smallText.append(" ")
    smallTextOutput = str(smallText)
    print(smallTextOutput)
    await ctx.send("".join(smallText))
@bot.command()
async def smallcaps(ctx, *text):
    smallChar = "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
    smallText = []
    for word in text:
        for char in word:
            if char.isalpha():
                index = ord(char) - ord("a")
                transformed = smallChar[index]
                smallText.append(transformed)
            else:
                smallText.append(char)
        smallText.append(" ")
    smallTextOutput = str(smallText)
    print(smallTextOutput)
    await ctx.send("".join(smallText))
        
#Serverinfo command
@bot.command()
async def serverinfo(ctx):
    server = ctx.guild
    textchannelamount = len(server.text_channels)
    voicechannelamount = len(server.voice_channels)
    serverDesc = server.description
    population = server.member_count
    serverName = server.name
    message = f"The server **{serverName}** has **{population}** members. \nServer description: {serverDesc} \nThis server has {textchannelamount} text channels and {voicechannelamount} voice channels."
    await ctx.send(message)
@bot.command()
async def si(ctx):
    server = ctx.guild
    textchannelamount = len(server.text_channels)
    voicechannelamount = len(server.voice_channels)
    serverDesc = server.description
    population = server.member_count
    serverName = server.name
    message = f"The server **{serverName}** has **{population}** members. \nServer description: {serverDesc} \nThis server has {textchannelamount} text channels and {voicechannelamount} voice channels."
    await ctx.send(message)

#Bee movie command
@bot.command()
@commands.has_permissions(ban_members = True)
async def beemovie(ctx):
    beemovie1file = open('beemovie1.txt', 'r')
    beemovie1 = beemovie1file.read()
    beemovie2file = open('beemovie1.txt', 'r')
    beemovie2 = beemovie2file.read()
    beemovie3file = open('beemovie3.txt', 'r')  
    beemovie3 = beemovie3file.read()
    beemovie4file = open('beemovie4.txt', 'r')
    beemovie4 = beemovie4file.read()
    beemovie5file = open('beemovie5.txt', 'r')
    beemovie5 = beemovie5file.read()
    beemovie6file = open('beemovie6.txt', 'r')  
    beemovie6 = beemovie6file.read()
    beemovie7file = open('beemovie7.txt', 'r')
    beemovie7 = beemovie7file.read()
    await ctx.send(beemovie1)
    await ctx.send(beemovie2)
    await ctx.send(beemovie3)
    await ctx.send(beemovie4)
    await ctx.send(beemovie5)
    await ctx.send(beemovie6)
    await ctx.send(beemovie7)
    print("someone asked for the bee movie script smh")
@bot.command()
@commands.has_permissions(ban_members = True)
async def beemoviescript(ctx):
    beemovie1file = open('beemovie1.txt', 'r')
    beemovie1 = beemovie1file.read()
    beemovie2file = open('beemovie1.txt', 'r')
    beemovie2 = beemovie2file.read()
    beemovie3file = open('beemovie3.txt', 'r')  
    beemovie3 = beemovie3file.read()
    beemovie4file = open('beemovie4.txt', 'r')
    beemovie4 = beemovie4file.read()
    beemovie5file = open('beemovie5.txt', 'r')
    beemovie5 = beemovie5file.read()
    beemovie6file = open('beemovie6.txt', 'r')  
    beemovie6 = beemovie6file.read()
    beemovie7file = open('beemovie7.txt', 'r')
    beemovie7 = beemovie7file.read()
    await ctx.send(beemovie1)
    await ctx.send(beemovie2)
    await ctx.send(beemovie3)
    await ctx.send(beemovie4)
    await ctx.send(beemovie5)
    await ctx.send(beemovie6)
    await ctx.send(beemovie7)
    print("someone asked for the bee movie script smh")

#Purge command
@bot.command()
@commands.has_permissions(manage_messages = True)
async def purge(ctx, amount:int):
    messages = await ctx.channel.history(limit = amount + 1).flatten()
    for message in messages:
        await message.delete()
@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount:int):
    messages = await ctx.channel.history(limit = amount + 1).flatten()
    for message in messages:
        await message.delete()
    
#Kick command
@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user : discord.User, *, reason="None"):
    reason = "".join(reason)
    embed = discord.Embed(title = "**Kicked**", description = "Someone got kicked!", color=0x821e1e)
    embed.set_thumbnail(url = "https://i.ibb.co/yqgjCm5/pfp-square.jpg")
    embed.add_field(name = "Kicked member", value = user.name, inline = True)
    embed.add_field(name = "Reason", value = reason, inline = True)
    embed.add_field(name = "Author", value = ctx.author.name, inline = True)
    listt = ['get rekt', 'instant karma', 'begone', 'they deserved it ngl', "lmao what a loser"]
    embed.set_footer(text = random.choice(listt))
    await ctx.send(embed = embed)
    await ctx.guild.kick(user, reason = reason)

#Ban command
@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user : discord.User, *, reason="None"):
    reason = "".join(reason)
    embed = discord.Embed(title = "**Ban**", description = "Someone got banned!", color=0x821e1e)
    embed.set_thumbnail(url = "https://i.ibb.co/yqgjCm5/pfp-square.jpg")
    embed.add_field(name = "Banned member", value = user.name, inline = True)
    embed.add_field(name = "Reason", value = reason, inline = True)
    embed.add_field(name = "Author", value = ctx.author.name, inline = True)
    listt = ['get rekt', 'instant karma', 'begone', 'they deserved it ngl', "lmao what a loser"]
    embed.set_footer(text = random.choice(listt))
    await ctx.send(embed = embed)
    await ctx.guild.ban(user, reason = reason)
#Unban command
@bot.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, user):
    userName, userTag = user.split("#")
    bannedUsers = await ctx.guild.bans()
    for i in bannedUsers:
        if i.user.name == userName and i.user.discriminator == userTag:
            await ctx.guild.unban(i.user)
            await ctx.send(f"{user} was unbanned from this server.")
            return
    await ctx.send("That user isn't in the banned users list. ")
@bot.command()
@commands.has_permissions(ban_members = True)
async def pardon(ctx, user):
    userName, userTag = user.split("#")
    bannedUsers = await ctx.guild.bans()
    for i in bannedUsers:
        if i.user.name == userName and i.user.discriminator == userTag:
            await ctx.guild.unban(i.user)
            await ctx.send(f"{user} was unbanned from this server.")
            return
    await ctx.send("That user isn't in the banned users list. ")

@bot.command()
async def juan(ctx, *args):
    await ctx.send("<:emoji_27:809727205935808542>")

@bot.command()
@commands.is_owner()
async def load(ctx, name=None):
    if name:
        bot.load_extension(name)
        await ctx.send(f"Extension {name} successfully loaded")


@bot.command()
@commands.is_owner()
async def unload(ctx, name=None):
    if name:
        bot.unload_extension(name)
        await ctx.send(f"Extension {name} successfully unloaded")


@bot.command()
@commands.is_owner()
async def reload(ctx, name=None):
    if name:
        try:
            bot.reload_extension(name)
            await ctx.send(f"Extension {name} successfully reloaded")
        except:
            bot.load_extension(name)
            await ctx.send(f"Extension {name} successfully reloaded")

#PREFIX COMMAND PREFIX COMMAND PREFIX COMMAND PREFIX COMMAND PREFIX COMMAND PREFIX COMMAND PREFIX COMMAND PREFIX COMMAND PREFIX COMMAND PREFIX COMMAND PREFIX COMMAND PREFIX COMMAND 

@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = ';'
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@bot.command(aliases=['prefixset', 'prefixchange', 'changeprefix'])
@commands.has_permissions(administrator=True)
async def setprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'Successfully changed the prefix to: **``{prefix}``**')

@bot.command()
@commands.has_permissions(administrator=True)
async def resetprefix(ctx, *args):
    with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = ";"

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'Successfully reset the prefix to: **`;`**')

@bot.command()
@commands.is_owner()
async def reboot(ctx, *args):
    await ctx.channel.send("Rebooting...")
    await bot.logout()
    await bot.login()

@bot.command(
    name='Shutdown',
    description="Shut down the bot and close all connections.",
    brief="Shut down the bot.")
@commands.is_owner()
async def shutdown(ctx, *args):
    await ctx.channel.send("Shutting down...")
    await bot.logout()

bot.run(token)
