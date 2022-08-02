import discord
import modules.main.voting_category as vr
import modules.main.voting_captains_one as vco
import modules.main.voting_captains_two as vct
import modules.main.functions as ff

class Queue():
    def __init__(self):
        self.match_id = ff.get_match_id()
        self.players = []
        self.team_one = []
        self.team_two = []
        self.remaining_players = []
        self.captain_one = None
        self.captain_two = None
        self.in_game = False
        self.category = None
    
    async def add_player(self, ctx):
        if len(self.players) < 7:
            if ctx.author in self.players:
                await ctx.respond("You are already in queue!", ephemeral = True)
                return
            self.players.append(ctx.author)
            await self.make_embed(ctx)
            if len(self.players) == 6:
                self.in_game = True
                voting = vr.VotingButton(self.players)
                await ctx.respond(f"6 People have joined the queue. {' '.join([x.mention for x in self.players])}\nPlease vote for either captains or for random teams.", view = voting)
                await voting.wait()               

                if voting.decision == 'random':
                    self.category = 'random'
                    await self.make_random_teams(ctx)
                elif voting.decision == 'captains':
                    self.category = 'captains'
                    await self.make_captains_teams(ctx)
                elif voting.decision == 'balanced':
                    self.category = 'balanced'
                    await self.make_balanced_teams(ctx)


    async def make_random_teams(self, ctx):
        self.team_one, self.team_two = await ff.make_random_teams(self.players)
        embed = discord.Embed(title = "Match ID", description = self.match_id, color = discord.Color.green())
        embed.add_field(name = "Team 1", value = ' '.join([x.mention for x in self.team_one]), inline = False)
        embed.add_field(name = "Team 2", value = ' '.join([x.mention for x in self.team_two]), inline = False)
        await ctx.send(embed = embed)
        ff.write_match(self)


    async def make_balanced_teams(self, ctx):
        self.team_one, self.team_two = ff.balance_teams(self.players)
        data = ff.load_dict('player_data.json')
        embed = discord.Embed(title = "Match ID", description = self.match_id, color = discord.Color.green())
        embed.add_field(name = "Team 1", value = ' '.join([f"<@{data[x]['user_id']}>" for x in self.team_one]), inline = False)
        embed.add_field(name = "Team 2", value = ' '.join([f"<@{data[x]['user_id']}>" for x in self.team_two]), inline = False)
        await ctx.send(embed = embed)
        ff.write_match(self)


    async def make_captains_teams(self, ctx):
        self.captain_one, self.captain_two, self.team_one, self.team_two = await ff.get_captains(self.players)
        self.remaining_players = [self.players[x] for x in range(len(self.players)) if x != 0 and x != 1]

        #Get first pick
        player_data = ff.get_captain_picks_data(self.remaining_players)
        embed = discord.Embed(title = "Please pick a player to be on your team.", description = '\n'.join([f"Player {index + 1}: {x[0].mention} - {x[1]}" for index, x in enumerate(player_data)]),color = discord.Color.blue())
        first_pick = vco.VotingButton(self.remaining_players, self.captain_one)
        await self.captain_one.send(embed = embed, view = first_pick)
        await first_pick.wait()
        self.team_one.append(first_pick.choice)
        self.remaining_players.remove(first_pick.choice)

        #Get second pick
        player_data = ff.get_captain_picks_data(self.remaining_players)
        embed = discord.Embed(title = "Please pick a player to be on your team.", description = '\n'.join([f"Player {index + 1}: {x[0].mention} - {x[1]}" for index, x in enumerate(player_data)]),color = discord.Color.blue())
        second_pick = vct.VotingButton(self.remaining_players, self.captain_two)
        await self.captain_two.send(embed = embed, view = second_pick)
        await second_pick.wait()
        for x in range(len(second_pick.choice)):
            self.team_two.append(second_pick.choice[x])
            self.remaining_players.remove(second_pick.choice[x])
        self.team_one.append(self.remaining_players[0])

        #Create embed
        embed = discord.Embed(title = "Match ID", description = self.match_id, color = discord.Color.green())
        embed.add_field(name = "Team 1", value = ' '.join([x.mention for x in self.team_one]), inline = False)
        embed.add_field(name = "Team 2", value = ' '.join([x.mention for x in self.team_two]), inline = False)
        await ctx.send(embed = embed)
        ff.write_match(self)


                
    async def make_embed(self, ctx):
        if len(self.players) == 1:
            embed = discord.Embed(title = "New queue started!", description = f"{self.players[0].mention} has started a new queue!", color = discord.Color.blue())
        else:
            embed = discord.Embed(title = "Player joined the queue", color = discord.Color.blue())
            embed.add_field(name = f"Current Members: {len(self.players)}", value = '\n'.join([x.mention for x in self.players]), inline = False)
        await ctx.respond(embed = embed)









