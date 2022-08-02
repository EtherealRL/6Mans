# import discord

# class NewJoin(discord.ui.View):
#     def __init__(self, players):
#         self.players = players
#         super().__init__(timeout = None)
#     @discord.ui.button(label = "Join Queue", style = discord.ButtonStyle.blurple, custom_id = "Join Button")
#     async def join_button_press(self, button: discord.ui.Button, interaction: discord.Interaction):
#         if interaction.user not in self.players:
#             self.players.append(interaction.user)
#             embed = discord.Embed(title = "Player joined the queue", color = discord.Color.blue())
#             embed.add_field(name = f"Current Members: {len(self.players)}", value = '\n'.join([x.mention for x in self.players]), inline = False)
#             view = NewJoin(self.players)
#             await interaction.response.send_message(embed = embed, view = view)
#             if len(self.players) == 6:
#                 self.stop()
#         else:
#             await interaction.response.send_message("You are already in queue", ephemeral = True)