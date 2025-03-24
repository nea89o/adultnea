import os

def get_var(name: str, hint: str) -> str:
    value = os.getenv(name)
    if not value:
        raise Exception(f'Missing config: Cannot read environment variable {name}: {hint}')
    return value

DISCORD_TOKEN = get_var('DISCORD_TOKEN', 'Your Discord Token')
