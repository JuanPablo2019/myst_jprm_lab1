
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Calculation and Time Series visualization of Market Microstructure indicators.             -- #
# -- script: visualizations.py : python visualization functions                                          -- #
# -- author: JuanPablo2019                                                                               -- #
# -- license: GNU General Public License v3.                                                             -- #
# -- repository:https://github.com/JuanPablo2019/myst_jprm_lab1.git                                      -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import plotly.offline as pyo
import pandas as pd
import plotly.io as pio
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
#---------------OrderBook Plot------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------

def plot_orderbook(book):
    """
    Limit OrderBook horizontal bars plot.
    
    Parameters
    ----------

    Returns
    -------
    
    References
    ----------

    """
    buy_side=book[['bid_size', 'bid']]
    buy_side=buy_side.groupby(['bid']).sum()
    buy_side['side']='buy'
    sell_side=book[['ask_size', 'ask']]
    sell_side=sell_side.groupby(['ask']).sum()
    sell_side['side']='sell'
    
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
    
    
    
  
    fig = px.bar(ob,x='price',y='size',color='side')
    return fig.show()
    
    
#----------------Public Trades Plot-------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------

def plot_plot_publictrades(pt_data,begin=0, end=120001):
    """
    Public Trades horizontal bars + traded price plot.
    
    Horizontal Colored-Bars (y-axis is volume, bar color is side) + line (traded price)
    with y-axis: Volume y1-axis: Traded price, x-axis: Timestamp
    
    Parameters
    ----------
    pt_data: dataframe with public trades containing the following columns.
        timestamp:
        price: traded price
        amount: traded volume
        side: nature of the operatio buy/sell
    begin: the number of price where you want to start to visualize
           by default start from 0.
    end: the number of price where you want to end the visualization
         by default begin at the end of the datframe
         
        

    Returns
    figure with the 
    -------
    
    

    """
    
    pt_n = pt_data.groupby(['time2','price']).sum()
    pf=pd.DataFrame()
    pf['time'] = [j[0] for j in [i for i in pt_n.index]]
    pf['amount']=pt_n.amount.tolist()
    pf['price']=[j[1] for j in [i for i in pt_n.index]]
    pf.sort_values(by=['time'], inplace = True)

   
    #fig = make_subplots(specs=[[{"secondary_y": True}]])
    #fig = px.bar(pf, x='time',y='amount')
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                   vertical_spacing=0.1, subplot_titles=('Traded Price', ' Traded Volume'), 
                   row_width=[0.2, 0.7])
    
    fig.add_trace(go.Scatter(mode='lines',x=pf['time'][begin:end],y=pf['price'][begin:end]), row=1, col=1)
    fig.add_trace(go.Bar(x=pf['time'][begin:end],y=pf['amount'][begin:end]), row=2, col=1)
    
    fig.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
    return fig.show()
