import datetime
import textwrap
import typing

import discord.ext.commands as commands
import discord

from adultnea.client import AdultClient, Context


@commands.group()
async def dinfo(ctx: Context):
	pass


@dinfo.command(aliases=['u'])
async def user(ctx: Context, user: discord.User):
	pass  # TODO


def format_timestamp(i: datetime.datetime):
	return f'<t:{int(i.timestamp())}:f>'


@dinfo.command(name='guild', aliases=['server', 's', 'g'])
async def _guild(
	ctx: Context, guild: typing.Union[discord.abc.GuildChannel, discord.Guild]
):
	if isinstance(guild, discord.abc.GuildChannel):
		guild = guild.guild
	guild = await ctx.bot.fetch_guild(guild.id)
	await ctx.followup(
		textwrap.dedent(
			f"""
        **Guild**: {guild.name} (`{guild.id}`)
        **Users**: `{guild.member_count}` (Presence: `{guild.approximate_presence_count}`)
        **Owner**: <@{guild.owner_id}>
        **Roles**: {len(guild.roles)}
        **Channels**: {len(guild.channels)}
        **Created**: {format_timestamp(guild.created_at)}
        """
		)
	)


async def setup(bot: AdultClient):
	bot.add_command(dinfo)
