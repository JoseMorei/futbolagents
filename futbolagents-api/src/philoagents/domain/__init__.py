from .evaluation import EvaluationDataset, EvaluationDatasetSample
from .exceptions import PlayerPhilosophyNotFound, PlayerStyleNotFound
from .philosopher import SoccerPlayer, PlayerExtract
from .philosopher_factory import PlayerFactory
from .prompts import Prompt

__all__ = [
    "Prompt",
    "EvaluationDataset",
    "EvaluationDatasetSample",
    "PlayerFactory",
    "SoccerPlayer",
    "PlayerPhilosophyNotFound",
    "PlayerStyleNotFound",
    "PlayerExtract",
    # Backward-compatible aliases
    "PhilosopherFactory",
    "Philosopher",
    "PhilosopherPerspectiveNotFound",
    "PhilosopherStyleNotFound",
    "PhilosopherExtract",
]

# Backward-compatible aliases
from .philosopher import Philosopher, PhilosopherExtract
from .philosopher_factory import PhilosopherFactory
from .exceptions import PhilosopherPerspectiveNotFound, PhilosopherStyleNotFound
