#!/usr/bin/env python
# coding: utf-8

import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

import pandas as pd

# read data file
# ------------------------------------------------------------------------------
df = pd.read_csv(
    "Data.csv",
    index_col= "Pokemon Id"
)
# manage data
df = df[df["Alternate Form Name"].isna()]
df["Generation"] = pd.factorize(df["Region of Origin"])[0]+1
df["Base Stat Total User"] = 1*df["Health Stat"] + 1*df["Attack Stat"] + 1*df["Defense Stat"] + 1*df["Special Attack Stat"] + 1*df["Special Defense Stat"] + 1*df["Speed Stat"]

df.drop(['Primary Ability', 'Primary Ability Description', "Secondary Ability",
         "Secondary Ability Description","Hidden Ability","Hidden Ability Description",
         "Special Event Ability","Special Event Ability Description","Male Ratio",
         "Female Ratio","Base Happiness","Original Pokemon ID","Health EV","Attack EV",
         "Defense EV","Special Attack EV","Special Defense EV","Speed EV","EV Yield Total",
         "Catch Rate","Experience Growth","Experience Growth Total","Experience Yield",
         "Primary Egg Group","Secondary Egg Group","Egg Cycle Count",
         "Pre-Evolution Pokemon Id","Evolution Details"], axis='columns', inplace=True)

# Set up app
# ------------------------------------------------------------------------------
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# HTML page Layout
# ------------------------------------------------------------------------------
# Page is divided in three parts:
#    * header: at the top, a title
#    * body: the main containt
#    * footer: at the bottom, contact, informations, credits
app.layout = html.Div(className="", children=[
    # ------ header
    html.Div(
        className="header",
        style={"backgroundColor": "#3c6382"},
        children=[html.H2(
            "DataViz CMI Pokemon",
            style={
                "color": "white",
                "padding": "30px 0 30px 0",
                "textAlign": "center"}
        )],
    ),

    # ----- body
    html.Div(className="body", children=[
        # a sub title
        html.H3("A plot"),
        # first dropdown selector
        html.Label("TOP n"),
        dcc.Slider(
            id="n-slider",
            min = 1,
            max = 20,
            step = 1,
            value = 10,
            marks = {
                i : str(i) for i in range(0,21)
            },
        ),
        html.Hr(),
        html.Label("Primary Type"),
        dcc.Dropdown(
            id = "Primary Type-dropdown",  # identifiant
            value = "Grass",  # default value
            # all values in the menu
            options= [
                {"label": types, "value": types} for types in df["Primary Type"].unique()
            ],
        ),
        html.Hr(),
        html.Label("Legendary Type"),
        dcc.Dropdown(
            id = "Legendary Type-dropdown",  # identifiant
            value = "With",  # default value
            # all values in the menu
            options = [
                {"label": "With", "value": "With"},
                {"label": "Only", "value": "Only"},
                {"label": "Without", "value": "Without"},                
            ],
        ),
        html.Hr(),
        html.Label("Health Stat"),
        dcc.Slider(
            id = "Health-slider",
            min = 0,
            max = 10,
            step = 1,
            value = 1,
            marks = {
                i : str(i) for i in range(0,11)
            }
        ),
        html.Hr(),
        html.Label("Attack Stat"),
        dcc.Slider(
            id = "Attack-slider",
            min = 0,
            max = 10,
            step = 1,
            value = 1,
            marks = {
                i : str(i) for i in range(0,11)
            }
        ),
        html.Hr(),
        html.Label("Defense Stat"),
        dcc.Slider(
            id = "Defense-slider",
            min = 0,
            max = 10,
            step = 1,
            value = 1,
            marks = {
                i : str(i) for i in range(0,11)
            }
        ),
        html.Hr(),
        html.Label("Special Attack Stat"),
        dcc.Slider(
            id = "Special Attack-slider",
            min = 0,
            max = 10,
            step = 1,
            value = 1,
            marks = {
                i : str(i) for i in range(0,11)
            }
        ),
        html.Hr(),
        html.Label("Special Defense Stat"),
        dcc.Slider(
            id = "Special Defense-slider",
            min = 0,
            max = 10,
            step = 1,
            value = 1,
            marks = {
                i : str(i) for i in range(0,11)
            }
        ),
        html.Hr(),
        html.Label("Speed Stat"),
        dcc.Slider(
            id = "Speed-slider",
            min = 0,
            max = 10,
            step = 1,
            value = 1,
            marks = {
                i : str(i) for i in range(0,11)
            }
        ),
        html.Hr(),
        # a place for the plot with an id
        html.Div(
            dcc.Graph(id='graph'),
        ),
        # a line
        html.Hr(),
        dash_table.DataTable(
            id="pivot-table",
        ),
        html.Hr(),
        html.Div(id="table")
    ]),

    # ----- footer
    html.Div(
        className="footer",
        style={"backgroundColor": "#3c6382"},
        children=[html.H2(
            "DataViz CMI Pokemon",
            style={
                "color": "white",
                "padding": "30px 0 30px 0",
                "textAlign": "center"}
        )],
    ),
])

# Callback functions => interactivity
# Each element on the page is identified thanks to its `id`
# ------------------------------------------------------------------------------


@app.callback(
    [Output(component_id = "graph", component_property = "figure"),
     Output(component_id = "table", component_property = "children")
    ],
    [Input(component_id = "n-slider", component_property = "value"),
     Input(component_id = "Primary Type-dropdown", component_property = "value"),
     Input(component_id = "Legendary Type-dropdown", component_property = "value"),
     Input(component_id = "Health-slider", component_property = "value"),
     Input(component_id = "Attack-slider", component_property = "value"),
     Input(component_id = "Defense-slider", component_property = "value"),
     Input(component_id = "Special Attack-slider", component_property = "value"),
     Input(component_id = "Special Defense-slider", component_property = "value"),
     Input(component_id = "Speed-slider", component_property = "value")
     ],
)
def display_graph(n, Primary_Type, Legendary_Type, Health, Attack, Defense, Special_Attack, Special_Defense, Speed):
    """ 
    This function produce the plot.
    The output is the "figure" of the graph
    The inputs, are the values of the two dropdown menus
    """
    df_modified = df
    df_modified["Base Stat Total User"] = Health*df["Health Stat"] + Attack*df["Attack Stat"] + Defense*df["Defense Stat"] + Special_Attack*df["Special Attack Stat"] + Special_Defense*df["Special Defense Stat"] + Speed*df["Speed Stat"]
    df_modified = df_modified[df_modified["Primary Type"]==Primary_Type]
    if Legendary_Type=="Only" :
        df_modified = df_modified[df_modified["Legendary Type"].notna()]
    if Legendary_Type=="Without" :
        df_modified = df_modified[df_modified["Legendary Type"].isna()]
    df_modified = df_modified.sort_values(by = "Base Stat Total User", ascending = False)
    df_modified = df_modified.head(n)
    
    figure = px.histogram(
        data_frame = df_modified,
        x = "Base Stat Total User",
        y = "Pokemon Name",
        template = "plotly_white",
        range_x = [df_modified["Base Stat Total User"].min()-10, df_modified["Base Stat Total User"].max()+10]
    )
    return (figure,
        html.Div([
            dash_table.DataTable(
                id = "table",
                data = df_modified.to_dict("rows"),
                columns=[{"name": col, "id": col} for col in df_modified.columns],
            )
        ])            
    )

@app.callback(
    [Output("pivot-table", "data"),
     Output("pivot-table", "columns")],
    [Input(component_id = "n-slider", component_property = "value"),
     Input(component_id = "Primary Type-dropdown", component_property = "value"),
     Input(component_id = "Legendary Type-dropdown", component_property = "value"),
     Input(component_id = "Health-slider", component_property = "value"),
     Input(component_id = "Attack-slider", component_property = "value"),
     Input(component_id = "Defense-slider", component_property = "value"),
     Input(component_id = "Special Attack-slider", component_property = "value"),
     Input(component_id = "Special Defense-slider", component_property = "value"),
     Input(component_id = "Speed-slider", component_property = "value")
     ],
)
def show_pivot_table(n, Primary_Type, Legendary_Type, Health, Attack, Defense, Special_Attack, Special_Defense, Speed):
    """ This function return a pivot Table """
    
    df_modified = df
    df_modified["Base Stat Total User"] = Health*df["Health Stat"] + Attack*df["Attack Stat"] + Defense*df["Defense Stat"] + Special_Attack*df["Special Attack Stat"] + Special_Defense*df["Special Defense Stat"] + Speed*df["Speed Stat"]
    df_modified = df_modified[df_modified["Primary Type"]==Primary_Type]
    if Legendary_Type=="Only" :
        df_modified = df_modified[df_modified["Legendary Type"].notna()]
    if Legendary_Type=="Without" :
        df_modified = df_modified[df_modified["Legendary Type"].isna()]
    df_modified = df_modified.sort_values(by = "Base Stat Total User", ascending = False)
    df_modified = df_modified.head(n)

    pivot_df = pd.pivot_table(
        data = df_modified,
        columns = "Pokemon Name",
        values = ["Base Stat Total User","Base Stat Total","Health Stat","Attack Stat","Defense Stat","Special Attack Stat","Special Defense Stat","Speed Stat"]
    )
    pivot_df = pivot_df.reset_index()
    #pivot_df = pivot_df.astype({"ht_bins": "str"})
    cols = [{"name": str(col), "id": str(col)} for col in pivot_df.columns]
    data = pivot_df.to_dict("records")

    return data, cols


if __name__ == '__main__' :
    app.run_server(debug=True)