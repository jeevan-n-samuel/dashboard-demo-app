import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from data_services import DBService
import base64
import os
import plotly.graph_objects as go
import pandas as pd
import numpy as np 

playerAttDataFrame = pd.DataFrame()
db = DBService('../data/database.sqlite')

def CreatePlayerProgression(playerName):
    #db = DBService('../data/database.sqlite')
    playerAttrDataFrame = db.get_player_attr_table()
    filteredDataFrame = playerAttrDataFrame[playerAttrDataFrame['player_api_id'] == playerName]
    if (filteredDataFrame.empty):
        return html.Div(children=[
            html.H2("No player selected")
        ])
    
    attrsToConsider = [ 'stamina', 'marking', 'sprint_speed', 'ball_control', 'finishing' ]
    traces = []
    for attr in attrsToConsider:
        traces.append(
            {
                'x' : list(filteredDataFrame['date']),
                'y' : list(filteredDataFrame[attr]),
                'name': attr
            }
        )
    return dcc.Graph(
        figure = {
            'data': traces,
            'layout': {'title': 'Player Progression'}
        }
    )

def CreatePlayerInfoSheet(playerName):
    #db = DBService('../data/database.sqlite')
    playerAttrDataFrame = db.get_player_table()
    filteredDataFrame = playerAttrDataFrame[playerAttrDataFrame['player_api_id'] == playerName]
    if (filteredDataFrame.empty):
        return html.Div(children=[
            html.H2("No player selected")
        ])
    heightStr = "Height - "+str(list(filteredDataFrame['height']))
    weightStr = "Weight - "+str(list(filteredDataFrame['weight']))
    playerInfoList = html.Ul( children=[
                                html.Li(heightStr),
                                html.Li(weightStr)
                                
                            ])
    return playerInfoList

def CreatePlayerRadarPlot(playerName):
    print(playerName)
    #db = DBService('../data/database.sqlite')
    playerAttrDataFrame = db.get_player_attr_table()
    filteredDataFrame = playerAttrDataFrame[playerAttrDataFrame['player_api_id'] == playerName]
    if (filteredDataFrame.empty):
        return html.Div(children=[
            html.H2("No player selected")
        ])

    attrsToConsider = [ 'stamina', 'marking', 'sprint_speed', 'ball_control', 'finishing' ]
    minVals = []
    meanVals = []
    maxVals = []
    for attr in attrsToConsider:
        minVals.append( np.min( list(filteredDataFrame[attr]) ) )
        meanVals.append( np.mean(list(filteredDataFrame[attr])) ) 
        maxVals.append( np.max(list(filteredDataFrame[attr])) )

    radarPlotDataMin = go.Scatterpolar(
        r=minVals,
        theta=attrsToConsider,
        # fill='toself',
        name='min'
    )

    radarPlotDataMean = go.Scatterpolar(
        r=meanVals,
        theta=attrsToConsider,
        # fill='toself',
        name='mean'
    )

    radarPlotDataMax = go.Scatterpolar(
        r=maxVals,
        theta=attrsToConsider,
        # fill='toself',
        name='max'
    )

    graph = dcc.Graph(
        figure = {
            'data': [radarPlotDataMin, radarPlotDataMean, radarPlotDataMax],
            'layout': go.Layout(
                    title = 'Player Atrribute Rating'
             )
        }
    )

    return graph


def PlayerPage():
    #db = DBService('../data/database.sqlite')
    playerDataFrame = db.get_player_table()
    print(playerDataFrame)

    playerNames = playerDataFrame['player_name']
    playerOptions = []
    for idx, row in playerDataFrame.iterrows():
        playerOptions.append(
            {
                'label': row['player_name'],
                'value': row['player_api_id']
            }
        )


    filename = os.getcwd()+'/assets/Messi.png'
    print(filename)
    encoded_image = base64.b64encode(open(filename, 'rb').read()) 
    layout = dbc.Container(
        children = [
            html.H1("Search player"),
            dcc.Dropdown(
                id='player-search-dropdown',
                options=playerOptions
            ),
            html.H1(children="Player Statistics"),
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            html.Img(src="data:image/png;base64,{}".format(encoded_image.decode()), style={'height':'100%', 'width':'20%'})
                        ]
                    ),
                    dbc.Col(
                        id="player-stat-list",
                        children=[
                            
                        ]
                    )
                ]
            ),
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            html.Div(id="player-stat-page")
                        ]
                    ),
                    dbc.Col(
                        children=[
                            html.Div(id="player-prog-page")
                        ]
                    )
                ]
            )
        ]
    )


    return layout