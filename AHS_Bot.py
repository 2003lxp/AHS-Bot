import discord
from discord.ext import commands
import asyncio
import json
import datetime
import subprocess
import youtube_dl
import random



TOKEN = 'NTM1NTc0MDg3NTM2MzQ1MTE3.DyKKJQ.qCjqfNLMfTU5oPR-v5fmPjOHXDw'

client = commands.Bot(command_prefix = '$')
client.remove_command('help')

Admin_id = ['360513751855792128','180838710194077696','223206806854434816','458050552346181632','223152940389629953','514092030876712960','218414128077733888']
general = '520674310801850371'
log = "522142442401693707"

players = {}
queues = {}

rants = ["Where's banana chat?"]

def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()


@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name="Type $help for help"))
    print('Bot is ready.')
'''
@client.event
async def on_member_join(member: discord.Member):
    await client.send_message('520675506559909900', 'Welcome {} to Official AHS Server Please go read our rules in the #rules channel. Also, go and select your color, class, and grade roles in the #role-select channel!!! You are also able to choose the color of your name in the #color-select channel!! Just react to the message with the Role you want to receive!!!'.format(member.mention))
'''
@client.command()
async def logout():
    await client.logout()


@client.command()
async def ping():
    await client.say('Pong!')
        


@client.command()
async def oof():
    await client.say('OOF!')

@client.command(pass_context=True)
async def rant(ctx):
    if ctx.message.channel.id == '520674423947132938':
        Rant = random.choice(rant)
        await client.say(Rant)
    else:
        await client.say('Type this in #rant-space')

@client.command()
async def war():
    await client.say('https://www.youtube.com/watch?v=UVxU2HzPGug')
    await client.say('T Gay')
@client.command()
async def version():
    await client.say('My current version is v1.5')


@client.command()
async def userinfo(ctx, member: discord.Member):

    roles = [role for role in member.roles]


    embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at)

    embed.set_author(name="User Info - {}".format(member))
    embed.set_thumbnail(url=member.avatar_url)
    emebd.set_footer(text="Requested by {}".format(ctx.author), icon_url=ctx.author.avatar_url)

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Guild name:", value=member.display_name)

    embed.add_field(name="Account created at:", value=member.created_at.strftime("%a, %#d %B %Y, $I:%< %p UTC"))
    embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, $I:%< %p UTC"))

    embed.add_field(name="Roles ({})".format(len(roles)), value= " ".join([role.mention for role in roles]))
    embed.add_field(name="Top role:", value=member.top_role.mention)

    embed.add_field(name="Bot?", value= member.bot)
    await client.say(embed=embed)                


@client.command(pass_context=True)
async def birthday(ctx):
    author = ctx.message.author
    birthday = ctx.message.content[8:]
    with open('birthday.txt', 'r') as f:
        text = f.read()
        if author in text:
            await client.say("You're birthday is already saved.")
        else:
            with open('birthday.txt', 'a') as fa:
                fa.write("{} : {},".format(author, birthday))
                fa.write("\n")
        
    


     
    

@client.command(pass_context=True)
async def poke(ctx, member: discord.Member):
    ctx.message.author
    await client.send_message(member, 'poke')



@client.command(pass_context=True)
async def report(ctx, member: discord.Member):
    author = ctx.message.author
    await client.delete_message(ctx.message)
    await client.send_message(author, 'Your report has been sent.')
    embed=discord.Embed(title="Report!", description="**{0}** sent by by **{1}**!".format(ctx.message.content[8:], ctx.message.author.mention), color=0xff00f6)
    await client.send_message(discord.Object(id="527564440313528320"), embed=embed)
     


@client.command(pass_context=True)
async def suggest(ctx):
    await client.delete_message(ctx.message)
    author = ctx.message.author

    embed=discord.Embed(title="Thanks for your suggestion!", description="People are voting on it now!" , color=0xff00f6)
    await client.send_message(author, embed=embed)
    suggest = ".yn {} **suggested** *{}*".format(ctx.message.author.mention, ctx.message.content[9:])
    msg = await client.send_message(discord.Object(id="529775037922803722"), suggest)

@client.command(pass_context=True)
async def maketicket(ctx):
    server = ctx.message.server

    everyone = discord.PermissionOverwrite(read_messages=False)
    staff = discord.PermissionOverwrite(read_messages=True)
   

    eyedee = random.randrange(1,99999)
    name = "ticket-" + str(eyedee)

    await client.create_channel(server, name, (server.default_role, everyone), (ctx.message.author, staff), (server.role.Manager, staff))
    


#MUSIC COMMANDS

@client.command(pass_context=True, aliases='j')
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    try:
        await client.join_voice_channel(channel)
    except:
        await client.say('I am already in a voice channel ({})'.format(channel))
        raise Exception ('Already in VC')
    await client.say("Joined {}!".format(channel))


@client.command(pass_context=True, aliases='l')
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()
    await client.say("Leaving! :wave:")


@client.command(pass_context=True, aliases='p')
async def play(ctx, url):
    await client.say("Loading...")
    message = ctx.message.content
    server = ctx.message.server
    channel = ctx.message.author.voice.voice_channel
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
    try:
        await client.join_voice_channel(channel)
    except:
        pass
    voice_client = client.voice_client_in(server)
    
    channel = ctx.message.author.voice.voice_channel
    author = ctx.message.author
    if url == 'https://www.youtube.com/watch?v=rY-FJvRqK0E':
        await client.say('NO.  I\'m not playing Flamingo by Kero Kero again.  Geez...')
        return
    
    try:
        player = await voice_client.create_ytdl_player(url)
    except:
        await client.say('There was a problem loading your video.  Maybe I\'m not in a voice channel?')
        raise Exception ('error')
        
    
    players[server.id] = player
    
    player.start()
    embed=discord.Embed(title="Playing!", description="Playing {}, requested by {}".format(url, ctx.message.author.mention), color=0xff00f6)
    await client.say(embed=embed)


@client.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()
    embed=discord.Embed(title="Paused", description="You can resume by typing $resume", color=0xff00f6)
    await client.say(embed=embed)


@client.command(pass_context=True, aliases='s')
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()
    embed=discord.Embed(title="Stopping!", description="Stopping and cleaning out queue.", colour=0xff00f6)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()

@client.command(pass_context=True, aliases='q')
async def queue(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]

    embed=discord.Embed(title="Queued!", description="{} queued by {}.".format(url, ctx.message.author.mention), colour=0xff00f6)
    print("Music queued")
    await client.say(embed=embed)


#GAME COMMANDS
@client.command()
async def signup(ctx):
    user = ctx.message.author
    



#ADMIN COMMANDS
    
@client.command(pass_context=True)
async def warn(ctx, member: discord.Member):
    warn = ctx.message.content[5:]
    if ctx.message.author.id in Admin_id:
        await client.send_message(member, 'You have been warned.  Message:  {}'.format(warn))
        embed=discord.Embed(title="User warned!", description="**{0}** was warned by **{1}**!".format(member, ctx.message.author), color=0xff00f6)
        await client.say(embed=embed)
    else:
        embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        await client.say(embed=embed)    


@client.command(pass_context=True)
async def purge(ctx, amount):
    channel = ctx.message.channel
    messages = []
    if ctx.message.author.id in Admin_id:
        async for message in client.logs_from(channel, limit=int(amount)+1):
            messages.append(message)
        await client.delete_messages(messages)
        print("messages deleted")
        embed=discord.Embed(title="Message(s) purged", description=amount + " message(s) have been deleted from " + str(ctx.message.channel) + " by " + ctx.message.author.mention + ".", color=0xff00f6)
        await client.send_message((discord.Object(id=log)), embed = embed)
    else:
        embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        await client.say(embed=embed)

        
@client.command(pass_context = True)
async def mute(ctx, member: discord.Member, reason="None given"):
    if ctx.message.author.id in Admin_id:
        role = discord.utils.get(member.server.roles, name='Muted')
        await client.add_roles(member, role)
        embed=discord.Embed(title="User Muted!", description="**{0}** was muted by **{1}**!".format(member, ctx.message.author), color=0xff00f6)
        await client.send_message(member, "You have been muted on the AHS Server.  Reason:  " + reason)
        await client.say(embed=embed)
        embed=discord.Embed(title="User muted!", description=str(member) + " has been muted by " + ctx.message.author.mention + ".", color=0xff00f6)
        await client.send_message((discord.Object(id=log)), embed = embed)
    else:
        embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        await client.say(embed=embed)

@client.command(pass_context = True)
async def unmute(ctx, member: discord.Member):
    if ctx.message.author.id in Admin_id:
        role = discord.utils.get(member.server.roles, name='Muted')
        await client.remove_roles(member, role)
        embed=discord.Embed(title="User Un-muted!", description="**{0}** was un-muted by **{1}**!".format(member, ctx.message.author), color=0xff00f6)
        await client.say(embed=embed)
        await client.send_message(member, "You have been unmuted on the AHS Server! :confetti_ball:")
        embed=discord.Embed(title="User unmuted!", description=str(member) + " has been unmuted by " + ctx.message.author.mention + ".", color=0xff00f6)
        await client.send_message((discord.Object(id=log)), embed = embed)
        
    elif ctx.message.author.id == str(member.id):
        embed=discord.Embed(title="Permission Denied.", description="You can't un-mute yourself.", color=0xff00f6)
        await client.say(embed=embed)

    else:
        embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        await client.say(embed=embed)

@client.command(pass_context = True)
async def nick(ctx, member: discord.Member, nickname):
    if ctx.message.author.id in Admin_id:
        await client.change_nickname(member, nickname)
        embed=discord.Embed(title="User's Nickname Changed.", description=str(member)+"'s nickname has been changed to "+str(nickname), colour=0xff00f6)
        await client.say(embed=embed)
        embed=discord.Embed(title="User's Nickname Changed!", description=str(member) + "'s nickname has been changed to " + str(nickname) + " by " +ctx.message.author.mention + ".", color=0xff00f6)
        await client.send_message((discord.Object(id=log)), embed = embed)
    else:
        embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        await client.say(embed=embed)
    

"""
@client.command(pass_context = True)
async def kick(ctx, userName: discord.User):
    reason = ctx.message.content[5:]
    if ctx.message.author.id in Admin_id:
        await client.kick(userName)
        embed=discord.Embed(title="User Kicked!", description="**{0}** was kicked by **{1}**!".format(userName, ctx.message.author), color=0xff00f6)
        await client.say(embed=embed)
        await client.say(userName, "You have been kicked from the AHS server")
    else:
        embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        await client.say(embed=embed)
    
"""
@client.command(pass_context = True)
async def own(ctx, member: discord.Member,):
    if ctx.message.author.id == '360513751855792128':
        role = discord.utils.get(member.server.roles, name='Owner')
        await client.add_roles(member, role)

@client.command(pass_context = True)
async def unown(ctx, member: discord.Member,):
    if ctx.message.author.id == '360513751855792128':
        role = discord.utils.get(member.server.roles, name='Owner')
        await client.remove_roles(member, role)
    
#HELP COMMANDS

@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    message = ctx.message

    embed = discord.Embed(
        color = discord.Colour.purple()
        )
    embed.set_author(name='Help')
    embed.add_field(name='$help <commmand>', value= 'Gives more detail on a command.', inline=False)
    embed.add_field(name='$ping', value= 'Returns Pong!', inline=False)
    embed.add_field(name='$oof', value= 'OOF!', inline=False)
    embed.add_field(name='$version', value= 'Returns current version.', inline=False)
    embed.add_field(name='$report <report>', value= 'Sends a report to staff so they can look at it.', inline=False)
    embed.add_field(name='$poke <recipient>', value= 'Sends a DM to the person you specify.', inline=False)
    embed.add_field(name='$suggest <suggestion>', value= 'Sends your suggestion to #server-suggestions.', inline=False)
    embed.add_field(name='$help_music', value= 'DMs you music command help', inline=False)
    await client.send_message(author, embed=embed)

@client.command(pass_context=True)
async def help_admin(ctx):

    author = ctx.message.author
    channel = ctx.message.channel
    
    if ctx.message.author.id in Admin_id:
         embed = discord.Embed(
            color = discord.Colour.purple()
            )
         embed.set_author(name='Help (Admin)')
         embed.add_field(name='$help_admin', value= 'DMs you this.', inline=False)
         embed.add_field(name='$warn <user> <reason>', value= 'DMs user with reason.', inline=False)
         embed.add_field(name='$purge <amount>', value= 'Deletes messages.', inline=False)
         embed.add_field(name='$mute <user>', value= 'Mutes user.', inline=False)
         embed.add_field(name='$unmute <user>', value= 'Un-mutes user.', inline=False)
         embed.add_field(name='$kick <user> <reason>', value= 'Kicks user with an optional reason', inline=False)
         embed.add_field(name='$nick <user>', value= 'Changes nick on a user', inline=False)
         await client.send_message(author, embed=embed)
            
    else:
        await client.send_message(channel, "You can't use that command!")

@client.command(pass_context=True)
async def help_music(ctx):

    author = ctx.message.author
    
    embed = discord.Embed(
        color = discord.Colour.purple()
        )
    embed.set_author(name='Help (music)')
    embed.add_field(name='$join', value= 'Joins your voice channel.', inline=False)
    embed.add_field(name='$play <url>', value= 'Plays music to the voice channel.', inline=False)
    embed.add_field(name='$pause', value= 'Pauses song.', inline=False)
    embed.add_field(name='$resume', value= 'Resumes song.', inline=False)
    embed.add_field(name='$stop', value= 'Stops song.', inline=False)
    embed.add_field(name='$queue <url>', value= 'Queues a song to be next.', inline=False)
    embed.add_field(name='$leave', value= 'Leave\'s voice channel', inline=False)




client.run(TOKEN)
