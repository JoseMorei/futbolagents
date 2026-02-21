class PlayerNameNotFound(Exception):
    """Exception raised when a player's name is not found."""

    def __init__(self, player_id: str):
        self.message = f"Player name for {player_id} not found."
        super().__init__(self.message)


class PlayerPhilosophyNotFound(Exception):
    """Exception raised when a player's football philosophy is not found."""

    def __init__(self, player_id: str):
        self.message = f"Player philosophy for {player_id} not found."
        super().__init__(self.message)


class PlayerStyleNotFound(Exception):
    """Exception raised when a player's style is not found."""

    def __init__(self, player_id: str):
        self.message = f"Player style for {player_id} not found."
        super().__init__(self.message)


class PlayerContextNotFound(Exception):
    """Exception raised when a player's context is not found."""

    def __init__(self, player_id: str):
        self.message = f"Player context for {player_id} not found."
        super().__init__(self.message)


# Keep backward-compatible aliases
PhilosopherNameNotFound = PlayerNameNotFound
PhilosopherPerspectiveNotFound = PlayerPhilosophyNotFound
PhilosopherStyleNotFound = PlayerStyleNotFound
PhilosopherContextNotFound = PlayerContextNotFound
