from loguru import logger
import streamlit as st
from streamlit import write

class StreamlitSink:
    def __init__(self):
        self.buffer = ""

    def write(self, message):
        self.buffer += message.record["message"] + "\n"

    def flush(self):
        write(self.buffer)
        self.buffer = ""

def log_callback(record):
  st.write(record["message"])

streamlit_sink = StreamlitSink()
LOGGER_NAME = "llm_logger"
logger = logger.getLogger(LOGGER_NAME)
logger.setLevel(logger.DEBUG)
logger.add(log_callback)
