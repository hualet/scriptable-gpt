#!/usr/bin/env python

import sys
import subprocess

from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_core.messages import HumanMessage

from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView

app = QApplication(sys.argv)
w = QWebEngineView()

def open_website(address):
    print("function open_website: ", address)
    w.load(QUrl(address))

class MyAgent:
    def __init__(self ) -> None:
        self.tools = [
            {
                "name": "open_website",
                "description": "用浏览器打开特定的网址",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "address": {
                            "type": "string",
                            "description": "要打开的网址，比如 baidu.com",
                        }
                    },
                    "required": ["address"],
                }
            },
        ]

        self.fc_model = self.setup_fc_model()
        self.v_model = self.setup_v_model()

    def run(self, script_str):
        resp = self.fc_model.invoke(script_str)
        if resp.tool_calls:
            for tool_call in resp.tool_calls:
                for tool in self.tools:
                    if tool["name"] == tool_call["name"]:
                        func_name = tool_call["name"]
                        params = tool_call["args"]
                        globals()[func_name](**params)

    def setup_fc_model(self):
        model = OllamaFunctions(model="qwen2", format="json")
        model = model.bind_tools(
            tools=self.tools,
            # function_call={"name": "open_website"},
        )
        return model

    def setup_v_model(self):
        return None



if __name__ == "__main__":
    script = [
        "打开网址 https://oa.uniontech.com",
    ]

    agent = MyAgent()

    for script_line in script:
        print(f"User: {script_line}")
        response = agent.run(script_line)
        print(f"Assistant: {response}")

    w.showMaximized()
    app.exec()