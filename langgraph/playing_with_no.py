from langchain.tools import tool
# from langchain_openai import ChatOpenAI
import os
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = AzureChatOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two numbers together."""
    print(f"Multiplying {a} and {b}")
    return a * b

@tool
def add(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b
@tool
def subtract(a: int, b: int) -> int:
    """Subtracts the second number from the first."""
    return a - b

tools = [multiply, add, subtract]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)

print(model_with_tools.invoke("What is 5 multiplied by 3?"))