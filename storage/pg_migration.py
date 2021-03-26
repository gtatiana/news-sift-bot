
def create_articles_table(storage):
    storage.execute('''CREATE TABLE articles (
                    id SERIAL,
                    title TEXT UNIQUE,
                    link TEXT,
                    content TEXT,
                    category INTEGER 
                    )
                    ''')


def create_train_data_table(storage):
    storage.execute('''CREATE TABLE train_data (
                        id SERIAL,
                        content TEXT,
                        category INTEGER 
                        )
                        ''')
