import datetime
import textwrap
import typing
from typing import TypeAlias

import discord.ext.commands as commands
import discord

from adultnea.client import AdultClient, Context

GenericGuild: TypeAlias = typing.Union[discord.abc.GuildChannel, discord.Guild]


def ungeneric_guild(generic: GenericGuild) -> discord.Guild:
	if isinstance(generic, discord.abc.GuildChannel):
		return generic.guild
	return generic


@commands.group()
async def dinfo(ctx: Context):
	pass


@dinfo.command(aliases=['u'])
async def user(ctx: Context, user: discord.User, guild: typing.Optional[GenericGuild]):
	info = textwrap.dedent(
		f"""
		**User**: {user.name} {user.mention}
		**Created At**: {format_timestamp(user.created_at)}
		"""
	)
	await ctx.followup(info)
	# if guild:
	# 	guild = ungeneric_guild(guild)
	# 	member = await guild.fetch_member(user.id)
	# 	TODO: do something with this info


def format_timestamp(i: datetime.datetime):
	return f'<t:{int(i.timestamp())}:f>'


@dinfo.command(name='guild', aliases=['server', 's', 'g'])
async def _guild(ctx: Context, guild: GenericGuild):
	guild = ungeneric_guild(guild)
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
