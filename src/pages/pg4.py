import dash
from dash import dcc, html
import pandas as pd
from dash import dash_table

dash.register_page(__name__,
                   path='/datatable2',
                   name='Overview Portfolios2',
                   title='Overview Portfolios2',
                   image='pg3.png',
                   description='Learn all about the heatmap.'
)


df = pd.read_csv('overview3.csv')


def create_link(url:str,solution:str) -> str:
    return f'''[{solution}]({url}) '''


df['SOLUTION'] = [create_link(url,solution) for url,solution in zip(df["URL"],df["SOLUTION"])]
df.drop(['URL'], axis = 1, inplace = True)

#  columns=[{'id': c, 'name': c} for c in df.columns],

layout = html.Div(
    [
        dcc.Markdown('### Overview Portfolios', style={'fontSize':12, 'font-family':'sans-serif','textAlign':'left'}),
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'id': c, 'name': c, 'presentation': 'markdown'} if c == 'SOLUTION' else {'id': c, 'name': c} for c in df.columns],
            markdown_options={"link_target": '_self'},
            style_cell_conditional=[
                {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['SOLUTION', 'STRATEGY']
        ],

        style_as_list_view=True,
        
        style_header={
            'backgroundColor': 'GREY',
            'fontWeight': 'bold'
            },
        style_data_conditional=[
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(220, 220, 220)',
    }
    ],
        style_cell={'fontSize':12, 'font-family':'sans-serif', 'text-align': 'center'}, 
        css=[dict(selector= "p", rule= "margin: 0; text-align: left")]
        )
     
     
                                    
    ]
)
