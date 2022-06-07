
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Calculation and Time Series visualization of Market Microstructure indicators.             -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: JuanPablo2019                                                                               -- #
# -- license: GNU General Public License v3.                                                             -- #
# -- repository:https://github.com/JuanPablo2019/myst_jprm_lab1.git                                      -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
# libraries
#from re import L
import numpy as np
import data as dt
import pandas as pd

# imported data
#data_ob=dt.ob_data

# función

def f_descriptive_ob(data_ob:dict) -> dict:
    """
    Docstring
  

    Parameters
    ----------
    data_ob : dict
        
        Datos de entrada del libro de ordenes, es un diccionario con la siguiente estructura:
        "timestamp": objeto tipo timestamp reconocible por maquina, e.g. pd.to_datetime()
        'bid_size:'volume de de niveles bid
        'bid:'volume de de niveles bid
        'ask:'volume de de niveles bid
        'ask_size:'volume de de niveles ask
            

    Returns
    -------
    r_data: dict
        Diccionario con las metricas calculadas 
        'median_ts_ob': float
        'midprice': float
        'spread': float
        
    References
    -------

    """
   
    
# Median time of orderbook update
    ob_ts = list(data_ob.keys())
    l_ts =[ pd.to_datetime(i_ts) for i_ts in ob_ts]
    ob_m1 = np.median([l_ts[n_ts+1] - l_ts[n_ts] for n_ts in range(0,len(l_ts)-1)]).total_seconds()*1000
    
    
    # spread midprice
    ob_m2 = [data_ob[ob_ts[i]]['ask'][0]-data_ob[ob_ts[i]]['bid'][0] for i in range(0,len(ob_ts))]
    
    # mid price
    ob_m3 = [(data_ob[ob_ts[i]]['ask'][0]+data_ob[ob_ts[i]]['bid'][0])*0.5 for i in range(0,len(ob_ts))]
    
    # No. price levels
    ob_m4 = [data_ob[i_ts].shape[0] for i_ts in ob_ts]
   
    # bid volume
    ob_m5= [np.round(data_ob[i_ts]['bid_size'].sum(),6) for i_ts in ob_ts]
    
    #ask volumne
    ob_m6= [np.round(data_ob[i_ts]['ask_size'].sum(),6) for i_ts in ob_ts]
    
    #total volumne
    ob_m7= [np.round(data_ob[i_ts]['bid_size'].sum()+data_ob[i_ts]['ask_size'].sum(),6) for i_ts in ob_ts]
    
    #order book imbalance
    ob_imb = [data_ob[i]['bid_size'].sum()/(data_ob[i]['bid_size'].sum()+data_ob[i]['ask_size'].sum()) for i in ob_ts]
    

    # weighted midprice
    ob_wm = [ob_imb[i]*ob_m3[i] for i in range(0,len(ob_ts))]
    
    #VWAP Volume Weighted Average Price
    
    vwap = [np.sum(data_ob[i]['bid']*data_ob[i]['bid_size'] + data_ob[i]['ask']*data_ob[i]['ask_size'])/np.sum(data_ob[i]['bid_size']+data_ob[i]['ask_size'])
        for i in ob_ts]
    
    r_data = {'median_ts_ob':ob_m1, 'spread': ob_m2, 'midprice': ob_m3, 'orderbook_imbalance': ob_imb, 'weighted_midprice':ob_wm,
              'Volume Weighted Average Price':vwap}
    
    
    return r_data

def transaction_vol_pt(pt_data):
    n_pt_data = pt_data['side'].resample('60T').count()
    return n_pt_data

def asset_volume_pt(pt_data):
    v_pt_data = pt_data['amount'].resample('60T').sum()
    return v_pt_data    

def ohlc(pt_data,n_pt_data,v_pt_data):
    ohlc = pd.DataFrame()

    ohlc['Hour'] = pt_data['price'].resample('60T').last().index
    ohlc['Opening'] = pt_data['price'].resample('60T').first().values
    ohlc['Close'] = pt_data['price'].resample('60T').last().values
    ohlc['Max'] = pt_data['price'].resample('60T').max().values
    ohlc['Min'] = pt_data['price'].resample('60T').min().values
    ohlc['Transaction Volume']=n_pt_data.values
    ohlc['Asset Volume']=v_pt_data.values
    
    return ohlc

def td_imb_pt(pt_data):
    
    pt_data['amount']=[j*-1 if i == 'sell' else j for i,j in zip(pt_data['side'],pt_data['amount'])]
    td_imb = pt_data['amount'].resample('60T').sum()
    return td_imb


