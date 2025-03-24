import discord.ext.commands as commands


class AdultClient(commands.Bot):
    async def on_ready(self):
        print('Logged in as', self.user)

client = AdultClient(
    command_prefix='~',
    self_bot=True,
)
