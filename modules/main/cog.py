import discord
from discord import Option
from discord.ext import commands
from discord.utils import get
import modules.main.queue as q
import modules.main.functions as ff

class SixMans(commands.Cog, name = "6 Mans Cog"):
    
    def __init__(self, client: commands.Bot):
        self.client = client
        self.game_queue = None

    async def join(self, ctx):
        if not ff.check_user(str(ctx.author.id)):
            await ctx.respond("You need to sign up before you are able to join a queue!")
            return
        if self.game_queue == None:
            self.game_queue = q.Queue()
        await self.game_queue.add_player(ctx)
        if len(self.game_queue.players) == 6:
            self.game_queue = None
    
    async def info(self, ctx):
        if self.game_queue == None:
            await ctx.respond("There are currently no open queues.")
        else:
            embed = discord.Embed(title = f"Data for match {self.game_queue.match_id}", color = discord.Color.blue())
            embed.add_field(name = f"Current Members: {len(self.game_queue.players)}", value = '\n'.join([x.mention for x in self.game_queue.players]), inline = False)
            await ctx.respond(embed = embed)

    async def leave(self, ctx):
        if not ff.check_user(str(ctx.author.id)):
            await ctx.respond("You need to sign up before you are able to leave a queue!")
            return
        if self.game_queue == None:
            await ctx.respond("You currently aren't in a queue.")
        else:
            if ctx.author in self.game_queue.players and self.game_queue.in_game == False:
                self.game_queue.players.remove(ctx.author)

                embed = discord.Embed(title = "Player left the queue.", description = f"{ctx.author.mention} has left the queue.", color = discord.Color.orange())
                if len(self.game_queue.players) == 0:
                    embed.add_field(name = "Cancelled queue.", value = "There is nobody in the queue so the queue has been cancelled.", inline = False)
                else:
                    embed.add_field(name = f"Current Members: {len(self.game_queue.players)}", value = '\n'.join([x.mention for x in self.game_queue.players]), inline = False)
                await ctx.respond(embed = embed)
            
            else:
                await ctx.respond("You currently aren't in a queue.")

    
    @commands.slash_command(guild_ids = [640289740738002946], description = 'Registers a user for 6 Mans')
    async def register(self, ctx, name: Option(str, "Choose a name the player will be known as.", required = True)):
        if ff.check_user(str(ctx.author.id)):
            embed = discord.Embed(title = "Error registering player", description = f"{ctx.author.mention} is already registered", color = discord.Color.red())
        else:
            if ff.check_name(name):
                await ctx.respond("A user has already been registered under that name! Please try another")
                return
            ff.create_user(ctx.author, name)
            embed = discord.Embed(title = "Player registered", description = f"{ctx.author.name} has been successfully registered.", color = discord.Color.purple())
        await ctx.respond(embed = embed)
    
    @commands.slash_command(guild_ids = [640289740738002946], description = 'Displays the server 6 Mans Leaderboard')
    async def leaderboard(self, ctx):
        lb_list = ff.create_lb()
        embed = discord.Embed(title = f"{ctx.guild.name} - Leaderboard", description = '\n'.join([f"{lb_list.index(x) + 1}: <@{x[0]}> - `{x[1]}`" for x in lb_list]), color = discord.Color.blue())
        await ctx.respond(embed = embed, ephemeral = True)

    async def clear(self, ctx):
        mod_role = get(ctx.guild.roles, id = 653469368520540203)
        if ctx.author not in mod_role.members:
            await ctx.respond("You do not have access to clear the queue")
            return
        self.game_queue = None
        await ctx.respond("Successfully cleared the queue.")



    @commands.slash_command(guild_ids = [640289740738002946], description = 'Report who won a 6 mans game')
    async def report(self, ctx, game_id, winning_team: Option(str, "Select the team which won the game", choices = ["Team 1", "Team 2"], required = True)):
        mod_role = get(ctx.guild.roles, id = 653469368520540203)
        if ctx.author not in mod_role.members:
            await ctx.respond("You do not have access to report games")
            return
        if not ff.check_games():
            await ctx.respond("There are currently no games available to be reported.")
            return
        await ff.report_game(ctx, f"game {game_id.lower()}", winning_team)


    @commands.slash_command(guild_ids = [640289740738002946], description = 'Queue for a 6 mans game')
    async def q(self, ctx, choice: Option(str, "Please select an option for the queue.", choices = ["join", "leave", "clear", "info"])):
        if choice == 'join':
            await self.join(ctx)
        elif choice == 'leave':
            await self.leave(ctx)
        elif choice == 'clear':
            await self.clear(ctx)
        elif choice == 'info':
            await self.info(ctx)




        
    







            

        



def setup(client: commands.Bot):
    client.add_cog(SixMans(client))