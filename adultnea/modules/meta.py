import logging

import discord.ext.commands as commands

from adultnea.client import AdultClient, Context


@commands.group(
    invoke_without_command=True
)
async def mod(ctx: Context):
    pass


@mod.command()
async def ls(ctx: Context):
    module_names = [it.replace(__package__, '') for it in ctx.bot.extensions.keys()]
    await ctx.followup('Modules:\n' + '\n'.join(f'- `{name}`' for name in module_names))


@mod.command(aliases=['r'])
async def reload(ctx: Context):
    await ctx.followup(content='Reload started.')
    await ctx.bot.reload_all()
    await ctx.followup(content='Reloaded.')


async def setup(bot: AdultClient):
    logging.info('Loading meta module.')
    bot.add_command(mod)
