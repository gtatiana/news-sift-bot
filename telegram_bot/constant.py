from decouple import config

WELCOME_MESSAGE = 'Hello! I am a News sif bot and I will help you distinguish good news from bad news.'
QUESTION = 'Do you want reading positive or negative news?'
TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')
DATABASE_DSN = config('DATABASE_URL')
