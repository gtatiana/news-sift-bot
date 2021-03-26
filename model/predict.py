import pandas as pd


def get_predict_features(prepared_data, vectorizer, fselect):
    features = vectorizer.transform(prepared_data['content'])
    features = fselect.transform(features)
    return features


def get_predict_category(model, predict_data, features):
    predictions = model.predict(features)
    predictions_df = pd.concat([predict_data['id'], pd.Series(predictions, name='predictions')], axis=1)
    return predictions_df




