import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_dangerously_set_inner_html

import plotly.figure_factory as ff
from plotly import tools
import plotly.graph_objs as go

import json
import datetime as dt
import pandas as pd


#Pandas Work
#Overall Topics by Timeframe
senate = pd.read_pickle("nysenate_master_new")
senate_presenting = senate [['date','basePrintNoStr','max_topic','topic_desc','summary','title','year','month','adopted']]
df = pd.DataFrame(senate_presenting.groupby(by=['year','month','topic_desc','adopted'])['max_topic'].count().sort_values(ascending=False)).reset_index()
#Dropdown Options
month_options = sorted(list(set(df["month"])))
year_options = sorted(list(set(df["year"])))

#Top Sponsors by Year in That Topic
sponsors = senate.groupby(by=['sponsor_fullName','sponsor_district','sponsor_chamber','adopted','year','topic_desc'])['basePrintNoStr'].count().reset_index()

#Topic Volume by Year:
monthly_topics = senate.groupby(by=['year','month','topic_desc','adopted'])['basePrintNoStr'].count().reset_index().sort_values(by=['month','year','topic_desc'])
monthly_topics = monthly_topics.rename({"basePrintNoStr":'bills'},axis=1)
def combo_yrmonth(row):
    row['month_year'] = dt.date(year=row['year'],month=row['month'],day=1)
    return row
monthly_topics = monthly_topics.apply(combo_yrmonth,axis=1)

monthly_topics2 = senate.groupby(by=['year','month','topic_desc'])['basePrintNoStr'].count().reset_index().sort_values(by=['month','year','topic_desc'])
monthly_topics2 = monthly_topics2.rename({"basePrintNoStr":'bills'},axis=1)
monthly_topics2 = monthly_topics2.apply(combo_yrmonth,axis=1)
exclude_topics = ['high school athletics honors','honoring firefighters','honoring resolutions','scouts']
monthly_topics2 = monthly_topics2[~monthly_topics2.topic_desc.isin(exclude_topics)]

#Adopted by Topic as Percentage of Bills Adopted in that Month
adopted_pct_by_topic = pd.read_pickle("bill_adopted_by_month")


def serve_layout():
    # return html.H1('The time is: ' + str(datetime.datetime.now()))
    return html.H1('Welcome!') #header at top
def get_month(month_num):
    '''
    Used to change the title of each graph, NYT and Senate, when month is selected in the dropdown at the top
    '''
    month_dict={1: 'Jan',
                 2: 'Feb',
                 3: 'Mar',
                 4: 'Apr',
                 5: 'May',
                 6: 'Jun',
                 7: 'Jul',
                 8: 'Aug',
                 9: 'Sep',
                 10: 'Oct',
                 11: 'Nov',
                 12: 'Dec'}
    return month_dict[month_num] #monthly convertor - number to month name
def generate_table(dataframe, max_rows=5):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )
######END PYTHON############END PYTHON############END PYTHON############END PYTHON############END PYTHON######
#####START DASH#########START DASH#########START DASH#########START DASH#########START DASH#########START DASH####

app = dash.Dash()

app.layout = html.Div([
    #HEADERS
    serve_layout(),

    html.Div([
        html.H2("New York Senate Topic Dashboard")], style={'width': '49%', 'display': 'inline-block', 'padding': '0 0'}),

    html.Div(
        id='output-a', style={'width': '49%', 'display': 'inline-block', 'float': 'right','padding': '0 0'}),

    #DROPDOWNS AND SENATE BAR GRAPH
    html.Div([
        dcc.Dropdown(
                id="month",
                options=[{
                    'label': i,
                    'value': i
                } for i in month_options],
                # multi=True,
                value=6
                ),
        dcc.Dropdown(
                id="year",
                options=[{
                    'label': i,
                    'value': i
                } for i in year_options],
                # multi=True,
                value=2018
                ),

        dcc.Graph(
            id='nysenate-graph'
            ,clickData={'points': [{'y': 'health care'}]}
                ),
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 0'}),

    #START OF ADOPTED/NOT ADOPTED GRAPHS ON RIGHT SIDE
    html.Div([
        #ADOPTED

        html.Div(
            # html.H3("Top Sponsors for Bills Adopted in Topic"),
            serve_layout(),
            id ='top_sponsors_adopted_table'
            ,className="six columns"),

        #NOT ADOPTED
        html.Div(
            # html.H3("Top Sponsors for Bills Not Adopted in Topic"),
            id ='top_sponsors_not_adopted_table'
            ,className="six columns"),

        ]#End of Contents in DIV
        ,style={'display': 'inline-block','float': 'right', 'width': '50%'}
        , className="row"),
    #END OF ADOPTED/NOT ADOPTED GRAPHS ON RIGHT SIDE


    html.Div([
    # html.H3("LINE GRAPH"),
    dcc.Graph(
        id='topic_by_time_pct_adopted')
    ]
    , style={'padding': '100 40'})


    #END LINE GRAPH TOPIC BY MONTH/YEAR
]
# ,style={'backgroundColor':'#11CAEF'}
)
#END OF HTML LAYOUT


#BEGIN UPDATE FUNCTIONS
@app.callback(
    dash.dependencies.Output('nysenate-graph', 'figure'),
    [dash.dependencies.Input('month', 'value'),dash.dependencies.Input('year', 'value')])
def update_senate_graph(month,year):
    df_senate_true = df[(df['month']==month)&(df['year']==year)&(df['adopted']==True)].copy()
    df_senate_false = df[(df['month']==month)&(df['year']==year)&(df['adopted']==False)].copy()

    # trace1 = go.Bar(x=pv.index, y=pv[('Quantity', 'declined')], name='Declined')
    # trace2 = go.Bar(x=pv.index, y=pv[('Quantity', 'pending')], name='Pending')
    trace_not_adopted = go.Bar(
                y=df_senate_false['topic_desc']
                , x=df_senate_false['max_topic']
                , name='Not Adopted'
                ,orientation = 'h'
                )
    trace_adopted = go.Bar(
                y=df_senate_true['topic_desc']
                , x=df_senate_true['max_topic']
                , name='Adopted'
                ,orientation = 'h'
                )

    return {
        'data': [trace_not_adopted,trace_adopted],
        'layout':
        go.Layout(
            title=f"NY State Senate Bills (by Topic) <br> Introduced in {get_month(month)} {year}",
            barmode='stack',
            margin=go.Margin(
        l=195,
        r=30,
        b=20,
        t=50,
        pad=4
        ) ) }

#######
@app.callback(
    dash.dependencies.Output('topic_by_time_pct_adopted', 'figure'),
    [dash.dependencies.Input('nysenate-graph', 'clickData')])
def topics_adopted_pct(clickData):

    orange = 'rgb(235, 139, 27)' #orange
    blue = 'rgb(17, 31, 233)' #blue
    topic = clickData['points'][0]['y']



    monthly_topics2_filtered = monthly_topics2[(monthly_topics2['topic_desc']==topic)].sort_values(by=['month_year'])

    #NOT ADOPTED BILLS FOR TOPIC
    trace_total_bills = go.Scatter(
    x = monthly_topics2_filtered['month_year'],
    y = monthly_topics2_filtered['bills'],
    mode = 'lines',
    name = 'Number of Bills in Topic',
    line = dict(color = (blue),
        width = 4)
        )

    fig = tools.make_subplots(rows=2, cols=1, specs=[[{}], [{}]],
                          shared_xaxes=True, shared_yaxes=False,
                          subplot_titles=(' ', f"Total Number of Bills Proposed in Topic: {topic}"),
                          vertical_spacing=0.1)

    adopted_pct_by_topic_filtered = adopted_pct_by_topic[adopted_pct_by_topic['topic_desc']==topic]

    #ADOPTED BILLS FOR TOPIC AS PCT OF ALL ADOPTED
    trace_adopted_pct_filtered = go.Scatter(
    x = adopted_pct_by_topic_filtered['month_year'],
    y = adopted_pct_by_topic_filtered['adopted_pct'],
    # mode = 'lines',
    name = f"Percentage of Bills Adopted, Adopted Bills in Topic {topic}"
    ,line = dict(color = (orange),width = 2)
                                        )
    fig.append_trace(trace_adopted_pct_filtered, 1, 1)
    fig.append_trace(trace_total_bills, 2, 1)

    fig['layout'].update(
    #     height=600
    # , width=600,
    title = f"Percentage of Bills Adopted, Adopted Bills in Topic: {topic} <br> (All Legislative Honors are filtered out)"
    , margin = {'l': 75, 'b': 30, 'r': 50, 't': 90})

    return fig

#######
@app.callback(
    dash.dependencies.Output('top_sponsors_adopted_table', 'children'),
    [dash.dependencies.Input('nysenate-graph', 'clickData'),dash.dependencies.Input('year', 'value')])
def sponsors_adopted_table(clickData,year):
    topic = clickData['points'][0]['y']
    sponsors_filtered_adopted = sponsors[(sponsors['topic_desc']==topic)&(sponsors['year']==year)&(sponsors['adopted']==True)].sort_values(by=['basePrintNoStr'],ascending=False).head(5)

    sponsors_filtered_adopted.rename({"basePrintNoStr":'bills'},axis=1,inplace=True)
    sponsors_filtered_adopted = sponsors_filtered_adopted[['sponsor_fullName','sponsor_district','sponsor_chamber','bills']]

    sponsors_filtered_adopted.columns = ['Sponsor- Adopted','District','Chamber','Number of Bills']

    return generate_table(sponsors_filtered_adopted)

@app.callback(
    dash.dependencies.Output('top_sponsors_not_adopted_table', 'children'),
    [dash.dependencies.Input('nysenate-graph', 'clickData'),dash.dependencies.Input('year', 'value')])
def sponsors_not_adopted_table(clickData,year):
    topic = clickData['points'][0]['y']
    sponsors_filtered_not_adopted = sponsors[(sponsors['topic_desc']==topic)&(sponsors['year']==year)&(sponsors['adopted']==False)].sort_values(by=['basePrintNoStr'],ascending=False).head(5)

    sponsors_filtered_not_adopted.rename({"basePrintNoStr":'bills'},axis=1,inplace=True)
    sponsors_filtered_not_adopted = sponsors_filtered_not_adopted[['sponsor_fullName','sponsor_district','sponsor_chamber','bills']]

    sponsors_filtered_not_adopted.columns = ['Sponsor- Not Adopted','District','Chamber','Number of Bills']

    return generate_table(sponsors_filtered_not_adopted)

@app.callback(
    dash.dependencies.Output('output-a', 'children'),
    [dash.dependencies.Input('nysenate-graph', 'clickData'),dash.dependencies.Input('year', 'value')])
def topic_clicked(clickData,year):
    topic = clickData['points'][0]['y']
    return html.H2(f"{year} Legislators by Bills Sponsored: {topic}")

#END UPDATE FUNCTIONS

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)
