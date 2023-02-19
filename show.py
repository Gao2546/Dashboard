from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas
import numpy
import dash_bootstrap_components as dbc
app = Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])

month = ['march', 'april', 'may', 'june', 'july', 'aug', 'sep', 'oct']
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pandas.read_csv("In_march_to_oct2562.csv", low_memory=False)
df['cost_build'] = df['cost_build'].replace(numpy.nan, 0)
df['typ_name'] = df['typ_name'].replace(numpy.nan, "อื่นๆ")
df['diff_per'] = ((df['contrct_price'] - df['cost_build']) / df['cost_build'])*100 

df_building = df[df['typ_name'] == 'จ้างก่อสร้าง']
typeName = df['typ_name'].unique()
month = df['month'].unique()

result = dict()

for t in typeName:
    r_m = []
    for m in month:
        sumCost = sum(df[(df['typ_name'] == t) & (
            df['month'] == m)]['cost_build'])

        r_m.append(sumCost)
    result[t] = r_m
total_type = pandas.DataFrame(result, index=month)

fig_bar = px.bar(total_type, color_discrete_sequence=['#FF99FF', '#CC99FF', '#9999FF','#6699FF', '#3399FF', '#0099FF'])

# sus_list
sus_list = df[((df['contrct_price'] - df['cost_build']) / df['cost_build']) *100 > 10].sample(10)
sus_print_list = []
for sus_item in sus_list.values:
    sus_print_list.append(html.P(f"proj_id:{sus_item[3]} ชื่อโครงการ:{sus_item[4]} หน่วยงาน:{sus_item[5]} บริษัทผู้ชนะ:{sus_item[11]} ราคากลาง:{sus_item[7]} มูลค่าสัญญา:{12} diff_per: {sus_item[-1]}"))

per = 10 # percent ที่อนุญาติให้เสนอได้ไม่เกิน ราคากลาง
con_high_cost = len(df[((df['contrct_price'] - df['cost_build']) / df['cost_build']) *100 > per]) # ราคาสัญญา สูง ราคากลาง 
con_high_proj = len(df[((df['contrct_price'] - df['proj_mny']) / df['proj_mny']) *100 > per]) # ราคาสัญญา สูงกว่า วงเงินงบประมาณ

fig_bar.update_layout(
    paper_bgcolor="whitesmoke",
    width=800,
    height=400
)

fig_circular = px.pie(
        values=[con_high_cost, con_high_proj],
        names=["ราคาสัญญา สูง ราคากลาง ", "ราคาสัญญา สูงกว่า วงเงินงบประมาณ"],title="Suspicious category ratio",
        color_discrete_sequence=['#AAAAAA', '#DDDDDD']
)
fig_circular.update_layout(
    paper_bgcolor="whitesmoke",
    width=800,
    height=400
)

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
        lon=filtered_df['LATITUDE'],
        lat=filtered_df['LONGTITUDE'],
        text=filtered_df['proj_no'],
        mode='markers',
        marker_color=filtered_df['proj_mny'],
        marker = dict(
        size =5,
        line =dict(width=0.5, color='#FFCCFF'))
    ))

    fig.update_layout(
        title='Government Construction Location 2019',
        geo_scope='asia',title_font_color='black', paper_bgcolor='whitesmoke', width=800, height=400
    )

    return fig


@app.callback(
    Output("pie_chart", "figure"),
    Input("month_year", "value"),
)
def show_data2(month_year='march'):
    print(month)
    filtered_df = df[df["month"] == month_year]
    # print(filtered_df)
    fig = px.pie(
        filtered_df,
        title='Project value in various forms',
        values="proj_mny",
        names="typ_name",
        color_discrete_sequence=['#33CCFF', '#FFCCFF', '#CCCCFF','#99CCFF', '#66CCFF'],
        # color="sub_category",
    )

    fig.update_layout(
        title="Project value in various forms",
        title_font_color='black',
        paper_bgcolor="whitesmoke",
        width=800, 
        height=400
    )
    return fig


@app.callback(
    Output("line_chart", "figure"),
    Input("type_name", "value"),
)
def show_data3(typename):
    print(typename)

    filtered_df = total_type[typename]
    # print(filtered_df)
    fig = px.line(filtered_df, markers=True ,color_discrete_sequence=['#FF33FF', '#CC33FF', '#CC33CC','#9933CC', '#6633CC', '#663399'])

    fig.update_layout(
        title_font_color='black',
        paper_bgcolor="whitesmoke",
        width=800, 
        height=400
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
        ), html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id="pie_chart"),
                    ],
                    className="col-8",
                ),
                html.Div(
                    [
                        dbc.Select(
                            options=[
                                dict(label=m, value=m) for m in df_building["month"].unique()
                            ],
                            id="month_year",
                            value=df_building["month"].min(),
                        ),
                    ],
                    className="col-4",
                ),
            ],
            className="row",
        ), html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id="line_chart"),
                    ],
                    className="col-8",
                ),
                html.Div(
                    [
                        dbc.Select(
                            options=[
                                dict(label=m, value=m) for m in df["typ_name"].unique()
                            ],
                            id="type_name",
                            value=df["typ_name"].unique(),
                        ),
                    ],
                    className="col-4",
                ),
            ],
            className="row",
        ), html.Div(
            children=[
                html.Div(
                    [dcc.Graph(id="example-graph-1", figure=fig_bar)], className="col-6"
                ),
            ],
            className="row",
        ), 
        html.Div(
            children=[
                html.Div(
                    [dcc.Graph(id="pie-graph-1", figure=fig_circular)] , className="col-6"
                )
            ]
        ),
        html.Div(
            children=[
                html.H1(
                    children="Sample Suspicious item",
                    style={
                        "textAlign": "center"
                    },
                ), 
                html.Div(sus_print_list)

            ],
            className="row",
        )



    ],
    className="container-fluid",
)

if __name__ == "__main__":
    app.run_server(debug=True)
