from src.model import Model, ModelConfig
from src.Providers.openai import OpenAICompatibleProvider
from src.chat import Chat

model_config = ModelConfig(
    model="gemini",
    temperature=0.7,
    max_tokens=1024,
)

provider = OpenAICompatibleProvider(
    endpoint="http://127.0.0.1:8080/v1/chat/completions",
)
model = Model(config=model_config, provider=provider)
message = Chat()
message.add_system("You are a math teacher. Always answer in maths.")
message.add_user("Tell me a story")
print("=== full response ===")
print(model.generate(prompt=message))

print("=== streaming response ===")
for chunk in model.stream(prompt=message):
    print(chunk, end="")
print()