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

def getPlayerName(playerId):
    playerTable = db.get_player_table()
    playerRow = playerTable[ playerTable['player_api_id'] == playerId]
    print(playerRow)
    return str(playerRow['player_name'].values)

def getValuesForDf(df, attrs, filterBy):
    filterDf = np.mean(df[df['player_api_id'] == filterBy])
    print(filterDf)
    output = list( filterDf.loc[attrs] )
    print(output)
    return output

def CreateCompStatChart(playerIdIn, attributes):
    print('playerIdIn')
    print(playerIdIn)
    print('attributes')
    print(attributes)
    playerAttrDataFrame = []
    filteredDataFrame = []
    attrsToConsider = []
    playerIds = []
    playerAttrDataFrame = db.get_player_attr_table()
    playerIds = playerIdIn
    if playerIds is None:
         return html.Div(children=[
            html.H2("No player selected")
        ])
    filteredDataFrame = playerAttrDataFrame[playerAttrDataFrame['player_api_id'].isin(playerIds)]
    attrsToConsider=attributes
    if attrsToConsider is None:
         return html.Div(children=[
            html.H2("No attributes selected")
        ])
    print('PlayerIds')
    print(playerIds)
    
    
    #attrsToConsider = [ 'stamina', 'marking', 'sprint_speed', 'ball_control', 'finishing' ]
    traces = []
    for playerId in playerIds:
        valuesToUse = getValuesForDf(filteredDataFrame, attrsToConsider, playerId)
        print('values to use')
        print(valuesToUse)
        traces.append(
            {
                'x': attrsToConsider,
                'y': valuesToUse,
                'name': getPlayerName(playerId),
                'type': 'bar'
            }
        )
    
    graph = dcc.Graph(
        figure = {
            'data': traces,
            'layout': {
                'title': 'Mean Attribute Values'
            }
        }
    )
    print("returning graph")
    print(graph)
    return graph
        

def PlayerCompPage():
    playerDataFrame = db.get_player_table()
    print(playerDataFrame)

    playerNames = playerDataFrame['player_name']
    playerOptions = []
    attrOptions = []
    for idx, row in playerDataFrame.iterrows():
        playerOptions.append(
            {
                'label': row['player_name'],
                'value': row['player_api_id']
            }
        )
    numericTypes = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    playerAttrDataFrame = db.get_player_attr_table().select_dtypes(include=numericTypes)
    for colName in playerAttrDataFrame.columns:
        attrOptions.append(
            {
                'label': colName,
                'value': colName
            }
        )


    layout = dbc.Container(
        children=[
            html.H1("Stat comparison"),
            html.P("Select player"),
            dcc.Dropdown(
                id='player-comp-search-dropdown',
                options=playerOptions,
                multi=True
            ),
            html.P("Add attribute"),
            dcc.Dropdown(
                id='player-comp-attr-dropdown',
                options=attrOptions,
                multi=True
            ),
            dbc.Row(
                id="stat-chart"
            )
        ]
    )

    return layout