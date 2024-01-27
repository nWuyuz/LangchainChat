#im using chinese engine baidu.com here as I can't build a web spider on google

from langchain.agents.agent_toolkits import create_python_agent
# from langchain.tools.python.tool import PythonREPLTool
# from langchain.python import PythonREPL
from langchain.llms.openai import OpenAI
from langchain.agents.agent_types import AgentType


from customer_tool import CustomerTool

agent_executor = create_python_agent(
    llm=OpenAI(
    temperaturve= 0,
    openai_api_base = "https://api.openai.com/"),
    openai_api_key = (""),
    tool=CustomerTool(),
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)


# agent_executor.run("奥巴马是谁?")

if __name__ == '__main__':
    while True:
        text = input("input：")
        if text == 'exit':
            break
        agent_executor.run(text)
