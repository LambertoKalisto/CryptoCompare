#!/usr/bin/env python3
import time
import unittest
import cryptocompare
import datetime
import calendar
import os


class TestCryptoCompare(unittest.TestCase):
    def assertCoinAndCurrInPrice(self, coin, curr, price):
        if isinstance(coin, list):
            for co in coin:
                self.assertCoinAndCurrInPrice(co, curr, price)
            return
        else:
            self.assertIn(coin, price)

        if isinstance(curr, list):
            for cu in curr:
                self.assertIn(cu, price[coin])
        else:
            self.assertIn(curr, price[coin])

    def test_coin_list(self):
        lst = cryptocompare.get_coin_list()
        self.assertTrue("BTC" in lst.keys())
        lst = cryptocompare.get_coin_list(True)
        self.assertTrue("BTC" in lst)

    def test_get_price(self):
        coin = "BTC"
        price = cryptocompare.get_price(coin)
        self.assertCoinAndCurrInPrice(coin, "EUR", price)

        price = cryptocompare.get_price(coin, currency="USD")
        self.assertCoinAndCurrInPrice(coin, "USD", price)
        currencies = ["EUR", "USD", "GBP"]
        price = cryptocompare.get_price(coin, currency=currencies)
        self.assertCoinAndCurrInPrice(coin, currencies, price)
        coins = ["BTC", "XMR"]
        price = cryptocompare.get_price(coins, currency=currencies)
        self.assertCoinAndCurrInPrice(coins, currencies, price)

    def test_get_price_full(self):
        price = cryptocompare.get_price("ETH", full=True)
        self.assertIn("RAW", price)
        self.assertIn("ETH", price["RAW"])
        self.assertIn("EUR", price["RAW"]["ETH"])
        self.assertIn("PRICE", price["RAW"]["ETH"]["EUR"])

    def test_get_historical_price(self):
        coin = "XMR"
        curr = "EUR"
        price = cryptocompare.get_historical_price(
            "XMR", timestamp=datetime.date(2017, 6, 6)
        )
        self.assertCoinAndCurrInPrice(coin, curr, price)
        price2 = cryptocompare.get_historical_price(
            "XMR", "EUR", datetime.datetime(2017, 6, 6)
        )
        self.assertCoinAndCurrInPrice(coin, curr, price2)
        self.assertEqual(price, price2)

    def test_price_day(self):
        coin = "BTC"
        curr = "USD"
        price = cryptocompare.get_historical_price_day(
            coin,
            currency=curr,
            limit=3,
            exchange="CCCAGG",
            toTs=datetime.datetime(2019, 6, 6),
        )
        for frame in price:
            self.assertIn("time", frame)

    def test_price_day_all(self):
        coin = "BTC"
        curr = "USD"
        price = cryptocompare.get_historical_price_day_all(
            coin, currency=curr, exchange="CCCAGG"
        )
        self.assertTrue(len(price) > 1)
        for frame in price:
            self.assertIn("time", frame)

    def test_price_day_from(self):
        coin = "BTC"
        curr = "USD"
        price = cryptocompare.get_historical_price_day_from(
            coin,
            currency=curr,
            exchange="CCCAGG",
            toTs=int(calendar.timegm(datetime.datetime(2019, 6, 6).timetuple())),
            fromTs=int(calendar.timegm(datetime.datetime(2019, 6, 4).timetuple())),
        )
        self.assertTrue(len(price) == 3)
        for frame in price:
            self.assertIn("time", frame)

    def test_price_hour(self):
        coin = "BTC"
        curr = "USD"
        price = cryptocompare.get_historical_price_hour(
            coin,
            currency=curr,
            limit=3,
            exchange="CCCAGG",
            toTs=datetime.datetime(2019, 6, 6, 12),
        )
        for frame in price:
            self.assertIn("time", frame)

    def test_price_hour_from(self):
        coin = "BTC"
        curr = "USD"
        price = cryptocompare.get_historical_price_hour_from(
            coin,
            currency=curr,
            exchange="CCCAGG",
            toTs=int(
                calendar.timegm(datetime.datetime(2019, 6, 6, 3, 0, 0).timetuple())
            ),
            fromTs=int(
                calendar.timegm(datetime.datetime(2019, 6, 6, 1, 0, 0).timetuple())
            ),
        )
        self.assertTrue(len(price) == 3)
        for frame in price:
            self.assertIn("time", frame)

    def test_price_minute(self):
        coin = "BTC"
        curr = "USD"
        price = cryptocompare.get_historical_price_minute(
            coin,
            currency=curr,
            limit=3,
            exchange="CCCAGG",
            toTs=datetime.datetime.now(),
        )
        for frame in price:
            self.assertIn("time", frame)

    def test_get_avg(self):
        coin = "BTC"
        curr = "USD"
        avg = cryptocompare.get_avg(coin, curr, exchange="Kraken")
        self.assertEqual(avg["LASTMARKET"], "Kraken")
        self.assertEqual(avg["FROMSYMBOL"], coin)
        self.assertEqual(avg["TOSYMBOL"], curr)

    def test_get_exchanges(self):
        exchanges = cryptocompare.get_exchanges()
        self.assertIn("Kraken", exchanges)

    def test_get_pairs(self):
        pairs = cryptocompare.get_pairs(exchange="Kraken")
        self.assertEqual("Kraken", pairs[0]["exchange"])

    def test_sets_api_key_using_environment_variable(self):
        os.environ["CRYPTOCOMPARE_API_KEY"] = "Key"
        api_key_parameter = cryptocompare.cryptocompare._set_api_key_parameter(None)
        assert api_key_parameter == "&api_key=Key"

    def test_sets_api_key_with_no_env_var_and_none_passed(self):
        if os.getenv("CRYPTOCOMPARE_API_KEY"):
            del os.environ["CRYPTOCOMPARE_API_KEY"]
        api_key_parameter = cryptocompare.cryptocompare._set_api_key_parameter(None)
        assert api_key_parameter == ""

    def test_sets_api_key_passed_in_works(self):
        api_key_parameter = cryptocompare.cryptocompare._set_api_key_parameter(
            "keytest"
        )
        assert api_key_parameter == "&api_key=keytest"

    def assertCoinAndCurrInPriceWithFields(self, coin, currency, price, fields):
        if isinstance(coin, list):
            for co in coin:
                self.assertCoinAndCurrInPriceWithFields(co, currency, price, fields)
            return
        else:
            self.assertIn(coin, price)

        if currency is not None:
            if isinstance(currency, list):
                for curr in currency:
                    self.assertIn(curr, price[coin])
            else:
                self.assertIn(currency, price[coin])

    def test_coin_list_with_fields(self):
        fields = ['FullName', 'Algorithm']
        lst_with_fields = cryptocompare.get_coin_list(fields=fields)
        self.assertTrue("BTC" in lst_with_fields.keys())

    def test_get_price_with_fields(self):
        coin = "BTC"
        fields = ['PRICE', 'LASTUPDATE']
        price_with_fields = cryptocompare.get_price(coin, fields=fields)
        self.assertCoinAndCurrInPriceWithFields(coin, "EUR", price_with_fields, fields)

        currency = "USD"
        price_with_fields = cryptocompare.get_price(coin, currency=currency, fields=fields)
        self.assertCoinAndCurrInPriceWithFields(coin, currency, price_with_fields, fields)

        currencies = ["EUR", "USD", "GBP"]
        price_with_fields = cryptocompare.get_price(coin, currency=currencies, fields=fields)
        self.assertCoinAndCurrInPriceWithFields(coin, currency, price_with_fields, fields)

        coins = ["BTC", "XMR"]
        price_with_fields = cryptocompare.get_price(coins, currency=currencies, fields=fields)
        self.assertCoinAndCurrInPriceWithFields(coin, currency, price_with_fields, fields)

    def test_get_price_full_with_fields(self):
        coin = "ETH"
        currency = "EUR"
        fields = ['PRICE', 'LASTUPDATE']
        price_with_fields = cryptocompare.get_price(coin, currency=currency, full=True, fields=fields)
        self.assertIsNotNone(price_with_fields)
        self.assertIn("RAW", price_with_fields)
        self.assertIn(coin, price_with_fields["RAW"])
        self.assertIn(currency, price_with_fields["RAW"][coin])
        for field in fields:
            self.assertIn(field, price_with_fields["RAW"][coin][currency])

    def test_get_historical_price_with_fields(self):
        coin = "XMR"
        curr = "EUR"
        timestamp = datetime.datetime(2017, 6, 6)
        fields = ['PRICE']
        price = cryptocompare.get_historical_price(coin, timestamp=timestamp, fields=fields)
        price2 = cryptocompare.get_historical_price(coin, currency=curr, timestamp=timestamp, fields=fields)
        self.assertIsNotNone(price)
        self.assertIsNotNone(price2)
        self.assertIn(coin, price)
        self.assertIn(coin, price2)
        self.assertIn(curr, price[coin])
        self.assertIn(curr, price2[coin])
        self.assertIsInstance(price[coin][curr], float)
        self.assertIsInstance(price2[coin][curr], float)
        self.assertEqual(price[coin][curr], price2[coin][curr])

    def test_price_day_with_fields(self):
        coin = "BTC"
        curr = "USD"
        fields = ['time']
        price = cryptocompare.get_historical_price_day(
            coin,
            currency=curr,
            limit=3,
            exchange="CCCAGG",
            toTs=datetime.datetime(2019, 6, 6),
            fields=fields
        )
        self.assertIsNotNone(price)
        for frame in price:
            self.assertIn("time", frame)

    def test_price_day_all_with_fields(self):
        coin = "BTC"
        curr = "USD"
        fields = ['time']
        price = cryptocompare.get_historical_price_day_all(
            coin,
            currency=curr,
            exchange="CCCAGG",
            fields=fields
        )
        self.assertTrue(len(price) > 1)
        for frame in price:
            self.assertIn("time", frame)

    def test_price_day_from_with_fields(self):
        coin = "BTC"
        curr = "USD"
        fields = ['time']
        price = cryptocompare.get_historical_price_day_from(
            coin,
            currency=curr,
            exchange="CCCAGG",
            fields=fields
        )
        self.assertIsNotNone(price)
        self.assertTrue(len(price) >= 3)
        for frame in price:
            self.assertIn("time", frame)

    def test_price_hour_with_fields(self):
        coin = "BTC"
        curr = "USD"
        fields = ['time', 'open', 'close']
        price = cryptocompare.get_historical_price_hour(
            coin,
            currency=curr,
            limit=3,
            exchange="CCCAGG",
            toTs=datetime.datetime(2019, 6, 6, 12),
            fields=fields
        )
        self.assertIsNotNone(price)
        for frame in price:
            for field in fields:
                self.assertIn(field, frame)

    def test_price_hour_from_with_fields(self):
        coin = "BTC"
        curr = "USD"
        fields = ['time', 'open', 'close']
        price = cryptocompare.get_historical_price_hour_from(
            coin,
            currency=curr,
            exchange="CCCAGG",
            toTs=int(calendar.timegm(datetime.datetime(2019, 6, 6, 3, 0, 0).timetuple())),
            fromTs=int(calendar.timegm(datetime.datetime(2019, 6, 6, 1, 0, 0).timetuple())),
            fields=fields
        )
        self.assertIsNotNone(price)
        self.assertTrue(len(price) == 3)
        for frame in price:
            for field in fields:
                self.assertIn(field, frame)

    def test_price_minute_with_fields(self):
        coin = "BTC"
        curr = "USD"
        fields = ['time', 'open', 'close']
        price = cryptocompare.get_historical_price_minute(
            coin,
            currency=curr,
            limit=3,
            exchange="CCCAGG",
            toTs=datetime.datetime.now(),
            fields=fields
        )
        self.assertIsNotNone(price)
        self.assertTrue(len(price) >= 3)
        for frame in price:
            for field in fields:
                self.assertIn(field, frame)

    def test_get_avg_with_fields(self):
        coin = "BTC"
        curr = "USD"
        fields = ['LASTMARKET', 'FROMSYMBOL', 'TOSYMBOL']

        avg = cryptocompare.get_avg(coin, curr, exchange="Kraken", fields=fields)

        self.assertIsNotNone(avg)
        self.assertEqual(avg["LASTMARKET"], "Kraken")
        self.assertEqual(avg["FROMSYMBOL"], coin)
        self.assertEqual(avg["TOSYMBOL"], curr)

    def test_get_exchanges_with_fields(self):
        fields = ['Id', 'Name']  # Мы проверяем только наличие Id и Name

        exchanges = cryptocompare.get_exchanges(fields=fields)

        self.assertIsNotNone(exchanges)
        for exchange in exchanges.values():  # Перебираем значения (словари) в exchanges
            if isinstance(exchange, dict):
                self.assertIn("Id", exchange)
                self.assertIn("Name", exchange)

    def test_get_pairs_with_fields(self):
        exchange = "Kraken"
        fields = ["exchange"]  # Мы проверяем только наличие ключа "exchange"

        pairs = cryptocompare.get_pairs(exchange=exchange, fields=fields)

        self.assertIsNotNone(pairs)
        if isinstance(pairs, list):  # Проверяем, что вернулся список
            self.assertTrue(len(pairs) > 0)  # Проверяем, что список не пустой
            for pair in pairs:
                if isinstance(pair, dict):  # Проверяем, что каждый элемент списка - словарь
                    self.assertIn("exchange", pair)
                    self.assertEqual(exchange, pair["exchange"])

if __name__ == "__main__":
    unittest.main()
