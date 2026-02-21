from pathlib import Path

import click

from philoagents.application import LongTermMemoryCreator
from philoagents.config import settings
from philoagents.domain.philosopher import PlayerExtract


@click.command()
@click.option(
    "--metadata-file",
    type=click.Path(exists=True, path_type=Path),
    default=settings.EXTRACTION_METADATA_FILE_PATH,
    help="Path to the player extraction metadata JSON file.",
)
def main(metadata_file: Path) -> None:
    """CLI command to create long-term memory for soccer players.

    Args:
        metadata_file: Path to the player extraction metadata JSON file.
    """
    players = PlayerExtract.from_json(metadata_file)

    long_term_memory_creator = LongTermMemoryCreator.build_from_settings()
    long_term_memory_creator(players)


if __name__ == "__main__":
    main()
