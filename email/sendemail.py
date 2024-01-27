#Yes, I use this thing to generate my school Email
#ignore my chinese notation. 
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage, SystemMessage
import json
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import datetime


now = datetime.datetime.now()
today = now.strftime('%Y-%m-%d %H:%M:%S')


FUNCTION_DESCRIPTIONS = [
    {
        "name": "send_email",
        "description": (
            "发送电子邮件到指定的邮箱"
            "这个函数不会返回任何值"
            "this function will not return anything"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "description": "who to send, eg: 110@gamil.com"
                },
                "subject": {
                    "type": "string",
                    "description": "subjct, eg: weather"
                },
                "content": {
                    "type": "string",
                    "description": "content, eg: its sunny today"
                }
            },
            "required": [
                "to",
                "subject",
                "content"
            ],
        }
    }
]


llm = ChatOpenAI(temperature=0,
                 model_name="gpt-3.5-turbo-16k-0613",
                 openai_api_base="https://openai-proxy.wslmf.com/v1",
                 openai_api_key="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",
                 streaming=True,
                 callbacks=[StreamingStdOutCallbackHandler()]
                 )


# 获取函数参数名称
# get function
def get_function_parameter_names(function):
    import inspect
    if function is not None and inspect.isfunction(function):
        parameter_names = inspect.signature(function).parameters.keys()
        return list(parameter_names)
    else:
        return None


# 开始发送邮件
#send
def send_email(to: str, subject: str,
               content: str) -> str:
    import smtplib

    from sendemail.mime.text import MIMEText
    from sendemail.mime.multipart import MIMEMultipart

    msg_from = ''  # 发送方邮箱
                 #from
    passwd = ''  # email key, not password

    to = [to]  # 接受方邮箱
                 #to

    # 设置邮件内容
    # MIMEMultipart类可以放任何内容
    msg = MIMEMultipart()
    conntent = content
    # 把内容加进去
    msg.attach(MIMEText(conntent, 'plain', 'utf-8'))

    # 设置邮件主题 "[重要] OpenAI SB Key余额不足"
    msg['Subject'] = subject

    # 发送方信息
    msg['From'] = msg_from

    s = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    # 登录邮箱
    s.login(msg_from, passwd)
    # 开始发送
    s.sendmail(msg_from, to, msg.as_string())
    s.quit()

    return "success"


def chat(question: str):
    first_response = llm.predict_messages(
        [
            SystemMessage(content=f"The current time is: {today}"),
            HumanMessage(content=question)
        ],
        functions=FUNCTION_DESCRIPTIONS)
    print(first_response)
    if first_response.additional_kwargs == {}:
        print('tool not found')
        pass
    function_name = first_response.additional_kwargs["function_call"]["name"]
    arguments = json.loads(first_response.additional_kwargs["function_call"]["arguments"])

    # 根据参数调用本地函数获取数据
    the_function = globals().get(function_name)
    parameter_names = get_function_parameter_names(the_function)
    parameter_values = []
    for parameter_name in parameter_names:
        if parameter_name in arguments:
            parameter_values.append(arguments[parameter_name])
        else:
            parameter_values.append(None)

    returned_value = the_function(*parameter_values)
    print(returned_value)

    llm.predict_messages(
        [
            SystemMessage(
                content=f"You are a senior python development engineer, very good at data analysis and data processing, the current time is: {today}"),
            HumanMessage(content=f"{question}"),
            AIMessage(content=str(first_response.additional_kwargs)),
            ChatMessage(
                role='function',
                additional_kwargs={'name': function_name},
                content=returned_value
            ),
        ],
        functions=FUNCTION_DESCRIPTIONS
    )


if __name__ == '__main__':

    chat(input("input:")

