from src.chat import Chat
from src.configs import Message


def test_chat_records_system_user_and_assistant_messages():
    chat = Chat()
    chat.add_system("system prompt")
    chat.add_user("user prompt")
    chat.add_assistant("assistant answer")

    assert chat.messages == [
        Message(role="system", content="system prompt"),
        Message(role="user", content="user prompt"),
        Message(role="assistant", content="assistant answer"),
    ]


def test_chat_to_dict_returns_serializable_messages():
    chat = Chat()
    chat.add_user("hello")

    assert chat.to_dict() == [{"role": "user", "content": "hello"}]
