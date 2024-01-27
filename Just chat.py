from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI

api = ("api.openai.com")
key = "" # 出国替换为api.openai.com,国内用openai-proxy.wslmf.com/v1
from langchain.memory import ChatMessageHistory

history = ChatMessageHistory()


def talk(content):
    chat = ChatOpenAI(temperature=1,
                      openai_api_base=api,
                      openai_api_key=key,
                      model_name="gpt-3.5-turbo-16k-0613",
                      streaming=True,
                      callbacks=[StreamingStdOutCallbackHandler()]
                      )
    history.add_user_message(content)
    res = chat(history.messages)
    history.add_ai_message(res.content)


if __name__ == '__main__':
    while True:
        msg = input("input")
        if msg == 'quit':
            exit(0)
        talk(msg)
