import numpy as np
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

data = {
    "Year": [
        1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974,
        1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014,
        2018, 2022
    ],
    "Winner": [
        "Uruguay", "Italy", "Italy", "Uruguay", "West Germany",
        "Brazil", "Brazil", "England", "Brazil", "West Germany",
        "Argentina", "Italy", "Argentina", "West Germany", "Brazil",
        "France", "Brazil", "Italy", "Spain", "Germany",
        "France", "Argentina"
    ],
    "RunnerUp": [
        "Argentina", "Czechoslovakia", "Hungary", "Brazil", "Hungary",
        "Sweden", "Czechoslovakia", "West Germany", "Italy", "Netherlands",
        "Netherlands", "West Germany", "West Germany", "Argentina", "Italy",
        "Brazil", "Germany", "France", "Netherlands", "Argentina",
        "Croatia", "France"
    ]
}

df = pd.DataFrame(data)

df["Winner"] = df["Winner"].replace({"West Germany": "Germany"})
df["RunnerUp"] = df["RunnerUp"].replace({"West Germany": "Germany"})


win_counts = df.groupby("Winner").size().reset_index(name="Wins")


iso_map = {
    "Uruguay": "URY",
    "Italy": "ITA",
    "Germany": "DEU",       
    "Brazil": "BRA",
    "England": "GBR",
    "Argentina": "ARG",
    "France": "FRA",
    "Spain": "ESP",
    "Netherlands": "NLD",
    "Hungary": "HUN",
    "Czechoslovakia": "CSK",  
    "Sweden": "SWE",
    "Croatia": "HRV"
}

win_counts["ISO"] = win_counts["Winner"].map(iso_map)

app = dash.Dash(__name__)
app.title = "FIFA World Cup Dashboard"
server = app.server

app.layout = html.Div([
    html.H1("FIFA World Cup Winners and Runner-Ups Dashboard"),

    dcc.Graph(id='choropleth-map'),
    html.Div([
        html.Label("Select a Winner Country:"),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{"label": c, "value": c} for c in sorted(win_counts["Winner"])],
            value="Brazil" 
        ),
        html.Div(id='win-count-output', style={'marginTop': '1em'})
    ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    html.Div([
        html.Label("Select a World Cup Year:"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{"label": y, "value": y} for y in sorted(df["Year"])],
            value=2022  # default selection
        ),
        html.Div(id='final-output', style={'marginTop': '1em'})
    ], style={'width': '45%', 'display': 'inline-block', 'marginLeft': '5%', 'verticalAlign': 'top'})
])
@app.callback(
    Output('choropleth-map', 'figure'),
    Input('country-dropdown', 'value')
)
def update_choropleth_map(selected_country):
    # Create the choropleth map based on total wins
    fig = px.choropleth(
        win_counts,
        locations="ISO",
        color="Wins",
        hover_name="Winner",
        color_continuous_scale=px.colors.sequential.Plasma,
        title="Total World Cup Wins by Country"
    )
    fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0})
    return fig
@app.callback(
    Output('win-count-output', 'children'),
    Input('country-dropdown', 'value')
)
def display_win_count(selected_country):
    row = win_counts[win_counts["Winner"] == selected_country]
    if row.empty:
        return f"{selected_country} has never won the World Cup."
    else:
        wins = row["Wins"].values[0]
        return f"{selected_country} has won the World Cup {wins} time(s)."

@app.callback(
    Output('final-output', 'children'),
    Input('year-dropdown', 'value')
)
def display_finalists(selected_year):
    row = df[df["Year"] == selected_year].iloc[0]
    winner = row["Winner"]
    runner_up = row["RunnerUp"]
    return f"In {selected_year}, {winner} won the World Cup and {runner_up} was the runner-up."

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
