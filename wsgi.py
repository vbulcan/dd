server = app.server
# -*- coding: utf-8 -*-

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
from datetime import datetime as dt

# Initiate app
app = dash.Dash(__name__)

# Set server variable (necessary if you plan to deploy the app)
application = app.server

# Reference hosted CSS
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

# Import data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
continents = pd.unique(df['continent'])
years = pd.unique(df['year'])

app.layout = html.Div(
    children=[
        html.Div(className='row',
                 style={'backgroundColor': 'rgb(56, 83, 108)',
                        'color':'white', 'padding': 30},
                 children=[html.Div(className='nine columns',
                                    children=[
                                        html.H1("Hello Dash!",
                                                style={'paddingBottom':0}),
                                        html.H6("A Pythonic Framework for Analytic Web Applications",
                                                style={'paddingTop':0, 'paddingBottom':0}),
                                        html.H6(children=[html.A('Contact Plotly',
                                                                 href='https://plotly.typeform.com/to/ocektY',
                                                                 style={'color': 'white', 'textAlign': 'right'})])
                                    ]),
                            html.Div(className='three columns',
                                     style={'float': 'right', 'paddingLeft': 20},
                                     children=[
                                        html.Img(src='https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe-inverted.png',
                                                 style={'maxWidth':'100%'}),
                            ])
        ]),
        html.Div(className='row',
                 style={'padding': 40, 'color':'#39536B'},
                 children=[html.Div(className='four columns',
                                    children=[html.H6('Add Continents:'),
                                              dcc.Dropdown(id='my-dropdown',
                                                           options=[{'label': continents[i],
                                                                     'value': continents[i]} for i in range(len(continents))],
                                                            value='Asia',
                                                            multi=True)]),
                           html.Div(className='eight columns',
                                    children=[html.H6('Select a Year:'),
                                             dcc.Slider(id='my-slider',
                                                        min=1952,
                                                        max=2007,
                                                        step=5,
                                                        value=1952,
                                                        marks={str(i): '{}'.format(i) for i in years})])
        ]),
        html.Div(className='row',
                 style={'padding': 40},
                 children=[dcc.Graph(id='my-graph')]),
])

@app.callback(Output('my-graph', 'figure'),
             [Input('my-dropdown', 'value'),
              Input('my-slider', 'value')])
def update_graph(dropdown_vals, slider_val):
    if not isinstance(dropdown_vals, (list,)):
        dropdown_vals=[dropdown_vals]

    colors = ['#229FFC', '#a6d8fd', '#39536B', '#a6adfd', '#36C9EF',]
    data = []

    for i in range(len(dropdown_vals)):
        color = colors[i]
        cont = dropdown_vals[i]
        dff = df[(df['continent']==cont) & (df['year']==slider_val)]

        data.append({'type': 'scatter',
                     'x': dff['gdpPercap'],
                     'y': dff['lifeExp'],
                     'text': dff['country'],
                     'mode': 'markers',
                     'name': cont,
                     'marker':{'color': color,
                               'sizemin':6,
                               'sizemode':'area',
                               'sizeref': 250000,
                               'size':dff['pop']}})

    layout = {'title':slider_val,
              'showlegend': True,
              'xaxis': {'title': 'GDP Per Capita<br>Sized by Population',
                        'zeroline': False,
                        'showline': False,
                        'showgrid': False},
              'yaxis': {'title': 'Life Expectancy',
                        'showline': False,
                        'showgrid': False},
               'margin': {'l': 60, 'r': 40, 't': 40, 'b': 60}}
    return {'data': data, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)
