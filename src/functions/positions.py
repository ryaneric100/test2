# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 16:33:16 2022

@author: DCHELD
"""

from dash import Input, Output, html, callback
import pandas as pd
import dash_ag_grid as dag
import dash_bootstrap_components as dbc


def positions():
        
    
        df = pd.read_csv('positions.csv')
    
    
        test =  html.Div(
            [
  

                dag.AgGrid(
                  id="portfolio-grid",
                  className="ag-theme-alpine-dark",
                  columnDefs=[{"headerName": i, "field": i, "cellRenderer": "markdown"} for i in df.columns],
                  rowData=df.to_dict("records"),
                  columnSize="sizeToFit",
                  #defaultColDef=defaultColDef,
                  #cellStyle=cellStyle,
                  dangerously_allow_html=True,
                  dashGridOptions={"undoRedoCellEditing": True, "rowSelection": "single", "pagination": False,"paginationAutoPageSize":True},
                  # style = {"height": "800px", "width": "100%"},
                  csvExportParams={
                  "fileName": "ag_grid_test.csv",
                 },
              ),
                
                html.Div(
                    html.Button("Download CSV", id="csv-button", n_clicks=0),
               ), 
                  
              
                                            
            ])
                
        
        return test
        
    
    


        

    
    


     
        
     
        
     
        