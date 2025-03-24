from adultnea import config
from adultnea.client import client


def main():
    print("Hello from adultnea!")
    client.run(token=config.DISCORD_TOKEN)


if __name__ == "__main__":
    main()
