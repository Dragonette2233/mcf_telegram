import os


OWNER = int(os.getenv('OWNER'))
AUTH_COMMAND = os.getenv('AUTH_COMMAND')

class TEXT:

    def get_from_disk(path):
        with open(path, 'r', encoding='utf-8') as greet:
            return greet.read()
 
    # some_text = get_from_disk('some_path//')

class STORAGE:

    MCF_BOT: str = os.getenv('MCF_BOT')

    #TRIAL_LINK = 'https://t.me/' + os.getenv('TRIAL_LINK')
    CHAT_LINK = '\nhttps://t.me/' + os.getenv('CHAT_LINK')
    NFA_LINK = '\nhttps://t.me/' + os.getenv('NFA_LINK')
    
    MIRROR_PAGE = os.path.join(MCF_BOT, 'untracking', 'mirror_page.txt')
    AUTH_USERS = os.path.join(MCF_BOT, 'untracking', 'authorized_users') # Postgre!

    GREET_MESSAGE = open(os.path.join('.', 'storage_data', 'greet_message.txt'), 'r', encoding='utf-8').read()
    PR_CHANNEL_MESSAGE = open(os.path.join('.', 'storage_data', 'pr_channel_message.txt'), 'r', encoding='utf-8').read()
    MAIN_INFO = open(os.path.join('.', 'storage_data', 'bot_info_message.txt'), 'r', encoding='utf-8').read()
    # EXTEND_INFO = open(os.path.join('.', 'storage_data', 'bot_extendinfo_message.txt'), 'r', encoding='utf-8').read()
    BETS_INFO = open(os.path.join('.', 'storage_data', 'bets_start_message.txt'), 'r', encoding='utf-8').read()
    # FLETS_INFO = open(os.path.join('.', 'storage_data', 'flets_info_message.txt'), 'r', encoding='utf-8').read()
    # SCORE_ANSWER = open(os.path.join(MCF_BOT, 'mcf_lib', 'score_snip.txt'), 'r', encoding='utf-8').read()

    PREDICTS_ANSWER = os.path.join('.', 'storage_data', 'predicts_answer_sample.txt')
    PREDICTS_TRACE_GLOBAL = os.path.join(MCF_BOT, 'untracking', 'predicts_trace.json')
    PREDICTS_TRACE_DAILY = os.path.join(MCF_BOT, 'untracking', 'predicts_trace_daily.json')

    

class Storage:

    INVITE_LINK = ...

    def getsafe(path: str):
        with open(path, 'r', encoding='utf-8') as file:
            return file.read().strip()
