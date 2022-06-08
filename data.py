
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Calculation and Time Series visualization of Market Microstructure indicators.             -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: JuanPablo2019                                                                               -- #
# -- license: GNU General Public License v3.                                                             -- #
# -- repository:https://github.com/JuanPablo2019/myst_jprm_lab1.git                                      -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""


#%% libraries

import pandas as pd
import json



#%% Orderbook data

f = open('orderbooks_05jul21.json')
orderbooks_data = json.load(f)

#%% orderbook data wranging

ob_data = orderbooks_data['bitfinex']

ob_data = {i_key: i_value for i_key, i_value in ob_data.items() if i_value is not None}

ob_data = {i_ob: pd.DataFrame(ob_data[i_ob])[['bid_size','bid','ask','ask_size']]
                   if ob_data[i_ob] is not None else None for i_ob in list(ob_data.keys())}

#%% Public trades data

pt_data = pd.read_csv('btcusdt_binance.csv',header=0, encoding='utf-8-sig')

#%% public trades data wrangling

pt_data.drop('Unnamed: 0',inplace=True, axis=1)
pt_data.index = pd.to_datetime(pt_data['timestamp'])
pt_data['time2']=pt_data['timestamp']
