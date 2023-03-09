# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 16:33:16 2022

@author: DCHELD
"""
from dash import dcc, html



def portfolio():
        test =  html.Div([
            html.H3('Tab content 3'),
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
        return test

