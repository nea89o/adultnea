# Adult Nea

> Growing up is realizing that application commands fucking suck.

After writing an application command based bot called [lilnea](https://github.com/nea89o/lilnea/) i have realized how annoying to use and limited those app commands are. They can't follow you into nearly any server (with good reason, they can quite easily be used to bypass all sort of spam detections and other auto mod checks), they can't see a lot of things about the servers you are in, they can't (easily) accept multi line text, etc.

The solution is selfbots (or userbots, if you are too scared of running the bot on your own account). They carry a ban risk (as does using discord client mods, that everyone uses anyway), but they can act pretty much exactly in the way your user does. They also directly respond to text commands, meaning you will have a much smoother experience typing out commands (assuming you remember them, which i do, because i wrote them).

So here we are, adultnea. I dont particularly like python (although it has come along quite nicely in regards to better typing (my primary criticism of python) in recent years), but i have a decent chunk of experience with it and it has an actually up to date and comprehensive user bot library: [discord.py-self](https://github.com/dolfies/discord.py-self).

## Project Setup

This project is primarily intended for myself and as such has made a few, let's just say bespoke, choices. I am however still open to suggestions regarding the project layout, design choices and such, and if you think a config option or two would make the bot more approachable, feel free to suggest or (preferably) PR.

## Usage

This project uses [uv](https://docs.astral.sh/uv/) for a lot of things:

- Install the dependencies using `uv sync`
- Run the project using `uv run -m adultnea`
- Format the project using `uv run ruff format`
- Lint the project using `uv run ruff check`
- Type-check the project using `uv run pyright`
- Use [`pre-commit`](https://pre-commit.com/) for automatically running format, check and type-check on commit
  - `pre-commit` tasks also get automatically executed in github actions.

Environment variables can optionally be saved in `.env`. There is no interactive setup or anything like that. Extract your discord token ([Tutorial](https://discordpy-self.readthedocs.io/en/latest/authenticating.html#how-do-i-obtain-mine)) and store it as `DISCORD_TOKEN=MzEwNzAyMT...`. After that running should just work. You can check out `~help` for a list of commands.
