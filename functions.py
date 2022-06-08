
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
data_ob=dt.ob_data
pt_data=dt.pt_data
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
    
    # Weighted midprice (B) (TOB) for extrapoints
    # W-MidPrice-B = [ask_volume/(total_volume)] *bid_price+[bid_volume/(total_volume)]*ask_price
    # W-MidPrice-B = (v[1]/np.sum(v[0]+v[1]))*p[0]+(v[0]/np.sum(v[0]+v[1]))*p[1]
    #VWAP Volume Weighted Average Price
    
    vwap = [np.sum(data_ob[i]['bid']*data_ob[i]['bid_size'] + data_ob[i]['ask']*data_ob[i]['ask_size'])/np.sum(data_ob[i]['bid_size']+data_ob[i]['ask_size'])
        for i in ob_ts]
    
    #OHLCV con mid price open, high, low, close, volume (Quoted volume)
    
    
    r_data = {'median_ts_ob':ob_m1, 'spread': ob_m2, 'midprice': ob_m3, 'orderbook_imbalance': ob_imb, 'weighted_midprice':ob_wm,
              'Volume Weighted Average Price':vwap}
    
    
    
    
    return r_data

#Public trade metrics

def f_publictrades_metrics(data_pt):
    """
    

    Parameters
    ----------
    data_pt : dict
        DESCRIPTION.

    Returns
    -------
    None.

    """
    # resampling for 1H
    # for each period
    
    # -- (1) Buy Trade Count -- #
    b_pt_data =pt_data[pt_data['side']=='buy']['side'].resample('60T').count()
    # -- (2) Sell Trade Count -- #
    s_pt_data =pt_data[pt_data['side']=='sell']['side'].resample('60T').count()
    # -- (3) Total Trade Count -- #
    n_pt_data = pt_data['side'].resample('60T').count()
    # -- (4) Difference in Trade Count (Buy-Sell) -- #
    diff_pt_data = b_pt_data - s_pt_data
  
    # -- (5) Sell Volume  -- #
    sv_pt_data = pt_data['amount'][pt_data['side']=='sell'].resample('60T').sum()
    # -- (6) Buy Volume -- #
    bv_pt_data = pt_data['amount'][pt_data['side']=='buy'].resample('60T').sum()
    # -- (6) Total Volume -- #
    v_pt_data = pt_data['amount'].resample('60T').sum()
    # -- (4) Difference in Volume (Buy-Sell) -- #
    diffv_pt_data = bv_pt_data-sv_pt_data

    
      


    ohlc = pd.DataFrame()

    ohlc['Hour'] = pt_data['price'].resample('60T').last().index
    ohlc['Opening'] = pt_data['price'].resample('60T').first().values
    ohlc['Close'] = pt_data['price'].resample('60T').last().values
    ohlc['Max'] = pt_data['price'].resample('60T').max().values
    ohlc['Min'] = pt_data['price'].resample('60T').min().values
    ohlc['Transaction Volume']=n_pt_data.values
    ohlc['Asset Volume']=v_pt_data.values
    
    
    

    td_imb = pt_data.apply(lambda x: x[2]*-1 if x[3] == 'sell' else x[2],axis=1).resample('60T').sum()
    
    
    
    p_data = {'Buy Trade Count': b_pt_data, 'Sell Trade Count':  s_pt_data,
              'Total Trade Count': n_pt_data, 'Difference in Trade Count': diff_pt_data, 
              'Total Volume':v_pt_data,'Buy Volume':bv_pt_data,'Sell Volume':sv_pt_data,
              'Difference in Volume':diffv_pt_data,
              'OHLCVV':ohlc,'Trade Flow Imbalance': td_imb}
    
    return p_data
    


