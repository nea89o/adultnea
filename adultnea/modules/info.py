import datetime
import inspect
import logging
import textwrap
from configparser import ConverterMapping

import discord.ext.commands as commands
import discord
from discord.ext.commands._types import BotT

from adultnea.client import AdultClient, Context


@commands.group()
async def dinfo(ctx: Context):
    pass


@dinfo.command(aliases=['u'])
async def user(ctx: Context, user: discord.User):
    pass  # TODO

def format_timestamp(i: datetime.datetime):
    return f'<t:{int(i.timestamp())}:f>'

class GuildConv(commands.GuildConverter):

    async def convert(self, ctx: Context, argument: str) -> discord.Guild:
        try:
            return await super().convert(ctx, argument)
        except commands.CommandError:
            try:
                chan = await commands.GuildChannelConverter() \
                    .convert(ctx, argument)
                return chan.guild
            except commands.CommandError:
                pass
            raise


@dinfo.command(aliases=['server', 's', 'g'])
async def guild(ctx: Context, guild: GuildConv):
    guild: discord.Guild
    guild = await ctx.bot.fetch_guild(guild.id)
    await ctx.followup(
        textwrap.dedent(
            f'''
        **Guild**: {guild.name} (`{guild.id}`)
        **Users**: `{guild.member_count}` (Presence: `{guild.approximate_presence_count}`)
        **Owner**: <@{guild.owner_id}>
        **Roles**: {len(guild.roles)}
        **Channels**: {len(guild.channels)}
        **Created**: {format_timestamp(guild.created_at)}
        ''')
    )


async def setup(bot: AdultClient):
    bot.add_command(dinfo)
