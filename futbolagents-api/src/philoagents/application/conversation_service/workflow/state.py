from langgraph.graph import MessagesState


class PlayerState(MessagesState):
    """State class for the LangGraph workflow. It keeps track of the information necessary to maintain a coherent
    conversation between the Soccer Player and the user.

    Attributes:
        player_context (str): The career and football context of the player.
        player_name (str): The name of the player.
        player_perspective (str): The football philosophy of the player.
        player_style (str): The talking style of the player.
        summary (str): A summary of the conversation. This is used to reduce the token usage of the model.
    """

    player_context: str
    player_name: str
    player_perspective: str
    player_style: str
    summary: str


# Keep backward-compatible alias
PhilosopherState = PlayerState


def state_to_str(state: PlayerState) -> str:
    if "summary" in state and bool(state["summary"]):
        conversation = state["summary"]
    elif "messages" in state and bool(state["messages"]):
        conversation = state["messages"]
    else:
        conversation = ""

    return f"""
PlayerState(player_context={state["player_context"]},
player_name={state["player_name"]},
player_perspective={state["player_perspective"]},
player_style={state["player_style"]},
conversation={conversation})
        """
