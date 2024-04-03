import os

OWNER = int(os.getenv('OWNER'))
AUTH_COMMAND = os.getenv('AUTH_COMMAND')

class PATH:

    MCF_BOT = os.getenv('MCF_BOT')

    INVITE_LINK = 'https://t.me/' + os.getenv('INVITE_LINK')
    
    MIRROR_PAGE = os.path.join('.', 'storage_data', 'mirror_page.txt')
    AUTH_USERS = os.path.join(MCF_BOT, 'untracking', 'authorized_users') # Postgre!
    MAIN_INFO = os.path.join('.', 'storage_data', 'bot_info_message.txt')
    EXTEND_INFO = os.path.join('.', 'storage_data', 'bot_extendinfo_message.txt')
    FLETS_INFO = os.path.join('.', 'storage_data', 'flets_info_message.txt')
    SCORE_ANSWER = os.path.join('.', 'storage_data', 'score_answer_sample.txt')
    PREDICTS_ANSWER = os.path.join('.', 'storage_data', 'predicts_answer_sample.txt')
    PREDICTS_TRACE_GLOBAL = os.path.join(MCF_BOT, 'untracking', 'predicts_trace.json')
    PREDICTS_TRACE_DAILY = os.path.join(MCF_BOT, 'untracking', 'predicts_trace_daily.json')
    GREET_MESSAGE = os.path.join('.', 'storage_data', 'greet_message.txt')

class Storage:

    INVITE_LINK = ...

    def getsafe(path: str):
        with open(path, 'r', encoding='utf-8') as file:
            return file.read().strip()
