import config
from parser import bbc_parse_articles
from model import predict, data_preprocessing
from model.train_model import get_trained


def parse_new_data(storage):
    print('start parse new data')
    articles = bbc_parse_articles.bbc_parse(config.BBC_URL)
    print('articles parsed, store to DB')
    storage.save_articles(articles)
    print('articles stored, run model')
    vectorizer, fselect, model = get_trained()

    predict_data = storage.get_predict_data()
    prepared_data = data_preprocessing.prepare_data(predict_data)

    features = predict.get_predict_features(prepared_data, vectorizer, fselect)

    predictions_df = predict.get_predict_category(model, predict_data, features)
    print('saving prediction to DB')
    storage.update_articles_prediction(predictions_df)
    print('prediction saved')
