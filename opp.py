import MetaTrader5 as mt5
import pandas as pd
from ta.trend import MACD

if not mt5.initialize(login= 2001070029, password="Ricmwas2015!", server="JustMarkets-Demo" ):
    print("Failed to initialize MetaTrader 5", mt5.last_error())
    quit()

rates = mt5.copy_rates_from_pos("GBPUSD.m", mt5.TIMEFRAME_H1, 0, 1000)

if rates is None:
    print("Failed to fetch rates:", mt5.last_error())
else:
    rates = pd.DataFrame(rates)
    rates['time'] = pd.to_datetime(rates['time'], unit='s')
    # rates.set_index('time', inplace=True)
    # rates.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'tick_volume': 'Tick_Volume', 'spread': 'Spread', 'real_volume': 'Real_Volume'}, inplace=True)

macd= MACD(
    close=rates['close'],
    window_slow=26,
    window_fast=12,
    window_sign=9
)
rates['MACD'] = macd.macd()
rates['MACD_Signal'] = macd.macd_signal()
rates['MACD_Histogram'] = macd.macd_diff()

# Initialize signal column
rates['MACD_Signal_Side'] = 0  # 0 = Hold, 1 = Buy, -1 = Sell

# Buy Signal: MACD crosses above Signal line
buy_signal = (rates['MACD'].shift(1) < rates['MACD_Signal'].shift(1)) & \
             (rates['MACD'] > rates['MACD_Signal'])

# Sell Signal: MACD crosses below Signal line
sell_signal = (rates['MACD'].shift(1) > rates['MACD_Signal'].shift(1)) & \
              (rates['MACD'] < rates['MACD_Signal'])

# Assign signals
rates.loc[buy_signal, 'MACD_Signal_Side'] = 1
rates.loc[sell_signal, 'MACD_Signal_Side'] = -1


print("Rates fetched successfully:", rates.tail()['MACD_Signal_Side'])
print(rates.MACD_Signal_Side.value_counts())


if rates.MACD_Signal_Side[-1]==1:
    print("Buy Signal Detected")
    # Execute buy order logic here

elif rates.MACD_Signal_Side[-1]==-1:
    print("Sell Signal Detected")
    # Execute sell order logic here
else:
    print("No Signal Detected")

