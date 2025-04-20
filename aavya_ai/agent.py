from google.adk.agents import Agent
from shared_libraries.constants import GEMINI_FLASH_LIVE_MODEL
from prompts.instructions.root_agent import ROOT_AGENT_INSTRUCTION


root_agent = Agent(
    name="Aavyaai",
    model=GEMINI_FLASH_LIVE_MODEL,
    description="Aavya AI is a virtual assistant that can help you with legal advice, research, drafting, and analysis.",
    instruction=ROOT_AGENT_INSTRUCTION
)

# print(f"Root agent: {root_agent}")
print(f"Root agent name: {root_agent.name}")
print(f"Root agent model: {root_agent.model}")