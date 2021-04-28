import plotly.graph_objects as go
import plotly.express as px

from ebayscraper import product_price_lists
from ebayscraper import models_product_info


x_values = ['3070', '3080', '3090']
retail_price = [499.99, 699.99, 1499.99]

ebay_dict = product_price_lists()
ebay_avgs = list(ebay_dict['Averages'].values())
ebay_lows = list(ebay_dict['Lows'].values())
ebay_highs = list(ebay_dict['Highs'].values())
ebay_lows_text = [f"{int(round(ebay_lows[idxLow]/retail_price[idxLow]*100, 0))}% increase from retail" for idxLow in range(len(ebay_lows))]
ebay_avgs_text = [f"{int(round(ebay_avgs[idxAvg]/retail_price[idxAvg]*100, 0))}% increase from retail" for idxAvg in range(len(ebay_avgs))]
ebay_highs_text = [f"{int(round(ebay_highs[idxHigh]/retail_price[idxHigh]*100, 0))}% increase from retail" for idxHigh in range(len(ebay_highs))]

fig_data = [
    go.Bar(name='Retail', x=x_values, y=retail_price, marker_color='lightslategray',
           marker_line_color='black', marker_line_width=1.5, opacity=0.6),
    go.Bar(name='eBay Lowest', x=x_values, y=ebay_lows, marker_color='lightblue',
           marker_line_color='black', marker_line_width=1.5, opacity=0.6,
           text=ebay_lows_text),
    go.Bar(name='eBay Average', x=x_values, y=ebay_avgs, marker_color='blue',
           marker_line_color='black', marker_line_width=1.5, opacity=0.6,
           text=ebay_avgs_text),
    go.Bar(name='eBay Highest', x=x_values, y=ebay_highs, marker_color='darkblue',
           marker_line_color='black', marker_line_width=1.5, opacity=0.6,
           text=ebay_highs_text)]

fig_layout = go.Layout(
    title={
        'text': 'Price of RTX 3000 series GPUs',
        'font': {'size': 30}},
    xaxis={
        'title': 'Model',
        'titlefont': {'size': 18}},
    yaxis={
        'title': 'Price',
        'titlefont': {'size': 18}})

fig = go.Figure(data=fig_data, layout=fig_layout)
fig.update_layout(title_x=0.5, barmode='group')
fig.show()
