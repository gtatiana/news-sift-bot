from apscheduler.schedulers.blocking import BlockingScheduler
from telegram_bot.news_sift_bot import run_bot
from argparse import ArgumentParser
from storage.pg_storage import PGStorage
import run_model
import config
from storage import pg_migration
from parse_new_data import parse_new_data


if __name__ == "__main__":
    print('starting')
    storage_pg = PGStorage(config.DATABASE_DSN)

    parser = ArgumentParser()
    parser.add_argument('command',
                        metavar='<command>',
                        help="'train' or 'migrate' or 'parse' or 'run-bot'")
    args = parser.parse_args()
    if args.command == "train":
        run_model.train(storage_pg)
        exit(0)
    if args.command == "migrate":
        pg_migration.create_articles_table(storage_pg)
        pg_migration.create_train_data_table(storage_pg)
        exit(0)
    elif args.command == "parse":
        parse_new_data(storage_pg)
        scheduler = BlockingScheduler()
        scheduler.add_job(lambda: parse_new_data(storage_pg), 'interval', minutes=30)
        scheduler.start()
        exit(0)
    elif args.command == "run-bot":
        run_bot()
        exit(0)
    else:
        print("Unsupported command: ", args.command)
        exit(1)

