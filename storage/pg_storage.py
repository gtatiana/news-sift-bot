import pandas as pd
import psycopg2
from sqlalchemy import create_engine


class PGStorage:
    def __init__(self, dsn):
        self.con = psycopg2.connect(dsn)
        self.engine = create_engine(dsn)

    def save_articles(self, articles):
        cursor = self.con.cursor()
        cursor.executemany("INSERT into articles(title, link, content)\
                                      VALUES (%(title)s, %(link)s, %(content)s) ON CONFLICT DO NOTHING;", articles)
        self.con.commit()

    def get_train_data(self):
        dataset = pd.read_sql_query("SELECT content, category FROM train_data", self.con)
        return dataset

    def get_predict_data(self):
        dataset = pd.read_sql_query("SELECT id, content FROM articles WHERE category IS NULL", self.con)
        return dataset

    def update_articles_prediction(self, predictions_df):
        predictions_df.to_sql('predictions_tb', self.engine, if_exists='replace')
        self.execute('''
                UPDATE articles AS a
                SET category = p.predictions::INTEGER
                FROM predictions_tb AS p
                WHERE a.id = p.id       
        ''')

    def execute(self, sql_query):
        cur = self.con.cursor()
        cur.execute(sql_query)
        self.con.commit()

    def get_article_links(self, is_positive):
        cur = self.con.cursor()
        sql = '''
                        SELECT link FROM articles WHERE category = %s
                        ORDER BY id DESC LIMIT 5
                        '''
        cur.execute(sql, (is_positive,))
        return cur.fetchall()
