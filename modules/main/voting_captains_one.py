import discord

class VotingButton(discord.ui.View):
    def __init__(self, players, captain):
        self.players = players
        self.captain = captain
        self.choice = None
        super().__init__(timeout = None)
    @discord.ui.button(label = "Player One", style = discord.ButtonStyle.primary, custom_id = "Player One Button")
    async def player_one_button_press(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.check_user(interaction, 'player_one')
    @discord.ui.button(label = "Player Two", style = discord.ButtonStyle.green, custom_id = "Player Two Button")
    async def player_two_button_press(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.check_user(interaction, 'player_two')
    @discord.ui.button(label = "Player Three", style = discord.ButtonStyle.red, custom_id = "Player Three Button")
    async def player_three_button_press(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.check_user(interaction, 'player_three')
    @discord.ui.button(label = "Player Four", style = discord.ButtonStyle.blurple, custom_id = "Player Four Button")
    async def player_four_button_press(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.check_user(interaction, 'player_four')

    async def check_user(self, interaction, choice):
        choices = {'player_one': self.players[0], 'player_two': self.players[1], 'player_three': self.players[2], 'player_four': self.players[3]}
        if interaction.user == self.captain:
            self.choice = choices[choice]
            await interaction.response.send_message(f"You have selected {self.choice.mention}")
            self.stop()
        else:
            await interaction.response.send_message("You either are not in queue or have already voted", ephemeral = True)
        



