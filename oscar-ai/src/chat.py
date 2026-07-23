from configs import Message

class Chat: 
    def __init__(self):
         self.messages: list[Message] = [] 
    def add_system(self, content: str): 
        self.messages.append( Message(role="system", content=content) )
    def add_user(self, content: str): 
        self.messages.append( Message(role="user", content=content) ) 
    def add_assistant(self, content: str):
        self.messages.append( Message(role="assistant", content=content) ) 
    def to_dict(self) -> list[dict[str, str]]:
        return [ message.model_dump() for message in self.messages ]