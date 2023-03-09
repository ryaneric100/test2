import dash
from dash import  dcc, html, Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
import dash_ag_grid as dag


dash.register_page(__name__,
                   path='/datatable10',
                   name='Aggrid',
                   title='Ag grid',
                   image='pg3.png',
                   description='Ag grid'
)


# dcc.Location(id="Aggrid")

# html. Meta(httpEquiv="refresh", content="1") 

equities = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "AMZN": "Amazon",
    "GOOGL": "Alphabet",
    "TSLA": "Tesla",
    "BRK-B": "Berkshire Hathaway",
    "UNH": "United Health Group",
    "JNJ": "Johnson & Johnson",
}


def get_stock_data():
    return yf.download(tickers=list(equities.keys()), period="5y", group_by="ticker")


stock_data = get_stock_data()


def last_close(ticker):
    return stock_data[ticker]["Close"].iloc[-1]


data = {
    "ticker": [ticker for ticker in equities],
    "company": [name for name in equities.values()],
    "quantity": [75, 40, 100, 50, 40, 60, 20, 40],
    "price": [last_close(ticker) for ticker in equities],
    "position": ["buy", "sell", "hold", "hold", "hold", "hold", "hold", "hold"],
    "comments": ["Notes" for i in range(8)],
}
df = pd.DataFrame(data)


columnDefs = [
    {
        "headerName": "Stock Ticker",
        "field": "ticker",
    },
    {
        "headerName": "Company",
        "field": "company",
        "unhide": True,
        "type": "rightAligned",
    },
    {
        "headerName": "Shares",
        "field": "quantity",
        "type": "rightAligned",
        "filter": "agNumberColumnFilter",
        "editable": True,
    },
    {
        "headerName": "Last Close Price",
        "field": "price",
        "type": "rightAligned",
        "filter": "agNumberColumnFilter",
        "valueFormatter": "Number(value).toFixed(2)",
        "dangerously_allow_html": True,
        "cellRenderer": "agAnimateShowChangeCellRenderer",
    },
    {
        "headerName": "Market Value",
        "type": "rightAligned",
        "filter": "agNumberColumnFilter",
        "valueGetter": "Number(data.price) * Number(data.quantity)",
        "valueFormatter": "Number(value).toFixed(2)",
        "dangerously_allow_html": True,
        "cellRenderer": "agAnimateShowChangeCellRenderer",
    },
    {
        "headerName": "Position",
        "field": "position",
        "editable": True,
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {
            "values": ["buy", "sell", "hold"],
        },
    },
    {
        "headerName": "Comments",
        "field": "comments",
        "editable": True,
        "cellEditorPopup": True,
        "cellEditor": "agLargeTextCellEditor",
    },
]

defaultColDef = {
    "filter": True,
    "resizable": True,
    "sortable": True,
    "editable": False,
    "floatingFilter": True,
}

cellStyle = {
    "styleConditions": [
        {
            "condition": "value == 'buy'",
            "style": {"backgroundColor": "#196A4E", "color": "white"},
        },
        {
            "condition": "value == 'sell'",
            "style": {"backgroundColor": "#800000", "color": "white"},
        },
        {
            "condition": "colDef.headerName == 'Shares'",
            "style": {"backgroundColor": "#444"},
        },
    ]
}


table = dag.AgGrid(
    id="portfolio-grid",
    className="ag-theme-alpine-dark",
    columnDefs=columnDefs,
    rowData=df.to_dict("records"),
    columnSize="sizeToFit",
    defaultColDef=defaultColDef,
    cellStyle=cellStyle,
    dangerously_allow_html=True,
    dashGridOptions={"undoRedoCellEditing": True, "rowSelection": "single"},
)

candlestick = dbc.Card(dcc.Graph(id="candlestick"), body=True)
pie = dbc.Card(dcc.Graph(id="asset-allocation"), body=True)
header = html.Div("My Portfolio", className="h2 p-2 text-white bg-primary text-center")


# app.layout = dbc.Container(
#     [
#         header,
#         dbc.Row([dbc.Col(candlestick), dbc.Col(pie)]),
#         dbc.Row(dbc.Col(table, className="py-4")),
#     ],
# )







layout = html.Div(
    [
     
       dbc.Row(dbc.Col(table, className="py-4")),
       dbc.Row([dbc.Col(candlestick), dbc.Col(pie)]),
       dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0)
      
     
                                    
    ]
)





@dash.callback(
    Output("candlestick", "figure"),
    Input("portfolio-grid", "selectionChanged"),
)
def update_candlestick(selected_row):
    if selected_row is None:
        ticker = "AAPL"
        company = "Apple"
    else:
        ticker = selected_row[0]["ticker"]
        company = selected_row[0]["company"]

    dff_ticker_hist = stock_data[ticker].reset_index()
    dff_ticker_hist["Date"] = pd.to_datetime(dff_ticker_hist["Date"])

    fig = go.Figure(
        go.Candlestick(
            x=dff_ticker_hist["Date"],
            open=dff_ticker_hist["Open"],
            high=dff_ticker_hist["High"],
            low=dff_ticker_hist["Low"],
            close=dff_ticker_hist["Close"],
        )
    )
    fig.update_layout(
        title_text=f"{ticker} {company} Daily Price", template="plotly_dark"
    )
    return fig


@dash.callback(
    Output("asset-allocation", "figure"),
    Input("portfolio-grid", "cellValueChanged"),
    State("portfolio-grid", "rowData"),
)
def update_portfolio_stats(_, data):
    dff = pd.DataFrame(data)
    dff["total"] = dff["quantity"].astype(float) * dff["price"].astype(float)
    portfolio_total = dff["total"].sum()

    return px.pie(
        dff,
        values="total",
        names="ticker",
        hole=0.3,
        title=f"Portfolio Total ${portfolio_total:,.2f}",
        template="plotly_dark",
    )


