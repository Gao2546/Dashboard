from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas
import dash_bootstrap_components as dbc
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

month = ['march','april', 'may', 'june', 'july', 'aug', 'sep', 'oct']
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pandas.read_csv("In_march_to_oct2562.csv", low_memory=False)

df_building = df[df['typ_name'] == 'จ้างก่อสร้าง']

@app.callback(
    Output("Scattergeo", "figure"),
    Input("month", "value"),
    Input("Total", "value"),
)
def show_data(month_year='march', Total='10'):
    print(month_year, Total)
    filtered_df = df_building[df_building["month"] == month_year][:int(Total)]
    # print(filtered_df)
    fig = go.Figure(data=go.Scattergeo(
        lon = filtered_df['LATITUDE'],
        lat = filtered_df['LONGTITUDE'],
        text = filtered_df['proj_no'],
        mode = 'markers',
        marker_color = filtered_df['proj_mny'],
    ))

    fig.update_layout(
        title = 'Government Construction Location 2019',
        geo_scope='asia', width=800, height=400
    )

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
            [
                html.Div(
                    [
                        dcc.Graph(id="Scattergeo"),
                    ],
                    className="col-8",
                ),
                html.Div(
                    [
                        dbc.Select(
                            options=[
                                dict(label=m, value=m) for m in df_building["month"].unique()
                            ],
                            id="month",
                            value=df_building["month"].min(),
                        ),
                        dbc.Select(
                            options=[
                                dict(label=num, value=num)
                                for num in range(10, len(df_building.index), 100)
                            ],
                            id="Total",
                            value=len(df_building.index),
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
