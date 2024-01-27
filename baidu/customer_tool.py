import time
from langchain.tools import BaseTool
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class CustomerTool(BaseTool):
    name = "search_baidu_tool"
    description = (
        "百度搜索工具,在网络上搜索相关内容时候优先使用此工具 "
        "此工具返回结果为字符串,表示搜索到的相关内容"
        "baidu search tool,return as text"
    )

    def _run(self, query: str) -> str:
        google_service = Service(executable_path=r'')
        browser = webdriver.Chrome(service=google_service)  # 替换为你的Chrome驱动程序路径/chrome location

        browser.get('https://baidu.com')

        # 查找搜索框元素，并输入搜索关键词f
        search_box = browser.find_element(By.ID, "kw")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        # # 等待搜索结果加载完毕
        # browser.implicitly_wait(5)  # 等待5秒钟

        # 查找搜索结果元素
        search_results = browser.find_element(By.CLASS_NAME, 'c-container')
        time.sleep(2)
        return search_results.text

    async def _arun(self, start_time: str, end_time: str) -> list:
        raise NotImplementedError("Not implemented yet")

