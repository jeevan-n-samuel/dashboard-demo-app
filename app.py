import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import data_services
from player_details import PlayerPage, CreatePlayerRadarPlot, CreatePlayerInfoSheet, CreatePlayerProgression
from team_details import TeamPage
from player_comparison import PlayerCompPage, CreateCompStatChart
from dash.dependencies import Input, Output

db = data_services.DBService('../data/database.sqlite')
validColumns = db.get_player_attr_table().columns

# print( db.execute_query('SELECT * FROM TEAM') )

playerDf = db.execute_query('SELECT * FROM PLAYER')

# print(playerDf)
x = playerDf['player_name']
y1 = playerDf['height']
y2 = playerDf['weight']

testData = [ 
	{'x': x, 'y': y1, 'type': 'bar', 'name': 'height'},
	{'x': x, 'y': y2, 'type': 'bar', 'name': 'weight'}
]


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout =  html.Div(
    children=[
        dcc.Location(id="url", refresh=False),
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(
                    dbc.NavLink("Player Stats", href="/player_stats")
                ),
                dbc.NavItem(
                    dbc.NavLink("Player Comparison", href="/team_stats")
                )
            ],
            brand="Team Manager Pro",
            sticky="top"
        ),
        html.Div(id="page-content")
    ]
)

# to supress exceptions relating to missing elements in layout
app.config.suppress_callback_exceptions = True

# callback for navigating between pages
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def route_to_page(pathname):
    print("changing page")
    print("pathname is")
    print(pathname)
    if ( pathname == '/player_stats'):
        return PlayerPage()
    else: 
        return PlayerCompPage()

# callback for player page to show stats based on specific player
@app.callback(Output('player-stat-page', 'children'), [Input('player-search-dropdown', 'value')])
def get_player_data(selectedPlayer):
    return CreatePlayerRadarPlot(selectedPlayer)    

# callback for player page to show stats based on specific player
@app.callback(Output('player-prog-page', 'children'), [Input('player-search-dropdown', 'value')])
def get_player_data(selectedPlayer):
    return CreatePlayerProgression(selectedPlayer)

# callback for player page to show stats based on specific player
@app.callback(Output('player-stat-list', 'children'), [Input('player-search-dropdown', 'value')])
def get_player_data(selectedPlayer):
    return CreatePlayerInfoSheet(selectedPlayer)

# callback for player page to show stats based on specific player
@app.callback(Output('stat-chart', 'children'), [Input('player-comp-search-dropdown', 'value'), Input('player-comp-attr-dropdown', 'value')])
def get_player_data(selectedPlayer, attr):
    return CreateCompStatChart(selectedPlayer, attr)

# # callback for player page to show stats based on specific player
# @app.callback(Output('stat-chart', 'children'), [Input('player-comp-attr-dropdown', 'value')])
# def get_player_data(selectedPlayer):
#     return CreateCompStatChart(selectedPlayer, 'X')

if __name__ == '__main__':
    app.run_server(debug=True)
