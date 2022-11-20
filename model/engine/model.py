import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import *
from sklearn.preprocessing import MinMaxScaler


class Model(object):
    def __init__(self, training_data, column):
        columns = ['Date', 'Open', 'High', 'Low', 'Close']
        training_data = training_data[columns]
        self.training_data = training_data
        self.num_shape = len(training_data) - 20

        columnIndex = columns.index(column)
        self.train = training_data.iloc[:self.num_shape, columnIndex:columnIndex + 1].values
        self.test = training_data.iloc[self.num_shape:, columnIndex:columnIndex + 1].values

        self.sc = MinMaxScaler(feature_range=(0, 1))
        train_scaled = self.sc.fit_transform(self.train)

        X_train = []
        y_train = []

        self.window = 60

        for i in range(self.window, self.num_shape):
            X_train_ = np.reshape(train_scaled[i - self.window:i, 0], (self.window, 1))
            X_train.append(X_train_)
            y_train.append(train_scaled[i, 0])

        X_train = np.stack(X_train)
        y_train = np.stack(y_train)

        self.model = Sequential()

        self.model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
        self.model.add(Dropout(0.2))

        self.model.add(LSTM(units=50, return_sequences=True))
        self.model.add(Dropout(0.2))

        self.model.add(LSTM(units=50, return_sequences=True))
        self.model.add(Dropout(0.2))

        self.model.add(LSTM(units=50))
        self.model.add(Dropout(0.2))

        self.model.add(Dense(units=1))

        self.model.compile(optimizer='adam', loss='mean_squared_error')
        self.model.fit(X_train, y_train, epochs=10, batch_size=32)

    def predict(self):
        df_volume = np.vstack((self.train, self.test))

        inputs = df_volume[df_volume.shape[0] - self.test.shape[0] - self.window:]
        inputs = inputs.reshape(-1, 1)
        inputs = self.sc.transform(inputs)

        num_2 = df_volume.shape[0] - self.num_shape + self.window

        X_test = []

        for i in range(self.window, num_2):
            X_test_ = np.reshape(inputs[i - self.window:i, 0], (self.window, 1))
            X_test.append(X_test_)

        X_test = np.stack(X_test)

        predict = self.model.predict(X_test)
        predict = self.sc.inverse_transform(predict)

        pred_ = predict[-1].copy()
        prediction_full = []
        window = 60
        df_copy = self.training_data.iloc[:, 1:2][1:].values
        self.training_data = pd.DataFrame(self.training_data[['Date', 'Close']].iloc[-30:])
        last_date = self.training_data['Date'].iloc[-1]

        for j in range(20):
            last_date += pd.Timedelta(1, 'd')

            df_ = np.vstack((df_copy, pred_))
            train_ = df_[:self.num_shape]
            test_ = df_[self.num_shape:]

            df_volume_ = np.vstack((train_, test_))

            inputs_ = df_volume_[df_volume_.shape[0] - test_.shape[0] - window:]
            inputs_ = inputs_.reshape(-1, 1)
            inputs_ = self.sc.transform(inputs_)

            X_test_2 = []

            for k in range(window, num_2):
                X_test_3 = np.reshape(inputs_[k - window:k, 0], (window, 1))
                X_test_2.append(X_test_3)

            X_test_ = np.stack(X_test_2)
            predict_ = self.model.predict(X_test_)
            pred_ = self.sc.inverse_transform(predict_)
            prediction_full.append([last_date, "%.1f" % pred_[-1][0]])
            df_copy = df_[j:]
        df = pd.DataFrame(prediction_full, columns=['Date', 'Close'])

        return pd.concat([self.training_data, df], ignore_index=True).to_numpy()
