from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import Datas

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

colors = {"background": "#111111", "text": "#7FDBFF"}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
data = Datas.data()
l_data = data.add_all_in_folder("use_data_by_class_T")
print(l_data)
# power = df[df["emission_type"].str.contains("ภาคพลังงาน")]


@app.callback(
    Output("pie-graph", "figure"),
    Input("month", "value"),
    Input("month_p", "value"),
)
def show_data(month, month_p):
    print(month, month_p)
    data_ = data.read_data(data.data["2562"][month][month_p]["clean"])
    print(data)
    # print(filtered_df)
    fig = px.pie(
        data_,
        values="contrct_price",
        names="subdep_class",
        # color="sub_category",
    )
    # fig.update_layout(transition_duration=500)

    return fig


app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Hello Dash",
                    style={
                        "textAlign": "center",
                    },
                )
            ],
            className="row",
        ),
        html.Div(
            children=[
                html.Div(
                    children="Dash: A web application framework for your data.",
                    style={
                        "textAlign": "center",
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
                        # dcc.Dropdown(
                        #     data.data["2562"].keys(),
                        #     id="month",
                        # ),
                        # dcc.Dropdown(
                        #     data.data["2562"]["may"].keys(),
                        #     id="month_p",
                        # ),
                        dbc.Select(
                            options=[
                                dict(label=be, value=be) for be in list(data.data["2562"].keys())
                            ],
                            id="month",
                            value=list(data.data["2562"].keys())[0],
                        ),
                        dbc.Select(
                            options=[
                                dict(label=et, value=et)
                                for et in list(data.data["2562"]["may"].keys())
                            ],
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
