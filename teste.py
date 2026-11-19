
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
import os
import dotenv
import sys

dotenv.load_dotenv()

base_url = os.environ["OLLAMA_BASE_URL"]
api_key = os.environ["OLLAMA_API_KEY"]
model = os.environ["OLLAMA_MODEL"]

system_prompt = "You are my assistent helper. You can only talk in english, if the question is in other language explain it. Don't use latex ou other type of marker as $$, you are in a terminal."

history = [SystemMessage(system_prompt)]

llm = ChatOllama(model=model, base_url=base_url, client_kwargs={"headers": {"Authorization": f"Bearer {api_key}"}}, temperature=2, repeat_penalty=1.5)


@tool(parse_docstring=True)
def get_power_result(base: int, exponent: int) -> int:
    """
    Calculate and get the result from the base power to the exponent.

    Args:
        base: a integer representing the base.
        exponent: a integer representing the exponent.
    """
    print("power teste")
    return base**exponent


llm = llm.bind_tools([get_power_result])


def get_llm_response(prompt: str) -> AIMessage:
    response = llm.invoke(prompt)
    return response


if __name__ == "__main__":
    try: 
        while True:
            prompt: str = input("prompt:")
            history.append(HumanMessage(content=prompt))

            response: AIMessage = get_llm_response(history)
            print(f"response: {response.content}")
            print(f"tools calls: {response.tool_calls}")
            history.append(response)
    except KeyboardInterrupt:
        print("Interrupted")
    except Exception:
        print("Error")

        