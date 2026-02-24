from dataclasses import dataclass
import uuid

@dataclass
class GameObject:
    name: str
    symbol: str
    description: str
    instance_type: str
    id: str = None

    def __post_init_(self):
        if self.id is None:
            self.id = str(uuid.uuid4())