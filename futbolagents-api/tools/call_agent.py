import asyncio
from functools import wraps

import click

from philoagents.application.conversation_service.generate_response import (
    get_streaming_response,
)
from philoagents.domain.philosopher_factory import PlayerFactory


def async_command(f):
    """Decorator to run an async click command."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.command()
@click.option(
    "--player-id",
    type=str,
    required=True,
    help="ID of the player to call.",
)
@click.option(
    "--query",
    type=str,
    required=True,
    help="Query to call the agent with.",
)
@async_command
async def main(player_id: str, query: str) -> None:
    """CLI command to query a soccer player agent.

    Args:
        player_id: ID of the player to call.
        query: Query to call the agent with.
    """

    player_factory = PlayerFactory()
    player = player_factory.get_player(player_id)

    print(
        f"\033[32mCalling agent with player_id: `{player_id}` and query: `{query}`\033[0m"
    )
    print("\033[32mResponse:\033[0m")
    print("\033[32m--------------------------------\033[0m")
    async for chunk in get_streaming_response(
        messages=query,
        player_id=player_id,
        player_name=player.name,
        player_perspective=player.perspective,
        player_style=player.style,
        player_context="",
    ):
        print(f"\033[32m{chunk}\033[0m", end="", flush=True)
    print("\033[32m--------------------------------\033[0m")


if __name__ == "__main__":
    main()
