import sqlite3
import pandas as pd


class Storage:
    def __init__(self, path):
        self.path = path
        self.con = sqlite3.connect(self.path)

    def save_articles(self, articles):
        cursor = self.con.cursor()
        cursor.executemany("INSERT OR IGNORE into articles(id, title, link, content)\
                                      VALUES (NULL, :title, :link, :content);", articles)
        self.con.commit()

    def get_train_data(self):
        dataset = pd.read_sql_query("SELECT content, category FROM train_data", self.con)
        return dataset

    def get_predict_data(self):
        dataset = pd.read_sql_query("SELECT id, content FROM articles WHERE category IS NULL", self.con)
        return dataset

    def update_articles_prediction(self, predictions_df):
        predictions_df.to_sql('predictions_tb', self.con, if_exists='replace')
        self.execute('''
                UPDATE articles AS a
                SET category = p.predictions
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
                        SELECT link FROM articles WHERE category = :is_positive
                        ORDER BY id DESC LIMIT 5
                        '''
        links = cur.execute(sql, (is_positive,))
        return links
