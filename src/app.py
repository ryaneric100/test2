import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY])  # COSMO  suppress_callback_exceptions=True
server = app.server

sidebar = dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
            className="bg-light"
           
)

# print(dash.page_registry.values())


app.layout = dbc.Container([

    # html.Hr(),
    
    # dbc.Row([
    #     dbc.Col(
    #     [
    #         html.Img(src='assets/logo.png')
    #     ], width=1
    #     ),
    #     dbc.Col(html.Div("Dufour Cockpit",
    #                       style={'fontSize':25, 'textAlign':'left'})),

    # ]),
   

    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                    html.Hr(),
                    html.Img(src='assets/logo.png'),
                    html.Hr(),
                    sidebar
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col(
                [
                    dash.page_container
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ]
    )
], fluid=True)


if __name__ == "__main__":
    app.run(debug=True)
