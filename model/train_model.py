from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import LogisticRegression
import pickle
import os

path = os.path.dirname(os.path.abspath(__file__)) + '/trained_data/'
vectorizer_path = path + 'vectorizer.pickle'
fselect_path = path + 'fselect.pickle'
model_path = path + 'model.pickle'


class TrainModel:
    def __init__(self, train_data):
        self.train_data = train_data

    def __get_vectorizer(self):
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 3),
                                     max_df=0.8, min_df=2, sublinear_tf=True)
        vectorizer.fit(self.train_data['content'])
        return vectorizer

    def __get_train_features(self, vectorizer):
        features = vectorizer.transform(self.train_data['content'])
        fselect = SelectKBest(chi2, k=25000).fit(features, self.train_data['category'])
        features = fselect.transform(features)
        return features, fselect

    def __train_model(self, features):
        y = self.train_data['category']
        log_reg = LogisticRegression(solver='liblinear')
        return log_reg.fit(features, y)

    def run_train(self):
        vectorizer = self.__get_vectorizer()

        with open(vectorizer_path, 'wb') as f:
            pickle.dump(vectorizer, f)

        features, fselect = self.__get_train_features(vectorizer)

        with open(fselect_path, 'wb') as f:
            pickle.dump(fselect, f)

        model = self.__train_model(features)

        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        exit()


def get_trained():
    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)

    with open(fselect_path, 'rb') as f:
        fselect = pickle.load(f)

    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return vectorizer, fselect, model
