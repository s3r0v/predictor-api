from django.db import models
import datetime, requests, json, time
from reviewers.settings import BINANCE_API


class Kline(models.Model):
    openTime = models.DateTimeField(verbose_name='Open Time')
    open = models.FloatField(verbose_name='Open')
    high = models.FloatField(verbose_name='High')
    low = models.FloatField(verbose_name='Low')
    close = models.FloatField(verbose_name='Close')
    volume = models.FloatField(verbose_name='Volume')
    closeTime = models.DateTimeField(verbose_name='Close Time')
    quoteAssetVolume = models.FloatField(verbose_name='Quote Asset Volume')
    numberOfTrades = models.IntegerField(verbose_name='Number Of Trades')
    takerBuyBaseAssetVolume = models.FloatField(verbose_name='Taker buy base asset volume')
    takerBuyQuoteAssetVolume = models.FloatField(verbose_name='Taker buy quote asset volume')

    class Meta:
        verbose_name = 'Kline'
        verbose_name_plural = 'Klines'


class KlineReceiver:
    def __init__(self):
        self.binanceApi = BINANCE_API

    def _updateDB(self, klines):
        print(len(klines))
        for kline in klines:
            datetimeOpenObj = datetime.datetime.utcfromtimestamp(int(kline[0]) / 1000)
            datetimeCloseObj = datetime.datetime.utcfromtimestamp(int(kline[6]) / 1000)
            Kline.objects.create(
                openTime=datetimeOpenObj.strftime("%Y-%m-%dT%H:%M"),
                open=kline[1],
                high=kline[2],
                low=kline[3],
                close=kline[4],
                volume=kline[5],
                closeTime=datetimeCloseObj.strftime("%Y-%m-%dT%H:%M"),
                quoteAssetVolume=kline[7],
                numberOfTrades=kline[8],
                takerBuyBaseAssetVolume=kline[9],
                takerBuyQuoteAssetVolume=kline[10],
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
            startTime = Kline.objects.last().closeTime
            startTime = int(time.mktime(startTime.timetuple()) * 1000)
        else:
            startTime = None
        KlineReceiver._requestAPI(self, startTime)
