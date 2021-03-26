from model import data_preprocessing, train_model


def train(storage):
    data = storage.get_train_data()
    train_data = data_preprocessing.prepare_data(data)
    model = train_model.TrainModel(train_data)
    model.run_train()