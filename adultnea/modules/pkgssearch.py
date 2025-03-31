import abc
import dataclasses
import datetime
import urllib.parse
from abc import abstractmethod
from typing import TypedDict, Optional

import discord.ext.commands as commands
from adultnea.client import AdultClient, Context
from adultnea.utils import join_till_limit


@dataclasses.dataclass
class Package:
	id: str
	name: str
	link: str
	latestVersion: str
	versionCount: Optional[int]
	latestReleaseTimestamp: datetime.datetime
	source: str


class Search(abc.ABC):
	@abstractmethod
	async def search(self, client: AdultClient, name: str) -> list[Package]: ...

	@abstractmethod
	def labels(self) -> list[str]: ...


JAVA_LABELS = ['java', 'maven']


def mkurl(url: str, **kwargs: str) -> str:
	return url.rstrip('?') + '?' + urllib.parse.urlencode(kwargs)


class SMOSearch(Search):
	class Response(TypedDict):
		docs: list['SMOSearch.Doc']

	class Doc(TypedDict):
		id: str
		"""The combined ``{group}:{artifact}`` id."""
		g: str
		"""The maven group of the package"""
		a: str
		"""The maven artifact id of the package"""
		latestVersion: str
		"""The version id of the latest artifact"""
		repositoryId: str
		"""Repository which contains this package"""
		timestamp: int
		"""Timestamp of the latest release (in millis)"""
		versionCount: int
		ec: list[str]
		"""List of artifacts extensions such as ``.jar``, ``-javadoc.jar``"""

	async def search(self, client: AdultClient, name: str) -> list[Package]:
		async with client.http_session.request(
			'GET',
			mkurl(
				'https://search.maven.org/solrsearch/select',
				q=name,
				rows='20',
				wt='json',
			),
		) as response:
			resp: SMOSearch.Response = (await response.json())['response']
			return [self.map_response(it) for it in resp['docs']]

	def map_response(self, doc: Doc) -> Package:
		return Package(
			doc['id'],
			doc['a'],
			f'https://search.maven.org/remotecontent?filepath={doc["g"].replace(".", "/")}/{doc["a"]}/{doc["latestVersion"]}',
			doc['latestVersion'],
			doc['versionCount'],
			datetime.datetime.fromtimestamp(doc['timestamp'] / 1000.0, datetime.UTC),
			'maven+' + doc['repositoryId'],
		)

	def labels(self) -> list[str]:
		return JAVA_LABELS + ['smo']


class CratesIOSearch(Search):
	class Response(TypedDict):
		crates: list['CratesIOSearch.Crate']

	class Crate(TypedDict):
		id: str
		name: str
		max_version: str
		description: str
		num_versions: int
		updated_at: str
		"""A timestamp in ISO 8601"""
		documentation: str

	def labels(self) -> list[str]:
		return ['rust', 'rs', 'cargo', 'crate', 'crates']

	async def search(self, client: AdultClient, name: str) -> list[Package]:
		async with client.http_session.get(
			mkurl('https://crates.io/api/v1/crates', q=name, per_page='20')
		) as resp:
			j: CratesIOSearch.Response = await resp.json()
			return [
				Package(
					it['id'],
					it['name'],
					f'https://crates.io/crates/{it["id"]}',
					it['max_version'],
					it['num_versions'],
					datetime.datetime.fromisoformat(it['updated_at']),
					'crates.io',
				)
				for it in j['crates']
			]


searches = [
	SMOSearch(),
	CratesIOSearch(),
]

assert all(tag.casefold() == tag for search in searches for tag in search.labels())


@commands.group(invoke_without_command=True, aliases=['pkgs'])
async def pkg(ctx: Context, tag: str, *, search: str):
	search_engines = [it for it in searches if tag.casefold() in it.labels()]
	if not search_engines:
		await ctx.followup(f'Could not find a search engine for {tag}')
		return
	packages = []
	for engine in search_engines:
		packages.extend(await engine.search(ctx.bot, search))
	if not packages:
		await ctx.followup('Could not find any packages for that query.')
		return
	message = join_till_limit(
		'\n',
		(f'- [`{it.id}`@`{it.latestVersion}`](<{it.link}>)' for it in packages),
		prefix='Packages:\n',
	)
	await ctx.followup(message)


@pkg.command()
async def ls(ctx: Context):
	await ctx.followup(
		'Search Tags:\n'
		+ '\n'.join(
			f'- `{tag}`'
			for tag in set(tag for search in searches for tag in search.labels())
		)
	)


async def setup(bot: AdultClient):
	bot.add_command(pkg)
