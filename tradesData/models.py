from django.db import models
import datetime, requests, json, time
import pandas as pd
import threading
from model.engine import Model
from reviewers.settings import BINANCE_API
from prediction.models import Prediction


def make_prediction(column):
    price_data = pd.DataFrame(list(Kline.objects.all().values()))
    model = Model(price_data, column)

    return model.predict()


class Kline(models.Model):
    Date = models.DateTimeField(verbose_name='Open Time')
    Open = models.FloatField(verbose_name='Open')
    High = models.FloatField(verbose_name='High')
    Low = models.FloatField(verbose_name='Low')
    Close = models.FloatField(verbose_name='Close')
    Volume = models.FloatField(verbose_name='Volume')
    CloseTime = models.DateTimeField(verbose_name='Close Time')
    QuoteAssetVolume = models.FloatField(verbose_name='Quote Asset Volume')
    NumberOfTrades = models.IntegerField(verbose_name='Number Of Trades')
    TakerBuyBaseAssetVolume = models.FloatField(verbose_name='Taker buy base asset volume')
    TakerBuyQuoteAssetVolume = models.FloatField(verbose_name='Taker buy quote asset volume')

    class Meta:
        verbose_name = 'Kline'
        verbose_name_plural = 'Klines'


class KlineReceiver:
    def __init__(self):
        self.binanceApi = BINANCE_API

    def _updateDB(self, klines):
        for kline in klines:
            datetimeOpenObj = datetime.datetime.utcfromtimestamp(int(kline[0]) / 1000)
            datetimeCloseObj = datetime.datetime.utcfromtimestamp(int(kline[6]) / 1000)
            Kline.objects.create(
                Date=datetimeOpenObj.strftime("%Y-%m-%dT%H:%M"),
                Open=kline[1],
                High=kline[2],
                Low=kline[3],
                Close=kline[4],
                Volume=kline[5],
                CloseTime=datetimeCloseObj.strftime("%Y-%m-%dT%H:%M"),
                QuoteAssetVolume=kline[7],
                NumberOfTrades=kline[8],
                TakerBuyBaseAssetVolume=kline[9],
                TakerBuyQuoteAssetVolume=kline[10],
            )

    def _requestAPI(self, startTime):
        if startTime:
            request = f'symbol=BTCUSDT&interval=1d&limit=1500&startTime={startTime}'
        else:
            request = 'symbol=BTCUSDT&interval=1d&limit=1500'
        klines = requests.get(BINANCE_API + request).text
        KlineReceiver._updateDB(self, json.loads(klines))

    def trigger(self):
        if Kline.objects.exists():
            startTime = Kline.objects.last().CloseTime
            startTime = int(time.mktime(startTime.timetuple()) * 1000)
        else:
            startTime = None
        KlineReceiver._requestAPI(self, startTime)

        columns = ['Close']
        if len(columns) > 1:
            data = []
            for i in range(len(columns)):
                thread = threading.Thread()
                thread.start()
                prediction_data = make_prediction(columns[i])
                prediction_data = [str(x) for x in prediction_data]
                data.append(prediction_data)
            data = tuple(zip(*data))
        else:
            data = make_prediction(columns[0])
        data = [[i[0].strftime("%Y-%m-%dT%H:%M"), i[1]] for i in data]
        dataModel = Prediction.objects.get()
        dataModel.data = data
        dataModel.save()


def trigger():
    klineReceiver = KlineReceiver()
    klineReceiver.trigger()
