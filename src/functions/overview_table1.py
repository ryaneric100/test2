# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 16:33:16 2022

@author: DCHELD
"""
from dash import  html
from dash import dash_table
import pandas as pd


def overview_table1():
        
        df = pd.read_csv('overview.csv')
        df['PORTFOLIO'] = [create_link(url,solution) for url,solution in zip(df["URL"],df["PORTFOLIO"])]
        df.drop(['URL'], axis = 1, inplace = True)
    
        df['TRADE ALERT'] = df['TRADE ALERT'].apply(lambda x: '🔴' if x > 0 else ' ')
        df['DATA ALERT'] = df['DATA ALERT'].apply(lambda x: '🔔' if x > 0 else ' ')
        
        test =  html.Div(
            [
                
                dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[{'id': c, 'name': c, 'presentation': 'markdown'} if c == 'PORTFOLIO' else {'id': c, 'name': c} for c in df.columns],
                    markdown_options={"link_target": '_self'},
                    style_cell_conditional=[
                        {
                    'if': {'column_id': c},
                    'textAlign': 'left'
                } for c in ['PORTFOLIO', 'STRATEGY']
                ],

                style_as_list_view=True,
                
                style_header={
                    'backgroundColor': '#A7C7E7',
                    'fontWeight': 'bold',
                    'border': '1px solid grey'
                    },
                style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(240, 240, 240)',
            }
            ],
                style_cell={'fontSize':12, 'font-family':'sans-serif', 'text-align': 'center'}, 
                css=[dict(selector= "p", rule= "margin: 0; text-align: left")]
                )
             
                                            
            ]
        )
        return test


def create_link(url:str,solution:str) -> str:
    return f'''[{solution}]({url}) '''