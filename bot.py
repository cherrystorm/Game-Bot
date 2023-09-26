import discord
import random
from discord.ext import commands

TOKEN = ''

# # Create a bot instance with a command prefix
# intents = discord.Intents.default()
# intents.members = True
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


# # Event handler for when the bot is ready
@bot.event
async def on_ready():
    # print("The bot is now online")
    print(f'Logged in as {bot.user.name}')

# # Command to divide users into two voice channels
@bot.command()
async def start(ctx):
    # Get the server (guild) where the command was executed
    
    server = ctx.guild

    # Check if the voice channels already exist
    voice_channel1 = discord.utils.get(server.voice_channels, name='Alpha 1')
    voice_channel2 = discord.utils.get(server.voice_channels, name='Alpha 2')

    # Create two voice channels
    if not voice_channel1:
        voice_channel1 = await server.create_voice_channel('Alpha 1')
        
    if not voice_channel2:
        voice_channel2 = await server.create_voice_channel('Alpha 2')
        
    # Get all members in the server
    members = server.members
    mem = []
    members_list = []
    alpha1 = []
    alpha2 = []
    count = 0

    for i in range(len(members)):
        mem.append(members[i].name)


    # Divide members into the two voice channels
    while(count < len(mem)):
        ran_mem = random.choice(mem)
        if ran_mem not in members_list:
            if(count % 2 == 0):
                alpha1.append(ran_mem)
                count = count + 1
            else:
                alpha2.append(ran_mem)
                count = count + 1
            members_list.append(ran_mem)
        else:
            continue
        
    #alpha1 group creation
    for alpha1_name in alpha1:
        for member in members:
            if ((alpha1_name == member.name) and (member.bot == False) and member.voice and member.voice.channel):
                await member.move_to(voice_channel1)
    
    #alpha2 group creation
    for alpha2_name in alpha2:
        for member in members:
            if ((alpha2_name == member.name) and (member.bot == False) and member.voice and member.voice.channel):
                await member.move_to(voice_channel2)
                
    
            
@bot.command()
async def end(ctx):
    # Get the server (guild) where the command was executed
    server = ctx.guild

    # Get the "General" voice channel (you can change the name as needed)
    general_channel = discord.utils.get(server.voice_channels, name='General')

    if not general_channel:
        await ctx.send('General voice channel not found.')
        return

    # Loop through all voice channels and move members to the "General" channel
    for channel in server.voice_channels:
        for member in channel.members:
            try:
                await member.move_to(general_channel)
            except discord.Forbidden:
                await ctx.send(f"Couldn't move {member.display_name} from {channel.name} to General (permission issue).")


# # Replace 'YOUR_BOT_TOKEN' with your bot's token
bot.run(TOKEN)