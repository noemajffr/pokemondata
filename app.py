#!/usr/bin/env python
# coding: utf-8

#Importation des libraries
import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

#Lecture du fichier
df = pd.read_csv(
    "Data.csv",
    index_col= "Pokemon Id"
)

#Gestion d'un dataframe
#Sélection des formes originales
df = df[df["Alternate Form Name"].isna()]

#Ajout d'une colonne "Generation"
df["Generation"] = pd.factorize(df["Region of Origin"])[0] + 1

#Ajout d'une colonne "Base Stat Total User"
df["Base Stat Total User"] = 1*df["Health Stat"] + 1*df["Attack Stat"] + 1*df["Defense Stat"] + 1*df["Special Attack Stat"] + 1*df["Special Defense Stat"] + 1*df["Speed Stat"]

#Supression de colonnes
df.drop(["Primary Ability", "Primary Ability Description", "Secondary Ability",
         "Secondary Ability Description","Hidden Ability","Hidden Ability Description",
         "Special Event Ability","Special Event Ability Description","Male Ratio",
         "Female Ratio","Base Happiness","Original Pokemon ID","Health EV","Attack EV",
         "Defense EV","Special Attack EV","Special Defense EV","Speed EV","EV Yield Total",
         "Catch Rate","Experience Growth","Experience Growth Total","Experience Yield",
         "Primary Egg Group","Secondary Egg Group","Egg Cycle Count",
         "Pre-Evolution Pokemon Id","Evolution Details"], axis = "columns", inplace = True)

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
        style={"backgroundColor": "#1c8745"},
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
        html.H4("Who is the best ?"),
        html.Hr(),
        html.P("In this application, you will find the best pokemons according to your choices : just select all the data you want to take into acount."),
        html.Hr(),
        
        #Entrée utilisateur de "Number of Pokemon"
        html.Label("Number of Pokemon :"),
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
        html.Br(),
        html.Br(),
        
        #Entrée utilisateur de "Primary Type"
        html.Label("Primary Type :"),
        dcc.Checklist(
            id = "Primary Type-checkbox",
            value = [types for types in pd.Series(df["Primary Type"].unique()).sort_values()],
            options = [
                {"label": types, "value": types} for types in pd.Series(df["Primary Type"].unique()).sort_values()
            ],
            labelStyle = {"display" : "inline-block"},
        ),
        html.Br(),
        
        #Entrée utilisateur de "Legendary"
        html.Label("Legendary :"),
        dcc.Dropdown(
            id = "Legendary Type-dropdown",  # identifiant
            value = "With",  # default value
            # all values in the menu
            options = [
                {"label": "Only", "value": "Only"},
                {"label": "With", "value": "With"},
                {"label": "Without", "value": "Without"},                
            ],
        ),
        html.Br(),
        html.P([
            "The next data will define your fighting style, please adjust the multiplying factor depending on your wishes.",
            html.Br(),
            "Example : You want to choose a assailant : select 1, 2, 1, 2, 1, 1."
        ]),
        html.Div(className="row", children=[
            html.Div(className="four columns", children=[
                html.Div(className="", children=[
                    html.Br(),
                    html.Br(),
                    
                    #Entrée utilisateur de "Health Stat"
                    html.Label("Weight of Health Stat :"),
                    dcc.Slider(
                        id = "Health-slider",
                        min = 0,
                        max = 10,
                        step = 1,
                        value = 1,
                        marks = {
                            i : str(i) for i in range(0,11)
                        },
                    ),
                    html.Br(),
                    
                    #Entrée utilisateur de "Attack Stat"
                    html.Label("Weight of Attack Stat :"),
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
                    html.Br(),
                    
                    #Entrée utilisateur de "Defense Stat"
                    html.Label("Weight of Defense Stat :"),
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
                    html.Br(),
                    
                    #Entrée utilisateur de "Special Attack Stat"
                    html.Label("Weight of Special Attack Stat :"),
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
                    html.Br(),
                    
                    #Entrée utilisateur de "Special Defense Stat"
                    html.Label("Weight of Special Defense Stat :"),
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
                    html.Br(),
                    
                    #Entrée utilisateur de "Speed Stat"
                    html.Label("Weight of Speed Stat :"),
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
                ]),
            ]),
            html.Div(className="eight columns", children=[
                html.Div(className="", children=[
                    
                    #Affichage d'un histograme
                    html.Div(
                        dcc.Graph(id='hist'),
                    ),          
                ]),
            ]),
        ]),
        
        #Affichage d'un pivot_table
        dash_table.DataTable(
            id="pivot-table",
        )
    ]),        

    # ----- footer
    html.Div(
        className="footer",
        style={"backgroundColor": "#1c8745"},
        children=[html.H2(
            "FRINGAN Ludovic - LALLEMENT Mathias - JAFFRÉ Noéma",
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
    [Output(component_id = "hist", component_property = "figure"),
     Output("pivot-table", "data"),
     Output("pivot-table", "columns")],
    [Input(component_id = "n-slider", component_property = "value"),
     Input(component_id = "Primary Type-checkbox", component_property = "value"),
     Input(component_id = "Legendary Type-dropdown", component_property = "value"),
     Input(component_id = "Health-slider", component_property = "value"),
     Input(component_id = "Attack-slider", component_property = "value"),
     Input(component_id = "Defense-slider", component_property = "value"),
     Input(component_id = "Special Attack-slider", component_property = "value"),
     Input(component_id = "Special Defense-slider", component_property = "value"),
     Input(component_id = "Speed-slider", component_property = "value")
     ],
)
def display_hist(n, Primary_Type, Legendary_Type, Health, Attack, Defense, Special_Attack, Special_Defense, Speed):
    """ 
    Cette fonction produit un histogramme
    Les sorties sont "figure", "data", "cols"
    Les entrées sont des valeurs de sept menus slider, un menu dropdown et un menu checkbox
    """
    
    #Modification du dataframe selon les données utilisateur
    df_modified = df
    df_modified["Base Stat Total User"] = Health*df["Health Stat"] + Attack*df["Attack Stat"] + Defense*df["Defense Stat"] + Special_Attack*df["Special Attack Stat"] + Special_Defense*df["Special Defense Stat"] + Speed*df["Speed Stat"]
    
    #Tri du dataframe selon les données utilisateur
    df_modified = df_modified[df_modified["Primary Type"].isin(Primary_Type)]
    
    #Tri du dataframe selon les données utilisateur
    if Legendary_Type=="Only" :
        df_modified = df_modified[df_modified["Legendary Type"].notna()]
    if Legendary_Type=="Without" :
        df_modified = df_modified[df_modified["Legendary Type"].isna()]
    
    df_modified = df_modified.sort_values(by = "Base Stat Total User", ascending = False)
    df_modified = df_modified.head(n)
    
    #Génération d'un histogramme
    figure = px.histogram(
        data_frame = df_modified,
        x = "Base Stat Total User",
        y = "Pokemon Name",
        color = "Primary Type",        
        title = f"YOUR {n} BEST POKEMON(S)",
        template = "plotly_white",
        range_x = [df_modified["Base Stat Total User"].min()-10, df_modified["Base Stat Total User"].max()+10]
        
    )
    figure.update_layout(xaxis_title = "Base Stat Total User", yaxis_title = "Pokemon Name"),
    figure.update_layout(yaxis_categoryorder = "max ascending")
    
    #Génération d'un pivot_table
    pivot_df = pd.pivot_table(
        data = df_modified,
        columns = "Pokemon Name",
        values = ["Base Stat Total User","Base Stat Total","Health Stat","Attack Stat","Defense Stat","Special Attack Stat","Special Defense Stat","Speed Stat"]
    )
    pivot_df = pivot_df.reset_index()
    cols = [{"name": str(col), "id": str(col)} for col in pivot_df.columns]
    data = pivot_df.to_dict("records")
    
    return (figure, data, cols)

if __name__ == '__main__' :
    app.run_server(debug=True)