import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json
import os




### --- YOUR DATA HERE --- ###
guild_id = YOUR_GUILD_ID
bot_token = "YOUR_BOT_TOKEN"
### ---------------------- ###





intents = discord.Intents.all()
intents.members = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix='_', intents=intents, case_insensitive=True)

channels = {}
with open(os.path.dirname(__file__) + '/proposal.json', 'r') as file:
    js = json.load(file)
    channels = js
    
print("Bot starting...")

@bot.event
async def on_ready():
    global guild_id
    global channels
    bot_guild = None
    for guild in bot.guilds:
        if guild.id == guild_id:
            await bot.register_application_commands(guild=guild)
            bot_guild = guild
    print(f"\nLogged in as {bot.user}\n")
    print("Guilds:")
    for guild in bot.guilds:
        print(f"- {guild.name} (id: {guild.id})")
    print("\nChannels:")
    for channel in channels:
        print(f"- {channel}: #{discord.utils.get(bot_guild.text_channels, id=channels[channel]).name} (id: {channels[channel]})")


@bot.listen()
async def on_component_interaction(interaction):
    member = interaction.user
    if interaction.custom_id.startswith("proposal"):
        msg = interaction.message
        if interaction.custom_id == "proposal-accept":
            channel = discord.utils.get(interaction.guild.text_channels, id=channels.get("Accepted"))
            embed = interaction.message.embeds[0]
            embed.remove_footer()
            await channel.send(embed=embed)
            components = discord.ui.MessageComponents(
                    discord.ui.ActionRow(
                    discord.ui.Button(label=f"Accepted by {member.name}#{member.discriminator}", custom_id="proposal-accept" , style=discord.ui.ButtonStyle.success, disabled=True),
                    discord.ui.Button(emoji="🗑️", custom_id="proposal-delete", style=discord.ui.ButtonStyle.danger, disabled=False),
                )
            )
            await interaction.response.edit_message(components=components)
        elif interaction.custom_id == "proposal-deny":
            components = discord.ui.MessageComponents(
                    discord.ui.ActionRow(
                    discord.ui.Button(label="Accept", custom_id="proposal-accept" , style=discord.ui.ButtonStyle.secondary, disabled=True),
                    discord.ui.Button(label="Deny", custom_id="proposal-deny", style=discord.ui.ButtonStyle.secondary, disabled=True),
                    discord.ui.Button(emoji="🗑️", custom_id="proposal-delete", style=discord.ui.ButtonStyle.danger),
                    discord.ui.Button(emoji="♻️", custom_id="proposal-reopen", style=discord.ui.ButtonStyle.success),
                )
            )
            embed = interaction.message.embeds[0]
            footer = ""
            if embed.footer.text is not embed.Empty:
                footer = embed.footer.text
            embed.set_footer(text=footer + f"\n❌ {member.name}#{member.discriminator}")
            await interaction.response.edit_message(components=components, embed=embed)
        elif interaction.custom_id == "proposal-delete":
            await interaction.message.delete()
        elif interaction.custom_id == "proposal-reopen":
            components = discord.ui.MessageComponents(
                    discord.ui.ActionRow(
                    discord.ui.Button(label="Accept", custom_id="proposal-accept" , style=discord.ui.ButtonStyle.success, disabled=False),
                    discord.ui.Button(label="Deny", custom_id="proposal-deny", style=discord.ui.ButtonStyle.danger, disabled=False),
                )
            )
            embed = interaction.message.embeds[0]
            footer = ""
            if embed.footer.text is not embed.Empty:
                footer = embed.footer.text
            embed.set_footer(text=footer + f"\n♻️ {member.name}#{member.discriminator}")
            await interaction.response.edit_message(components=components, embed=embed)


@bot.command(    
    application_command_meta=commands.ApplicationCommandMeta(
        options=[
            discord.ApplicationCommandOption(
                name="channel",
                type=discord.ApplicationCommandOptionType.channel,
                description="Select the channel."
            ),
            discord.ApplicationCommandOption(
                name="type",
                choices=[
                    discord.ApplicationCommandOptionChoice(name="Type: Proposals", value="Proposal"),
                    discord.ApplicationCommandOptionChoice(name="Type: Queue", value="Queue"),
                    discord.ApplicationCommandOptionChoice(name="Type: Accepted", value="Accepted")
                ],
                type=discord.ApplicationCommandOptionType.string,
                description="The type of the channel."
            )
        ]
    )
)
@has_permissions(administrator=True)
async def proposal(ctx, channel, type: str):
    global channels
    channels[type] = int(channel)
    js = json.dumps(channels, indent = 4)
    with open(os.path.dirname(__file__) + '/proposal.json', 'w') as file:
        file.write(js)
    await ctx.send(f"<a:success:937438369984708678> **<#{channel}>** is now the `{type}` channel!", ephemeral=True)
    text = "```" \
            "You can send in your suggestions/proposals here, which will then be checked.\n"\
            "If these work, they will be posted to the respective channel with your name.\n"\
            "e.g. in the #accepted Channel.\n\n"\
            "The message you send here will be automatically deleted.```"
    if type == "Proposal":
        proposal_channel = discord.utils.get(ctx.guild.text_channels, id=channels.get("Proposal"))
        await proposal_channel.send(text)

    
@bot.listen()
async def on_message(message):
    if message.author.bot:
        return
    global channels
    channel = message.channel
    # Verify that the channel belongs to the PROPOSAL System.
    if channel.id in channels.values():
        """
        
        The Bot will get the messages out of this channel and sends it 
        to the "Queue" Channel you've set before.
        
        - Proposal Channel should be available to all or selected users.
        - Queue Channel should be only available to staff members
            -> They decide which proposal is good and which not.
        - Accept Channel will get all accepted messages from the Queue Channel.
        
        """
        
        if channels["Proposal"] == channel.id:
            member = message.author
            queue = discord.Embed(title=" ", description=message.content, color=0x036ffc) 
            queue.set_author(name=f"{member.name}#{member.discriminator}", icon_url=member.avatar.url)
            queue_channel = discord.utils.get(message.guild.text_channels, id=channels.get("Queue"))
            components = discord.ui.MessageComponents(
                    discord.ui.ActionRow(
                    discord.ui.Button(label="Accept", custom_id="proposal-accept" , style=discord.ui.ButtonStyle.success),
                    discord.ui.Button(label="Deny", custom_id="proposal-deny", style=discord.ui.ButtonStyle.danger),
                )
            )
            await queue_channel.send(embed=queue, components=components)
            await message.delete()
    

bot.run(bot_token)
