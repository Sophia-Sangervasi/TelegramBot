
#!/usr/bin/env python3
"""
10/07/2021
Author: Sophia Sangervasi
Jira Ticket number: DEVOPS-239

This project instantiates a Telegram Bot that when added to a Telegram chat
by the '/record' command, it spawns a new bot in the corresponding chat.
Once the bot is in the chat it begins polling the chat conversation and stores
a Telegram Message object into a list of dictionaries. Each dictionary consists
of a (Key, Value) pair where the Key is the Telegram chat conversation's unique
ID value, and the Value is the Telegram Message object.

The Telegram Bot is able to be in multiple conversations at once allowing for
multiple records of different conversations that are running in parallel.
"""
import json
import os
import telebot
import logging
from pprint import pprint as pp
from datetime import datetime
from collections import defaultdict



################################## INITIALIZING THE BOT ########################

#the bot token to be used. Given by the BotFather
#MAKE AN ENV VARIABLE FOR SECURITY PURPOSES
API_KEY = os.environ.get('API_KEY')


#creating bot with given token
bot = telebot.TeleBot(API_KEY)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.'

################################### GLOBAL VARIABLES ##########################

#dictionary to hold all of the data that is in the chat after
#the bot has entered the chat
all_chats = {}


#################################### METHODS FOR BOT ###########################

########################################################
# This method converts unix date and time to
# utc date and time. It then replaces the unix
# in dict with the new converted time.
# @param unix_time: The needing to be converted to utc
# @param dict: The dictionary that holds place where date
# will be stored *NOT IN USE*
#######################################################
def convert_to_utc(unix_time, json):
    unix_time = datetime.utcfromtimestamp(int(unix_time)).strftime('%Y-%m-%d %H:%M:%S')
    print(unix_time)
    json.update({"date": unix_time})
    print(json)

######################################################
# This method takes a message object that is then used
# to get the message new_chat_members. If there are
# no users in the chat the bot will stop polling and
# leave chat. *NOT IN USE*
######################################################
def lonely_bot(message):

    #the current list of users in the chat
    cid = message.chat.id

    num_members = bot.get_chat_member_count(cid)

    print("number of ppl in chat")
    pp(num_members)

    #if bot is only one in the chat then leave the chat
    if num_members == 1:
        pp(num_members)

        #leave the chat after there is no one there
        bot.leave_chat()

    else:
        pass


######################################################
# This function checks to see if the given chat id is
# already in the data_dict dictionary.
######################################################
def already_exists(all_chats, message_obj):
        #adding time and date attribute in converted unix time
        #grabbing the unix date and time to be converted into utc time
        #unix_date_time = json.get("date")

        #method that converts unix time/date stamp to utc
        #convert_to_utc(unix_date_time, json)

    #if the convos_list does not hold the chat Id data then place new dictionary in dictionar of conversations
    if message_obj.chat.id not in all_chats :

            new_msg_list = []
            #adding new dictionary to the all chats dictionary to hold new conversation
            pp(all_chats)

            #creating a new dictionary for a new conversation dictionary to be
            #added to the conversation list
            all_chats[message_obj.chat.id] = {}
            #list of messages that are part of this convo
            all_chats[message_obj.chat.id]["messages"] = new_msg_list
            print("AFTER THE NEWLY ADDED dict with message")
            pp(all_chats)

    #add data to the list

    all_chats[message_obj.chat.id]["messages"].append(message_obj.json)

            #placing new message in a list
            #message_list.append(json)

            #placing a copy of the updated message list in var
            #msg_list_copy = message_list.copy()

            #placing a copy of updated message list in data dictionary
            #new_dict.update({"message_list": msg_list_copy})

            #new_dict_copy = new_dict.copy()

            #print("new dict copy")
            #pp(new_dict_copy)
            #convos_list.append(new_dict_copy)

            #print("I am here in the first if")
            #pp(convos_list)
    """else:


        for dict in convos_list:
            #the chat id in the available ditcionary
            val = dict.get("chat_id")

            if  val == cid:

                #grabbing the unix date and time to be converted into utc time
                #unix_date_time = json.get("date")

                #method that converts unix time/date stamp to utc
                #convert_to_utc(unix_date_time, json)

                #first grabbing the pre exisiting message list from
                #corresponding dict that matched the CID
                dict_message_list = dict.get("message_list")

                #placing new message in a list
                dict_message_list.append(json)

                #placing a copy of the updated message list in var
                msg_list_copy = dict_message_list.copy()

                #placing a copy of updated message list in data dictionary
                dict.update({"message_list": msg_list_copy})

                print("I AM THE FIRST IF")
                pp(convos_list)
                break;


            elif (val != cid) and (convos_list.index(dict) == len(convos_list) - 1):


                new_dict["chat_id"] = cid
                #grabbing the unix date and time to be converted into utc time
                #unix_date_time = json.get("date")

                #method that converts unix time/date stamp to utc
                #convert_to_utc(unix_date_time, json)

                #placing new message in a list
                new_msg_list.append(json)

                #placing a copy of the updated message list in var
                msg_list_copy = new_msg_list.copy()

                #placing a copy of updated message list in data dictionary
                new_dict.update({"message_list": msg_list_copy})

                new_dict_copy = new_dict.copy()
                convos_list.append(new_dict_copy)

                pp(convos_list)
                break;"""

    return all_chats

######################################################
# This function notifies user's in chat that the
# chat has begun being recorded.
######################################################
@bot.message_handler(commands=['record'])
def inform_users(message):
    ########send message to user########
    bot.send_message(message.chat.id, "Hello, my name is Wallie! I will be archiving all messages in this chat for Prime Trust's records. Recording has started.")

#####################################################
# This function begins directly after the /record
# command and stores all the data of chat and message
# data that was recieved in the 'json' attribute of
# the telegram message object. The json dictionary contains

'''
'json': {
'message_id': the id of message sent,
'from': {
'id': id of the user that sent the message,
 'is_bot': if the message was sent by a bot,
 'first_name': fist name of user,
'last_name': last name of user,
 'language_code': set language code
},
'chat': {
'id': id number of chat,
'title': name of chat,
'type': chat type (group, private, channel),
'all_members_are_administrators': True
},
'date': date and time of message sent in unix time,
 'text': content of message that is text,
 'entities': [{'offset': 0, 'length': 7, 'type': 'bot_command'}]}}

'''
#####################################################
@bot.message_handler(func=lambda m: True)
def record(message): #recording on messages

        #gets the chat info from message obj
        #chat_info = message.chat

        #getting dict from message ("not actually json in json format")
        #json=message.json

        #method that checks if chat_id is in the convo list; passing the message
        #obj and global conversation list
        updcon = already_exists(all_chats, message)

        print("This is what is returned")
        pp(updcon)

        #lonely_bot(message)


bot.polling(timeout=20)
