import dataclasses
import random
import re

import discord.ext.commands as commands
from adultnea.client import AdultClient, Context


@dataclasses.dataclass
class Roll:
	dice: int
	count: int

	@classmethod
	async def convert(cls, ctx: Context, argument: str):
		match = re.match(r'([0-9]+)d([0-9]+)', argument)
		if not match:
			raise commands.BadArgument(
				f'Could not parse {argument} as a dice roll. Use something in the form of 1d6.'
			)
		return cls(int(match.group(2)), int(match.group(1)))

	def execute(self) -> int:
		total = 0
		for _ in range(self.count):
			total += random.randint(1, self.dice)
		return total


@commands.command()
async def roll(ctx: Context, dice: Roll):
	await ctx.followup(f'{dice.execute()}')


async def setup(bot: AdultClient):
	bot.add_command(roll)
