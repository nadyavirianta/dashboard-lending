import matplotlib
import dash_core_components as dcc
import dash_html_components as html
import dash

from dash.dependencies import Input, Output, State
import pandas as pd
from dash.exceptions import PreventUpdate
import plotly.express as px
import numpy as np
import os 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

data = pd.read_csv('data/LuxuryLoanPortfolio.csv')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
port = int(os.environ.get("PORT", 5000))

data['records'] = 1
dur = data['duration years'].unique()
purpose = data['purpose'].unique()
data['year'] = data.funded_date.str.slice(0, 4)
app.layout = html.Div(
[ html.H1("Luxury Loan Portfolio Dashboard"),

html.Div([
html.H3('Avg funded amount per year by purpose'),
    dcc.Checklist(
        id="checklist",
        options=[{"label": x, "value": x} 
                 for x in purpose],
        value=purpose,
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id="line-chart"),
]),

html.Div(
    [ html.H3('Loan balance per purpose by duration years'),
    html.P("Duration years:"),
    dcc.Dropdown(
        id="dropdown",
        options=[{"label": x, "value": x} for x in dur],
        value=dur[0],
        clearable=False,
    ),
    dcc.Graph(id="bar-chart"),
])
,
html.H3('Ratio of variety of category'),
    html.Div([
    html.P("Column:"),
    dcc.Dropdown(
        id='names', 
        value='purpose', 
        options=[{'value': x, 'label': x} 
                 for x in ['purpose', 'TAX CLASS AT PRESENT', 'BUILDING CLASS AT PRESENT']],
        clearable=False
    ),
   html.P("Values:"),
    dcc.Dropdown(
        id='values', 
        value='records', 
        options=[{'value': x, 'label': x} 
                 for x in ['records', 'TOTAL UNITS', 'loan balance']],
        clearable=False
    ),
    dcc.Graph(id="pie-chart")]),
    
    
])

@app.callback(
    Output("pie-chart", "figure"), 
    [Input("names", "value"), 
     Input("values", "value")])
def generate_chart(names, values):
    fig = px.pie(data, values=values, names=names)
    return fig

@app.callback(
    Output("bar-chart", "figure"), 
    [Input("dropdown", "value")])
def update_bar_chart(dur):
    mask = data["duration years"] == dur
    fig = px.bar(data[mask], x="purpose", y="loan balance", 
                 barmode="group")
    return fig
    
@app.callback(
    Output("line-chart", "figure"), 
    [Input("checklist", "value")])
def update_line_chart(purposes):
    
    mask = data.purpose.isin(purposes)
    y = data[mask][['funded_amount', 'year']]
    hh = y.groupby('year').agg({'funded_amount': ['mean']}).reset_index()
    hh.columns = ['year', 'funded_amount']
    fig = px.line(hh, 
        x="year", y="funded_amount")
    return fig
    
		
if __name__ == "__main__":
    app.run(debug=False,host="0.0.0.0",
                   port=port)