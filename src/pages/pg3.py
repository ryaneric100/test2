import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import pandas as pd
from dash import dash_table
import dash_bootstrap_components as dbc
from  functions.portfolio import portfolio
from  functions.positions import positions


dash.register_page(__name__,
                   path='/portfolio1',
                   name='Portfolio1',
                   title='Portfolio',
                   image='pg3.png',
                   description='Learn all about the heatmap.'
)


# call the function
#portfolio()

layout = html.Div(    
    [
     html.Div(id="csv-button"), 
     
 dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Positions", tab_id="tab-positions"),
                    dbc.Tab(label="Trading", tab_id="tab-trading"),
                    dbc.Tab(label="Stats", tab_id="tab-2"),
                    dbc.Tab(label="Allocations", tab_id="tab-3"),
                    dbc.Tab(label="Contributions", tab_id="tab-4"),
                    dbc.Tab(label="Info & Rankings", tab_id="tab-5"),
                    dbc.Tab(label="Data", tab_id="tab-6"),
                ],
                id="card-tabs",
                active_tab="tab-positions",
            )
        ),
        dbc.CardBody(html.P(id="card-content", className="card-text")),
    ]
)
 
 
  ]
)


@callback(
    Output("card-content", "children"), [Input("card-tabs", "active_tab")]
)

def render_content(active_tab):
    if active_tab == 'tab-positions':
        return positions()
    elif active_tab == 'tab-trading':
        return html.Div([
            html.H3('Tab content 2'),
            dcc.Graph(
                figure=dict(
                    data=[dict(
                        x=[1, 2, 3],
                        y=[5, 10, 6],
                        type='bar'
                    )]
                )
            )
        ])
    elif active_tab == 'tab-3':
        return portfolio()
    
    
    
    
@callback(
  Output("portfolio-grid", "enableExportDataAsCsv"),
  Input("csv-button", "n_clicks"),
  )
def export_data_as_csv(n_clicks):
  if n_clicks:
    return True

#  return False     
   
    