import settings
import nextcord
import random
from nextcord.ext import commands
from nextcord import Interaction

'''
This python file has some basic commands for bot
'''
allowed_guilds = [1259471640539037717]

def run():
    # print(settings.DISCORD_API_KEY) // This will print the token of your bot present in .env file
    intents = nextcord.Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents)

    '''
    This will print your bot name and it's ID
    '''
    @bot.event
    async def on_ready():
        print(bot.user)
        print(bot.user.id)

    '''
    This is command
    To use it, enter th prompt !ping in your server with the bot, It will respond with msg 'pong'
    !help ping will print "This is help"
    If enabled is made false, the bot will not accept the command
    '''
    @bot.command(
        help = "This is help",
        enabled = True # If you 
    )   
    async def ping(context):
        await context.send("pong")

    '''
    Usage : !say xyz 
    Output : xyz
    Usage : !say xyz abc
    Output : xyz
    Usage : !say
    Output : What?
    '''
    @bot.command()
    async def say(context, what_to_say = "What?"):
        await context.send(what_to_say)
    
    '''
    Usage : !adv_say abc def ghi
    Output : abc,def,ghi
    Usage : !adv_say
    Output : What?
    '''
    @bot.command()
    async def adv_say(context, *what_to_say):
        if not what_to_say:
            await context.send("What?")
        else:
            await context.send(", ".join(what_to_say))
    
    '''
    This will simply choose an option randomly from the set of options given and print it
    '''
    @bot.command()
    async def random_choice(context, *options):
        if not options:
            await context.send("Give me the options")
        else:
            await context.send(random.choice(options))
    
    @bot.command(pass_context = True)
    async def join(ctx):
        if(ctx.author.voice):
            channel = ctx.message.author.voice.channel
            await channel.connect()
            await ctx.send("I joined the voice channel")
        else:
            await ctx.send("you must be in the voice channel to send that command")

    @bot.command(pass_context = True)
    async def leave(ctx):
        if(ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
            await ctx.send("I left the voice channel")
        else:
            await ctx.send("I am not in the voice channel")

    @bot.event
    async def on_message(message): 
        
        """
        The below line is must for you to process the command
        This function will check if the message == "Hentai"
        if yes then it will delete it, else it will just leave the message and won't check is it a command or not
        if you add the below line it will check for commands after this event is executed
        """
        await bot.process_commands(message) 



    @bot.command()
    async def message(ctx, user:nextcord.Member, *, message=None):
        message = "Welcome to the server"
        embed = nextcord.Embed(title=message)
        await user.send(embed=embed)

    @bot.event
    async def on_reaction_add(reaction, user):
        channel = reaction.message.channel
        message_content = reaction.message.content[:1024]  # Truncate message content to avoid exceeding Discord's limit
        await channel.send(f"{user.name} added: {reaction.emoji} to: {message_content}")

    @bot.slash_command(name="test", description="First slash command", guild_ids = allowed_guilds)
    async def test(interaction : Interaction):
        await interaction.response.send_message("Hello, I am a bot")


    bot.run(settings.DISCORD_API_KEY)

    

if __name__ == "__main__":
    run() 