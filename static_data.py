import os

OWNER = int(os.getenv('OWNER'))
AUTH_COMMAND = os.getenv('AUTH_COMMAND')

class TEXT:

    def get_from_disk(path):
        with open(path, 'r', encoding='utf-8') as greet:
            return greet.read()

    # some_text = get_from_disk('some_path//')

class PATH:

    MCF_BOT = os.getenv('MCF_BOT')

    INVITE_LINK = 'https://t.me/' + os.getenv('TRIAL_LINK')
    CHAT_LINK = 'https://t.me/' + os.getenv('CHAT_LINK')
    
    MIRROR_PAGE = os.path.join(MCF_BOT, 'untracking', 'mirror_page.txt')
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
