from enum import Enum, auto

class EditorState(Enum):
    WELCOME = auto()
    EDITING = auto()
    PLAYTEST = auto()