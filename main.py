
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Calculation and Time Series visualization of Market Microstructure indicators.             -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: JuanPablo2019                                                                               -- #
# -- license:   GNU General Public License v3.                                                           -- #
# -- repository: https://github.com/JuanPablo2019/myst_jprm_lab1.git                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import data as dt
import functions as fn
#from functions import f_publictrades_metrics,f_descriptive_ob

data_1 = fn.f_descriptive_ob(dt.ob_data)

#%% Public trades functions dict output test

data_2 =fn.f_publictrades_metrics(dt.pt_data)
#%%
a=pt_data.apply(lambda x: x[2]*-1 if x[3] == 'sell' else x[2],axis=1)

#%%
td_imb = pt_data.apply(lambda x: x[2]*-1 if x[3] == 'sell' else x[2],axis=1).resample('60T').sum()
    #td_imb=pd.DataFrame([j*-1 if i == 'sell' else j for i,j in zip(pt_data['side'],pt_data['amount'])]).resample('60T').sum()
    #pt_data['amount']=[j*-1 if i == 'sell' else j for i,j in zip(pt_data['side'],pt_data['amount'])]
td_imb =td_imb.resample('60T').sum()

#%%
#vwap = [np.sum(data_ob[i]['bid']*data_ob[i]['bid_size'] + data_ob[i]['ask']*data_ob[i]['ask_size'])/np.sum(data_ob[i]['bid_size']+data_ob[i]['ask_size'])
 #       for i in ob_ts]
ob_ts = list(dt.ob_data.keys())
import pandas as pd
ohlcv = [pd.DataFrame(dt.ob_data[i]) for i in ob_ts]

#%%
from scipy.stats import moment,skew

#a = skew(data_1['orderbook_imbalance'])

#%%
book = dt.ob_data[list(dt.ob_data.keys())[0]]

buy_side=book[['bid_size', 'bid']]
buy_side=buy_side.groupby(['bid']).sum()
buy_side['side']='buy'
sell_side=book[['ask_size', 'ask']]
sell_side=sell_side.groupby(['ask']).sum()
sell_side['side']='sell'

#%%


price_bid = list(buy_side.index)
price_ask = list(sell_side.index)
price_levels = price_bid + price_ask


s_bid = list(buy_side['bid_size'])
s_ask = list(sell_side['ask_size'])
size_levels = s_bid + s_ask


b_side = list(buy_side['side'])
a_side = list(sell_side['side'])
side_levels = b_side + a_side


ob = pd.DataFrame()
ob['price']=price_levels
ob['size']=size_levels
ob['side']=side_levels

#%%
import plotly.io as pio
pio.renderers.default = "browser"
import plotly.express as px
fig = px.bar(ob,x='price',y='size',color='side')
fig.show()


#%%

fn.plot_orderbook(book)

#%% test plot public trades
import plotly.graph_objects as go

pt_data = dt.pt_data.sort_values(by=['time2'])
pf=pd.DataFrame()

#%%

#%%
pt_n = pt_data.groupby(['time2','price']).sum()
pf['time'] = [j[0] for j in [i for i in pt_n.index]]
pf['amount']=pt_n.amount.tolist()
pf['price']=[j[1] for j in [i for i in pt_n.index]]
pf.sort_values(by=['time'], inplace = True)
#%%
from plotly.subplots import make_subplots
#fig = make_subplots(specs=[[{"secondary_y": True}]])
#fig = px.bar(pf, x='time',y='amount')
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
               vertical_spacing=0.03, subplot_titles=('Public Traded Price', ' Traded Volume'), 
               row_width=[0.2, 0.7])

fig.add_trace(go.Scatter(mode='lines',x=pf['time'][0:10000],y=pf['price'][0:10000]), row=1, col=1)
fig.add_trace(go.Bar(x=pf['time'][0:10000],y=pf['amount'][0:10000]),row=2, col=1)


fig.show()
