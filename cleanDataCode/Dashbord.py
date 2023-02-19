from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import Datas

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])



data = Datas.data()
l_data = data.add_all_in_folder("use_data_by_class_T")




@app.callback(
    Output("pie-graph", "figure"),
    Input("month", "value"),
    Input("month_p", "value"),
)
def show_data(month, month_p):
    print(month, month_p)
    data_ = data.read_data(data.data["2562"][month][month_p]["clean"])
    fig = px.pie(
        data_,
        values="contrct_price",
        names="subdep_class",
    )
    fig.update_layout(transition_duration=500,paper_bgcolor='black',height = 500,legend_font_color="white",uniformtext_minsize=12, uniformtext_mode='hide')
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig


app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Public sector procurement report in 2019",
                    style={
                        "textAlign": "center",
                        "text": "#ffffe0",
                        "background":"#A75C1B",
                        "margin-left":" 80px",
                        "margin-top": "10px",
                        "border-radius": "5px",
                        "transition":" 0.3s",
                        "width" : "90vw",
                        "hover" : "white",
                    },
                )
            ],
            className="row",
        ),
        html.Div(
            children=[
                html.Div(
                    children="march - oct 2019",
                    style={
                        "textAlign": "center",
                        "text": "#ffffe0",
                        "background":"#723500",
                        "margin-left":" 45vw",
                        "margin-top": "10px",
                        "margin-bottom":"10px",
                        "border-radius": "5px",
                        "transition":" 0.3s",
                        "width" : "10vw",
                        "hover" : "white",
                    },
                ),
            ],
            className="row",
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id="pie-graph"),
                    ],
                    className="col-8",
                ),
                html.Div(
                    [
                        dbc.Select(
                            options=[
                                dict(label=val, value=val) for val in list(data.data["2562"].keys())
                            ],
                            style={
                                "textAlign": "center",
                                "color": "#454241",
                                "margin-top": "50px",
                                
                            },
                            id="month",
                            value=list(data.data["2562"].keys())[0],
                        ),
                        dbc.Select(
                            options=[
                                dict(label=word, value=val)
                                for word,val in zip(["ครึ่งเดือนแรก","ครึ่งเดือนหลัง"],list(data.data["2562"]["may"].keys()))
                            ],
                            style={
                                "textAlign": "center",
                                "color": "#454241",
                                "margin-top": "10px",
                                
                            },
                            id="month_p",
                            value=list(data.data["2562"]["may"].keys())[0],
                        ),
                    ],
                    className="col-4",
                ),
            ],
            className="row",
        ),
    ],
    className="container-fluid",
)

if __name__ == "__main__":
    app.run_server(debug=True)
