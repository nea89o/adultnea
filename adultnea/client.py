import logging
import typing
from pathlib import Path
from typing import Any, Optional, Sequence

import aiohttp
import discord.ext.commands as commands
from discord.ext.commands import errors
import discord


class Context(commands.Context['AdultClient']):
	followup_message: Optional[discord.message.Message]

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.followup_message = None

	async def followup(
		self,
		content: str,
		attachments: Sequence[discord.File] = discord.utils.MISSING,
		allowed_mentions: Optional[discord.AllowedMentions] = None,
	):
		allowed_mentions = allowed_mentions or discord.AllowedMentions.none()
		if self.followup_message:
			await self.followup_message.edit(
				content=content,
				attachments=attachments,
				allowed_mentions=allowed_mentions,
			)
		else:
			self.followup_message = await self.reply(
				content, files=attachments, allowed_mentions=allowed_mentions
			)


class AdultClient(commands.Bot):
	http_session: aiohttp.ClientSession

	async def on_ready(self):
		logging.info(f'Logged in as {self.user}')

	async def close(self) -> None:
		if self.http_session:
			await self.http_session.close()
		return await super().close()

	async def setup_hook(self) -> None:
		await self.reload_all()
		self.http_session = aiohttp.ClientSession(
			loop=self.loop,
			headers={
				'user-agent': aiohttp.http.SERVER_SOFTWARE
				+ ' AdultNea (github.com/nea89o/adultnea/)'
			},
		)

	async def reload_all(self) -> None:
		base_path = Path(__file__).parent / 'modules'
		assert __package__
		base_package = __package__ + '.modules'
		for file in base_path.rglob('*.py'):
			typing.assert_type(file, Path)
			relative_file = file.with_name(file.name[: -len('.py')]).relative_to(
				base_path
			)
			name = (
				base_package
				+ '.'
				+ str(relative_file).replace('/', '').replace('\\', '.')
			)
			if name in self.extensions:
				logging.info(f'Reloading {name}.')
				await self.reload_extension(name)
			else:
				logging.info(
					f'Loading extension from {file} ({relative_file}) as {name}'
				)
				await self.load_extension(name)

	def __init__(self) -> None:
		super().__init__(
			command_prefix='~',
			self_bot=True,
			chunk_guilds_at_startup=False,
		)
		self.http_session = discord.utils.MISSING

	async def on_command_error(
		self, context: commands.Context, exception: errors.CommandError, /
	) -> None:
		logging.error(
			f'Encountered error in {context.command.qualified_name if context.command else "unknown"}:',
			exc_info=exception,
		)

	async def get_context(self, *args, **kwargs) -> Any:
		return await super().get_context(*args, **kwargs, cls=Context)


client = AdultClient()
