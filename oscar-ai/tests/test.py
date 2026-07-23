from src.chat import Chat
from src.configs import Requirements
from src.model import Model, ModelConfig
from src.Providers.openai import OpenAICompatibleProvider
from src.router import Registry, Router

model_config = ModelConfig(
    model="gemini",
    temperature=0.7,
    max_tokens=1024,
)

provider = OpenAICompatibleProvider(
    endpoint="http://127.0.0.1:8080/v1/chat/completions",
)

registry = Registry()
model_one = Model(config=model_config, provider=provider)
model_two = Model(config=model_config, provider=provider)
registry.register_model("first-model", model_one)
registry.register_model("second-model", model_two)
router = Router(registry)

prompt_one = Chat()
prompt_one.add_system("You are a math teacher. Always answer in maths.")
prompt_one.add_user("Tell me a story")

prompt_two = Chat()
prompt_two.add_system("You are a philosopher. Always answer with deep insight.")
prompt_two.add_user("Tell me a story")

print("=== full response model one ===")
print(router.generate(prompt_one, Requirements(id="first-model")))

print("=== full response model two ===")
print(router.generate(prompt_two, Requirements(id="second-model")))

print("=== streaming response model one ===")
for chunk in router.stream(prompt_one, Requirements(id="first-model")):
    print(chunk, end="")
print()

print("=== streaming response model two ===")
for chunk in router.stream(prompt_two, Requirements(id="second-model")):
    print(chunk, end="")
print()
