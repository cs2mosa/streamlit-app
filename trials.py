import youtube_transcript_api
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import extract
import logging
import sys

#sl.title("ASU study partner is here for help!")
##sl.text("our brand new ai powered chatbot")

prompt = ChatPromptTemplate.from_messages([
    ("system" , "You are a helpful assistant."),
    ("placeholder" ,"{chat_history}"),
    ("human" ,"{input}"),
    ("placeholder","{agent_scratchpad}")
    ])

#apikey = sl.text_input("input your api key")


model = ChatGoogleGenerativeAI(
    api_key='AIzaSyD0yMT6lGNwZ2dHUmBelESydwSjz-pcOFk',
    model = "gemini-1.5-pro",
    temperature= 0
    )

@tool
def get_summary(url: str)->str:
    """ :parameter: a YouTube link to the video to summarize
        :returns a summary of the video in text"""

    try:
        id_ = extract.video_id(url)
    except Exception as e:
        logging.error(f"Error extracting video ID: {str(e)}")
        return "not a valid youtube video, please use another link"

    try:
        txt = YouTubeTranscriptApi.get_transcript(id_,['ar','en'])
    except youtube_transcript_api.NoTranscriptFound:
        logging.warning(f"No transcript found for video ID: {id_}")
        return "error found: please prompt with another video"
    except Exception:
        logging.error("Error fetching transcript")
        return "Error: Unable to fetch video transcript"

    whole_text = "".join(item['text'] for item in txt)

    try:
        prompting = f"please summarize this text , and give bullet points style to its important notes in english, here is the text :{whole_text}"
        returned_text = model.invoke(prompting)
        return returned_text.content
    except Exception:
        logging.error("Error generating summary")
        return "unable to get a summary of this video due to an error, try another one please"


tools = [get_summary]
try:
    agent = create_tool_calling_agent(model, tools, prompt)
    agent_exec = AgentExecutor(agent=agent, tools=tools, verbose=True)
except Exception as e:
    logging.error(f"Error creating agent: {str(e)}")
    sys.exit(1)

def main():
    while True:#sl.button("Ask Question"):
        #user_input = sl.text_input("Hello, how can I help you?")
        user_input = input("Hello, how can I help you? (Type 'exit' to quit) ")

        if user_input.lower() == 'exit': #sl.button("exit"):
            break
        try:
            result = agent_exec.invoke({"input": user_input})
            print(result['output'])
            #sl.write(result['output'])
        except Exception:
            print("An error occurred while processing your request. Please try again.")
            sys.exit(1)

if __name__ == "__main__":
    main()
