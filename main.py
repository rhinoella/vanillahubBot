import discord
from discord.ext import commands, tasks
import requests
import asyncio
import time
import json

server = "vanillahub.net"

bot = commands.Bot(command_prefix='.', help_command=None)


#class to store the time of each command call to manage cooldowns
#allows the startTime to be accessed by every command

class cooldown:
    startTime = 0
    
    @classmethod
    def changeStartTime(cls, start):
        cooldown.startTime = start

    def returnStart(self):
        return self.startTime

commandCooldown = cooldown()

#indicating the bot is online:

@bot.event
async def on_ready():
    botstatus.start()
    print("We have logged in as {0.user}".format(bot))


#getting the status of the server:

resp3 = requests.get(f"https://api.mcsrvstat.us/2/{server}")
onlineStatus = resp3.json()["online"]
if onlineStatus is True:
    print(resp3)
    status_onlineStatus = "Online"
    pingthumbnail = "https://i.imgur.com/ioDEAac.png"
if onlineStatus is False:
    status_onlineStatus = "Offline"
    pingthumbnail = "https://i.imgur.com/9wSMlwl.png"


def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True


#command cooldown to avoid spam

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown, commandCooldown):
        end = time.monotonic()
        start = commandCooldown.returnStart()
        elapsedtime = (end - start)
        sec = round(10 - elapsedtime)
        cooldownMessage = await ctx.send(f"This command is on cooldown, please wait {sec} seconds.")
        await asyncio.sleep(3)
        await cooldownMessage.delete()


#show the player count as the bot's status

@tasks.loop(seconds=20) #refreshes every 20 seconds
async def botstatus():
    resp4 = requests.get(f"https://api.mcsrvstat.us/2/{server}")
    isValid = validateJSON(resp4.text)
    if (isValid == True):
        try:
          playersOnline2 = resp4.json()["players"]["online"]
        except KeyError:
            print("Error querying")
            playersOnline2 = 0
        await bot.change_presence(activity=discord.Game(name=f"VH Players Online: {playersOnline2}"))
    else:
        print("Error connecting to API")


#status command

@bot.command(pass_context=True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def status(ctx, commandCooldown):
    start = time.monotonic()
    commandCooldown.changeStartTime(start)
    resp2 = requests.get(f"https://api.mcsrvstat.us/ping/{server}")
    playersOnline = resp2.json()["players"]["online"]
    embedstatus = discord.Embed(title="__VanillaHub Server Status__", color=0xbbd6ec)
    embedstatus.set_author(name="VanillaHub Bot", icon_url="https://i.imgur.com/rieHwqU.png")
    embedstatus.add_field(name="Status", value=status_onlineStatus, inline=True)
    embedstatus.add_field(name="Players Online", value=f"{playersOnline}/500", inline=True)
    embedstatus.set_thumbnail(url=pingthumbnail)
    if (ctx.channel.id == 775052803835953202 or ctx.channel.id == 795297497336905738): #ensures the user is using the correct channel
        await ctx.channel.send(embed=embedstatus)
    else:
        wrongChannel = await ctx.send("Please only use commands in the #bot-commands channel")
        await asyncio.sleep(3)
        await wrongChannel.delete()


#help command to list all possible commands

@bot.command(pass_context=True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def help(ctx, commandCooldown):
    start = time.monotonic()
    commandCooldown.changeStartTime(start)

    embedinfo = discord.Embed(title="__VanillaHub Bot Help__", description="Try these commands!", color=0xbbd6ec)
    embedinfo.set_author(name="VanillaHub Bot", icon_url="https://i.imgur.com/rieHwqU.png")
    embedinfo.add_field(name=".vote", value="Vote Links", inline=False)
    embedinfo.add_field(name=".status", value="Sever Status", inline=False)
    embedinfo.add_field(name=".ip", value="Server IP", inline=False)
    embedinfo.add_field(name=".store", value="Store Link", inline=False)
    embedinfo.add_field(name=".socials", value="Social Media Links", inline=False)
    embedinfo.add_field(name=".rules", value="VanillaHub Rules", inline=False)
    embedinfo.set_thumbnail(url="https://i.imgur.com/XW5aFYB.png")
    if (ctx.channel.id == 775052803835953202):
        await ctx.send(embed=embedinfo)

    else:
        wrongChannel = await ctx.send("Please only use commands in the #bot-commands channel")
        await asyncio.sleep(3)
        await wrongChannel.delete()


#server voting links

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def vote(ctx, commandCooldown):
    start = time.monotonic()
    commandCooldown.changeStartTime(start)

    embedvote = discord.Embed(title="__VanillaHub Vote Sites__", color=0xbbd6ec)
    embedvote.set_author(name="VanillaHub Bot", icon_url="https://i.imgur.com/rieHwqU.png")
    embedvote.add_field(name="MinecraftServers", value="https://bit.ly/3hEhH5D", inline=False)
    embedvote.add_field(name="Planet Minecraft", value="https://bit.ly/2X3mHan", inline=False)
    embedvote.add_field(name="TopMinecraftServers", value="https://bit.ly/3QwG4Cu", inline=False)
    embedvote.add_field(name="Best Minecraft Servers", value="https://bit.ly/3QvZHuk", inline=False)
    embedvote.add_field(name="Minecraft-MP", value="https://bit.ly/3hDkMCV", inline=False)
    embedvote.set_footer(
        text="Earn in-game rewards from voting!")
    if (ctx.channel.id == 775052803835953202):
        await ctx.send(embed=embedvote)

    else:
        wrongChannel = await ctx.send("Please only use commands in the #bot-commands channel")
        await asyncio.sleep(3)
        await wrongChannel.delete()



#store link

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def store(ctx, commandCooldown):
    start = time.monotonic()
    commandCooldown.changeStartTime(start)
    embedstore = discord.Embed(title="__VanillaHub Store__", description="Buy ranks, packs, and more!",
                               url="https://store.vanillahub.net/", color=0xbbd6ec)
    embedstore.set_author(name="VanillaHub Bot", icon_url="https://i.imgur.com/rieHwqU.png")
    embedstore.set_thumbnail(url="https://i.imgur.com/XW5aFYB.png")
    if (ctx.channel.id == 775052803835953202):
        await ctx.send(embed=embedstore)

    else:
        wrongChannel = await ctx.send("Please only use commands in the #bot-commands channel")
        await asyncio.sleep(3)
        await wrongChannel.delete()


#server ip

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def ip(ctx, commandCooldown):
    start = time.monotonic()
    commandCooldown.changeStartTime(start)
    embedip = discord.Embed(title="__Server IP__", description="vanillahub.net", color=0xbbd6ec)
    embedip.set_author(name="VanillaHub Bot", icon_url="https://i.imgur.com/rieHwqU.png")
    embedip.set_thumbnail(url="https://i.imgur.com/XW5aFYB.png")
    await ctx.send(embed=embedip)


#social media links

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def socials(ctx, commandCooldown):
    start = time.monotonic()
    commandCooldown.changeStartTime(start)
    embedsoc = discord.Embed(title="__VanillaHub Social Media__", color=0xbbd6ec)
    embedsoc.set_author(name="VanillaHub Bot", icon_url="https://i.imgur.com/rieHwqU.png")
    embedsoc.add_field(name="<:insta:795308501902557234> Instagram", value="@vanillahubmc", inline=True)
    embedsoc.add_field(name="<:twitter:795316148333182986> Twitter", value="@vanillahub", inline=True)
    if (ctx.channel.id == 775052803835953202):
        await ctx.send(embed=embedsoc)

    else:
        wrongChannel = await ctx.send("Please only use commands in the #bot-commands channel")
        await asyncio.sleep(3)
        await wrongChannel.delete()

#rules pages

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def rules(ctx, commandCooldown):
    # Rules Page 1:

    start = time.monotonic()
    commandCooldown.changeStartTime(start)

    embedrules = discord.Embed(title="__VanillaHub Rules__", description="See #welcome for discord server rules.",
                               url="https://rules.vanillahub.net/", color=0xbbd6ec)
    embedrules.set_author(name="VanillaHub Bot", icon_url="https://i.imgur.com/rieHwqU.png")
    embedrules.add_field(name="1. No cheats or hacks",
                         value="Cheating can be using modified clients to gain an advantage over others.\nThese include:\n• Xray (includes texture packs)\n• Hacking (such as movement, insta-mine etc.)\n• Alt Abuse (spamming server with bots)\n• Abusing exploits",
                         inline=False)
    embedrules.add_field(name="2. Do not abuse chat for spamming or advertising",
                         value="• Do not spam chat\n• Do not advertise\n• Swearing excessively in public chat isn't allowed\n• CAPS should be kept to a minimum",
                         inline=False)
    embedrules.add_field(name="3. Do not grief",
                         value="• Griefing is never allowed, including unclaimed bases.\n• Do not greif terrain (tnt griefing, cobble monsters etc.)\n• Greifing players' farms is not allowed (killing mobs within them)",
                         inline=False)
    embedrules.add_field(name="4. Do not bypass PVP protections",
                         value="• When PVPing, both parties must have consented\n• No tp killing, kill warps or traps",
                         inline=False)
    embedrules.add_field(name="5. No inappropriate names, skins or builds",
                         value="• Your username must contain no sexual themes, racist or hurtful words\n• Skins must not replicate inappropriate things\n• Renaming items must be appropriate",
                         inline=False)
    embedrules.set_footer(text="React to switch page                           『 1/3 』")

    # Rules Page 2:

    embedrules2 = discord.Embed(title="__VanillaHub Rules__", description="See #welcome for discord server rules",
                                url="https://rules.vanillahub.net/", color=0xbbd6ec)
    embedrules2.set_author(name="VanillaHub Bot", icon_url="https://i.imgur.com/rieHwqU.png")
    embedrules2.add_field(name="6. Do not build or claim next to other bases without consent",
                          value="This can result in your claim being removed by a member of\nstaff. Always ask permission.",
                          inline=False)
    embedrules2.add_field(name="7. Do not talk about sensitive subjects in chat",
                          value="This includes but is not limited to:\n• Politics/disturbing events\n• Suicide\n• Family issues\nWe would like to keep chat friendly and mainly about the game.",
                          inline=False)
    embedrules2.add_field(name="8. Predatory behavior will not be tolerated",
                          value="You can guess what this means.", inline=False)
    embedrules2.add_field(name="9. Do not harass other players",
                          value="This includes:\n• TP request spam\n• Sending unsolicited messages to other players\n• Not leaving a base/claim after being asked to\n• Targeting players",
                          inline=False)
    embedrules2.add_field(name="10. Do not share personal information about players",
                          value="Keep this too private messages and not in public chat.", inline=False)
    embedrules2.set_footer(text="React to switch page                           『 2/3 』")

    # Rules Page 3:

    embedrules3 = discord.Embed(title="__VanillaHub Rules__", description="See #welcome for discord server rules",
                                url="https://rules.vanillahub.net/", color=0xbbd6ec)
    embedrules3.set_author(name="VanillaHub Bot", icon_url="https://i.imgur.com/rieHwqU.png")
    embedrules3.add_field(name="11. Do not impersonate staff members",
                          value="Impersonating staff members is never allowed, such as nick naming\nyourself in game.",
                          inline=False)
    embedrules3.add_field(name="12. Ban evasion is not permitted",
                          value="• Trying to evade a ban will lead to a longer/perm ban\n• If you wish to appeal a ban open a support ticket.",
                          inline=False)
    embedrules3.add_field(name="13. Do not abuse alt accounts",
                          value="This includes:\n• Generating votes\n• Using alts to finish more quests", inline=False)
    embedrules3.add_field(name="14. Respect players and staff",
                          value="Staff are here to enforce rules and maintain a positive environment.\nIf you need more clarity on a rule, please open a ticket.",
                          inline=False)
    embedrules3.set_footer(text="React to switch page                           『 3/3 』")

    rulespages = [embedrules, embedrules2, embedrules3]

#will flip through the pages depending on the user's reaction to the message

    def check(reaction, user):

        return user == ctx.author and str(reaction.emoji) in ['▶', '◀']

    page = 0

    if (ctx.channel.id == 775052803835953202):

        while True:

            reactmessage = await ctx.send(embed=rulespages[(page)])

            right = '▶'
            left = '◀'

            if page == 0:
                await reactmessage.add_reaction(right)

            if page == 1:
                await reactmessage.add_reaction(left)
                await reactmessage.add_reaction(right)

            elif page == 2:
                await reactmessage.add_reaction(left)

            react = await bot.wait_for('reaction_add', check=check)

            if str(react[0]) == left:
                page -= 1

            elif str(react[0]) == right:
                page += 1

            await reactmessage.delete()

    else:
        wrongChannel = await ctx.send("Please only use commands in the #bot-commands channel")
        await asyncio.sleep(3)
        await wrongChannel.delete()

bot.run('''TOKEN''') #token removed for security
