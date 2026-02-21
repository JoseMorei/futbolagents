import json
from pathlib import Path
from typing import List

from pydantic import BaseModel, Field


class PlayerExtract(BaseModel):
    """A class representing raw player data extracted from external sources.

    This class follows the structure of the extraction_metadata.json file and contains
    basic information about players before enrichment.

    Args:
        id (str): Unique identifier for the player.
        urls (List[str]): List of URLs with information about the player.
    """

    id: str = Field(description="Unique identifier for the player")
    urls: List[str] = Field(
        description="List of URLs with information about the player"
    )

    @classmethod
    def from_json(cls, metadata_file: Path) -> list["PlayerExtract"]:
        with open(metadata_file, "r") as f:
            players_data = json.load(f)

        return [cls(**player) for player in players_data]


# Keep backward-compatible alias
PhilosopherExtract = PlayerExtract


class SoccerPlayer(BaseModel):
    """A class representing a soccer player agent with memory capabilities.

    Args:
        id (str): Unique identifier for the player.
        name (str): Name of the player.
        perspective (str): Description of the player's football philosophy.
        style (str): Description of the player's talking style.
    """

    id: str = Field(description="Unique identifier for the player")
    name: str = Field(description="Name of the player")
    perspective: str = Field(
        description="Description of the player's football philosophy"
    )
    style: str = Field(description="Description of the player's talking style")

    def __str__(self) -> str:
        return f"SoccerPlayer(id={self.id}, name={self.name}, perspective={self.perspective}, style={self.style})"


# Keep backward-compatible alias
Philosopher = SoccerPlayer
