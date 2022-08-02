import discord

class VotingButton(discord.ui.View):
    def __init__(self, players, captain):
        self.remaining = players
        self.captain = captain
        self.choice = []
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

    async def check_user(self, interaction, choice):
        choices = {'player_one': self.remaining[0], 'player_two': self.remaining[1], 'player_three': self.remaining[2]}
        if interaction.user == self.captain:
            if choices[choice] in self.choice:
                await interaction.response.send_message("You have already selected this user!", ephemeral = True)
            else:
                self.choice.append(choices[choice])
                await interaction.response.send_message(f"You have selected {choices[choice].mention} as pick {len(self.choice)}")
                if len(self.choice) == 2:
                    self.stop()
        else:
            await interaction.response.send_message("You either are not in queue or have already voted", ephemeral = True)
        



