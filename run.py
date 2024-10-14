import streamlit
import streamlit.web.cli as stcli
import os, sys
import youtube_transcript_api
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import tool,AgentExecutor, create_tool_calling_agent
from pytube import extract


def resolve_path(path):
    resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))
    return resolved_path


if __name__ == "__main__":
    sys.argv = [
        "streamlit",
        "run",
        resolve_path("streamlit_app.py"),
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main())