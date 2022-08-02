import discord

class VotingButton(discord.ui.View):
    def __init__(self, players):
        self.captains = 0
        self.random = 0
        self.balanced = 0
        self.decision = None
        self.voters = []
        self.players = players
        super().__init__(timeout = None)
    @discord.ui.button(label = "Captains Pick: 0/3", style = discord.ButtonStyle.green, custom_id = "Captains Button")
    async def captains_button_press(self, button: discord.ui.Button, interaction: discord.Interaction):
        if await self.check_user(interaction, 'captains'):
            button.label = f"Captains Pick: {self.captains}/3"
            await interaction.response.edit_message(view = self)
    @discord.ui.button(label = "Random Teams: 0/3", style = discord.ButtonStyle.red, custom_id = "Random Button")
    async def random_button_press(self, button: discord.ui.Button, interaction: discord.Interaction):
        if await self.check_user(interaction, 'random'):
            button.label = f"Random Teams: {self.random}/3"
            await interaction.response.edit_message(view = self)
    @discord.ui.button(label = "Balanced Teams: 0/3", style = discord.ButtonStyle.blurple, custom_id = "Balanced Button")
    async def balanced_button_press(self, button: discord.ui.Button, interaction: discord.Interaction):
        if await self.check_user(interaction, 'balanced'):
            button.label = f"Balanced Teams: {self.balanced}/3"
            await interaction.response.edit_message(view = self)

    async def check_user(self, interaction, choice):
        if interaction.user not in self.voters and interaction.user in self.players:
            if choice == 'random':
                self.random +=  1
            elif choice == 'captains':
                self.captains += 1
            elif choice == 'balanced':
                self.balanced += 1
            self.voters.append(interaction.user)
            if self.random == 3:
                self.decision = 'random'
                self.stop()
            elif self.captains == 3:
                self.decision = 'captains'
                self.stop()
            elif self.balanced == 3:
                self.decision = 'balanced'
                self.stop()
            return True
        else:
            await interaction.response.send_message("You either are not in queue or have already voted", ephemeral = True)
        



