import settings
import nextcord
import random
import requests
import json
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions, MissingPermissions
from nextcord import member
from nextcord import Interaction
import google.generativeai as genai
import requests
from requests import get

genai.configure(api_key=settings.GEMINIAI)
allowed_guilds = [1259471640539037717]
codeforces_api = "https://codeforces.com/api/"

"""
Template code of gemini
"""
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
  ]
)

# print(settings.DISCORD_API_KEY) // This will print the token of your bot present in .env file
intents = nextcord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("all set, let's goo!")

"""
on_message is an inbuilt function which reads the message send by users in the channel
"""

@bot.command()
async def embed(ctx):
    EMBED = nextcord.Embed(title="Dog", url="https://www.google.com/", description="We love dogs!")
    EMBED.set_author(name=ctx.author.display_name, url=None, icon_url=ctx.author.avatar.url)
    EMBED.set_thumbnail(url="https://fastly.picsum.photos/id/933/200/300.jpg?grayscale&hmac=wkdO1SD8vr6yRv8wL9FoigKhNuXVNtLAEp_aS1JLfzg")
    EMBED.add_field(name="codeforces", value="1800", inline=True)
    EMBED.add_field(name="codechef", value="2000", inline=True)
    EMBED.set_footer(text="Thank you")
    await ctx.send(embed=EMBED)

"""
Input: !gemini {message}

Output: Response recieved from gemini
"""
@bot.command()
async def gemini(ctx, *message):
    user_message = (" ").join(message)
    p = chat_session.send_message(user_message)
    answer = p.candidates[0].content.parts[0].text
    await ctx.send(answer)

"""
Input: !pbset {contestId} {index_list} {count}

{contestId} : The id at the end of contest URL . Ex: https://codeforces.com/contest/1886 => contestId = 1886
{index_list} : a string of problem number . Ex: In contest having A, B1, B2, C, D, E1, E2 if you want A, B2, E1 => index_list = 136
{count} : number of problems you want . Ex : count = 10, returns a set of 10 problems

Output:
Embed with Links to {count} number of problems, If {count} not given then 5 problems will be sent
"""
@bot.command()
async def pbset(ctx, contestId, index_list, count=5):
    print("pbset")
    contestproblems = []
    url = codeforces_api + "problemset.problems?tags=" 
    response = get(url)
    data = response.json()
    for problem in data['result']['problems']:
        if(int(problem['contestId']) == int(contestId)):
            contestproblems.append(problem)

    contestproblems = contestproblems[::-1]
    required_problems = []
    for i in index_list:
        if i<'1' or i >'9' or (int(i)-1 >= len(contestproblems)):
            await ctx.send("Invalid problem numbers")
        required_problems.append(contestproblems[int(i)-1])
        
    tags = []
    ratings = []
    for problem in required_problems:
        ratings.append(problem['rating'])
        for tag in problem['tags']:
            tags.append(tag)
    tags = set(tags)    
    
    avg_rating = sum(ratings)/len(ratings)

    if(avg_rating > 2000):
        avg_rating = 2200
    elif(avg_rating > 1800):
        avg_rating = 2000
    elif(avg_rating > 1600):
        avg_rating = 1800
    else:
        avg_rating =1600
        
    problemset = []

    for problem in data['result']['problems']:
        if 'rating' in problem and (problem['rating'] == avg_rating):
            if all(element in tags for element in problem['tags']):
                problemset.append(problem)
    
    indices = random.sample(range(0,len(problemset)), int(count))

    problemset = [problem for i, problem in enumerate(problemset) if i in indices]

    embed = nextcord.Embed(title="Upsolve set", description="Test your understanding, Happy Learning!", color=nextcord.Color.green())
    i = 1
    for problem in problemset:
        url = "https://codeforces.com/problemset/problem/" + str(problem['contestId']) + "/" + str(problem['index'])
        embed.add_field(name=f"Problem {i}", value=url, inline=False)
        i += 1

    user = ctx.author
    user = ctx.guild.get_member(user.id)
    await user.send(embed=embed)
    await ctx.send("The problem set has been sent")

"""
input : /cfget {category} {rating}

{category} : If you are intrested in some topic like greedy, dp etc, else enter "any"
{rating} : Specify rating . Ex: 1600, 2000 etc.

Output:
Embed with a random problem of your interest
"""

@bot.slash_command(name="cfget",
                description="This will return a random problem taken from the codeforces problem set based on your specifications", 
                guild_ids = allowed_guilds)
async def cfget(interaction : nextcord.Interaction, category, rating):
    url = codeforces_api + "problemset.problems?tags=" 
    if(category != "any") :
        url = url + category
    response = get(url)  # Use await for asynchronous operations
    data = response.json()  # Now you can call json() after await
    filtered_problems = []
    for problem in data['result']['problems']:
        if 'rating' in problem and problem['rating'] == int(rating):
            filtered_problems.append(problem)
    if(len(filtered_problems) == 0):
        await interaction.response.send_message("No problem with such rating or tag")
    random_problem_index = random.randint(0,len(filtered_problems)-1)
    index = str(filtered_problems[random_problem_index]['index'])
    contestID = str(filtered_problems[random_problem_index]['contestId'])
    name = str(filtered_problems[random_problem_index]['name'])
    
    embed = nextcord.Embed(title=index+" "+name,url="https://codeforces.com/problemset/problem/" + contestID + "/" + index,description="codeforces problem")

    await interaction.response.send_message(embed=embed)

bot.run(settings.DISCORD_API_KEY)



