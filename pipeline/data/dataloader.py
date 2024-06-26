from langchain_community.chat_loaders.telegram import TelegramChatLoader
from schema.data import TelegramChatMessage
from typing import List 
from loguru import logger
import streamlit as st
import sys

# def log_callback(record):
#   st.write(record["message"])

# logger.add(log_callback)

def parse_special_types(nested_message: dict):
  match nested_message.get('type'):
    case 'mention' | 'link':
      return nested_message['text']
    case _:
      return nested_message

def preprocess_telegram_message(raw_messages: List[str]) -> List[TelegramChatMessage]:
  logger.debug("Preprocessing telegram messages now...")
  chat_messages: List[TelegramChatMessage] = []
      
  for raw_message in raw_messages:
      content = raw_message.content
      if len(content) == 0:
        continue
      
      # Get content of message
      plain_content = ""
      if isinstance(content, list):
        for element in content:
          if isinstance(element, dict):  # Check if it's a dictionary
            plain_content += f"{parse_special_types(element)}"  # Use the function for username extraction
          else:
            plain_content += element.replace("\n", "")
      else:
        plain_content = content
        
      # Get sender info (assumption: will always be available)
      sender = raw_message.additional_kwargs['sender']
      message_time = raw_message.additional_kwargs['events'][0]['message_time']
      chat_messages.append(TelegramChatMessage(sender=sender, message=plain_content, timestamp=message_time))
        
  return chat_messages  

def load_data(path: str =  "../dataset/ces_team_group.json") -> List[TelegramChatMessage]:
    loader = TelegramChatLoader(path=path)
    raw_messages = loader.load()
    if raw_messages is not None and len(raw_messages[0]['messages'])>0:
      logger.debug(f"Loading data now... There are {len(raw_messages[0]['messages'])} messages")
      return preprocess_telegram_message(raw_messages[0]['messages'])
    else:
      logger.error(f"No data found in {path}!")
      sys.exit(1)