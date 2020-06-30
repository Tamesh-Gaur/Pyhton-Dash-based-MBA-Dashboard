#########################################################################
############################# LIBRARY ###################################
#########################################################################

import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import json
import pandas as pd
import numpy as np
import random
import seaborn as sns 
import matplotlib.pyplot as plt 
import pandas as pd
import requests 
import time
import pandas as pd
import base64
import io
import dash_table
from collections import Counter
import plotly.graph_objects as go
from mlxtend.frequent_patterns import association_rules
from mlxtend.frequent_patterns import apriori
from plotly.offline import plot


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#########################################################################
############################# Options for connection ####################
#########################################################################
df1=['Select CSV file','Connect with Database '];
range_=len(df1)

#########################################################################
############################# DASH APP BEGIN ############################
#########################################################################
app = dash.Dash()
        
body = {
'background-color':'#F29C6B',
},
        





app.layout = html.Div(
        children=[
################################################ HEADER

            html.Div(
              className = "app_header",
              children = [
                html.Div('Market Basket Analysis', className = "app-header--title")
              ],style={'padding': '60px', 'text-align': 'center','font-size': '30px', 'color': 'black'}
            ),
            
        html.Div(
        className='grid_container',
        children=[
                

            
################################################# dropdown for connection        
       html.Div(
       className='sm-box sm-box--1',
               
       children=[
       dcc.Dropdown(
       id='dropdown',
       
        options=[{'label': df1[i] , 'value': i} for i in range(range_)],
        value='a'
    ),
#        html.Div(id='dd-output-container'),
#        html.Div(id="table1"),
         ############################################################ for database connction
        html.Div(
                id="db-input",
                children=[
                html.I("Enter DataBase Details"),
                html.Br(),
                dcc.Input(id="input1",className="in1", type="text", placeholder="db name"),
                dcc.Input(id="input2",className="in1", type="text", placeholder="user name ", debounce=True),
                dcc.Input(id="input3",className="in1", type="text", placeholder="ip"),
                dcc.Input(id="input4",className="in1", type="text", placeholder="password ", debounce=True),
                dcc.Input(id="input5",className="in1", type="text", placeholder="table name ", debounce=True),
                html.Div(id="output"),
            ]
            
        ),
        ################################################# for csv input (DB/CSV)
        html.Div(
                id="csv-input",
                children=[
                html.Div([
                dcc.Upload(
                id='datatable-upload',
                children=html.Div([
                        'Drag and Drop or ',
                         html.A('Select Files')
                 ]),
                 style={
                        'width': '200px', 'height': '130px', 'lineHeight': '60px',
                        'borderWidth': '1px', 'borderStyle': 'dashed',
                        'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px',
                        'font-size':'120%',
                       },
                ),

            ])     
        ]
            
        ),


        ],style={'width': '20%', 'display': 'inline-block','vertical-align':'top',
                 
               }
        ),
################################################# Catagory BAR garpah (categoryBar)       
        html.Div(id='categoryBar',
        className='sm-box sm-box--2',
        children=[
                 dcc.Graph(id='datatable-upload-graph21',
                 figure={
                         'data': [
                                 {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
                                 {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'line', 'name': u'Montréal'},
                                 ],
                         'layout': {
                                    'title': 'List of all categories',
                                    'plot_bgcolor':'rgba(0,0,0,0)',
                                    'paper_bgcolor':'rgba(0,0,0,0)',
                                    }
                        }
                               
                )],style={'width': '38%', 'display': 'inline-block',
                           'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                           'margin': '10px'
#                           '-moz-box-shadow':    'inset 0 0 10px #000000',
#                            '-webkit-box-shadow': 'inset 0 0 10px #000000',
#                            'box-shadow':         'inset 0 0 10px #000000',
                
                
                }),
################################################# Catagory Pie garpah (pi category)       
         html.Div(id='categoryPi',
         className='sm-box sm-box--3',
         children=[
                  dcc.Graph(id='catPi',
                  figure={
                          'data': [
                                   {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
                                   {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'line', 'name': u'Montréal'},
                                   ],
                                'layout': {
                                            'title': 'categories distribution over total transaction (%)',
                                            'plot_bgcolor':'rgba(0,0,0,0)',
                                            'paper_bgcolor':'rgba(0,0,0,0)',
                                            }
                            }          
                            )
                  ],style={'width': '38%', 'display': 'inline-block','margin': '10px',
                'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)'}),
        
    
 

##################### FOR TABLE ##########################################
        html.Div(
                id="tableMain",
                children=[
                html.Div('Uploded Data',className = 'dataHeader'),
################# FOR STYLING tabe data
                dash_table.DataTable(
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto'
                            },
                style_table={'overflowX': 'scroll',
                             'maxHeight': '300px',
                             'overflowY': 'scroll'},         ################ for scrolling
                style_cell={'textAlign': 'left',
                            'minWidth': '0px', 'maxWidth': '180px',},
                style_header={                               ###########FOR HEADER
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'
                              },
################# OF DIFFE COLOR IN ROWS
                style_cell_conditional=[
                    {
                        'if': {'column_id': c},
                        'textAlign': 'left'
                    } for c in ['Date', 'Region']
                ],
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ],
                id='datatable-upload-container',
                
                editable=True,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                column_selectable="single",
                selected_columns=[],
            
                ),
            ],style={'width': '30%', 'display': 'inline-block','vertical-align':'top',
                    'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                    'margin':'10px','margin-top': '100px', 'height' : '530px'
            
            }
            
        ),
################################################# subcat histo garpah (sub cat histo)       

         html.Div(id='sub_cat_histo',
         children=[
                  dcc.Graph(id='datatable-upload-graph',
                  figure={
                          'data': [
                                   {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
                                   {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'line', 'name': u'Montréal'},
                                   ],
                                'layout': {
                                            'title': 'selected category to see sub categories ',
                                            'plot_bgcolor':'rgba(0,0,0,0)',
                                            'paper_bgcolor':'rgba(0,0,0,0)',
                                            }
                            }
                            )],style={'width': '65%', 'display': 'inline-block',
                                        'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                        'margin':'10px','margin-top': '100px',
                                        }
                
                ),
################################################# sub category bar graph filter
         html.Div(
         children=[
                 html.Div('Filter categories',className = 'dataHeader'),
                 dcc.Dropdown(id='dd',style={'vertical-align':'top'}),
                  ],style={'width': '31%', 'display': 'inline-block','vertical-align':'top'}
                 ),
         
################################################# sub category bar graph
         html.Div(id='subcat',
         children=[
                  dcc.Graph(id='datatable-upload-graph3',
                  figure={
                          'data': [
                                  {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
                                  {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'line', 'name': u'Montréal'},
                                   ],
                         'layout': {
                                    'title': 'sub category',
                                    'plot_bgcolor':'rgba(0,0,0,0)',
                                    'paper_bgcolor':'rgba(0,0,0,0)',
                                    }
                        }
                           
                           
                           )],style={'width': '67%', 'display': 'inline-block',
                                    'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                    'margin':'10px','margin-top': '50px'
                 }),
 



                

                
################################################# submt button for Heatmap

         html.Div(
         id="csvinput1",
         children=[
                  html.I("csv file deatis"),
                  html.Br(),
                  html.Button('Submit', id='button1'),
#                  html.Div(id="output9"),
                  html.Div(
                  className = "test1111",
                  children = [
                    html.Div( id="output9")
                  ],style={'padding': '60px', 'font-size': '18px', 'color': 'black'}
                ),
                  ################################################# market basket heatmap graph

                    dcc.Graph(id='my-graph1',
                    figure={
                                      'data': [
                                              {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
                                              {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'line', 'name': u'Montréal'},
                                               ],
                                     'layout': {
                                                'title': 'Market Basket Analysis',
                                                'plot_bgcolor':'rgba(0,0,0,0)',
                                                'paper_bgcolor':'rgba(0,0,0,0)',
                                                }
                                    }),   
                ],style={'width': '99%',
                        'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                        'margin':'10px','margin-top': '50px'
                
                
                }
                
                ),
         



                
                
                
                ]
                
                
                
                
                ),



                ]
)
        
        
        
        
        
        
#########################################################################
############## FOR file UPLOD AND TABLE #################################
#########################################################################
                
################################################# for csv input (DB/CSV)   
##################### FOR TABLE ##########################################
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        return pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))
    elif 'xls' in filename:
        # Assume that the user uploaded an excel file
        return pd.read_excel(io.BytesIO(decoded))


@app.callback([Output('datatable-upload-container', 'data'),
               Output('datatable-upload-container', 'columns')],
              [Input('datatable-upload', 'contents')],
              [State('datatable-upload', 'filename')])
def update_output(contents, filename):
    if contents is None:
        return [{}], []
    df = parse_contents(contents, filename)
    return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]





################################################# subcat histo garpah (sub cat histo)       
@app.callback(Output('datatable-upload-graph', 'figure'),
              [Input('datatable-upload-container', 'data')])
def display_graph(rows):
    df = pd.DataFrame(rows)
    df1=pd.DataFrame([Counter(df.iloc[:,1])])

    if (df.empty or len(df.columns) < 1):
        return {
            'data': [{
                'x': [],
                'y': [],
                'type': 'bar'
            }],
            'layout': {
                    'title': 'List of all subcategories ',
                    'plot_bgcolor':'rgba(0,0,0,0)',
                    'paper_bgcolor':'rgba(0,0,0,0)',
                }
        }
    return {
        'data': [{
            'x': df1.columns,
            'y': [df1.iloc[0,i] for i in range(df1.shape[1]-1)],
            'type': 'bar'
        }],
        'layout': {
                    'title': 'List of all subcategories ',
                    'plot_bgcolor':'rgba(0,0,0,0)',
                    'paper_bgcolor':'rgba(0,0,0,0)',
                  }
    }
        
################################################# Catagory BAR garpah (categoryBar)       
@app.callback([Output('datatable-upload-graph21', 'figure'),
               Output('datatable-upload-graph21', 'data')],
              [Input('datatable-upload-container', 'data')])
def display_graph(rows):
    df = pd.DataFrame(rows)
    df1=pd.DataFrame([Counter(df.iloc[:,0])])
    

    if (df.empty or len(df.columns) < 1):
        return {    
            'data': [{
                'x': [],
                'y': [],
                'type': 'bar'
            }],
            'layout': {
                    'title': 'List of all categories',
                    'plot_bgcolor':'rgba(0,0,0,0)',
                    'paper_bgcolor':'rgba(0,0,0,0)',
                }
        },df.iloc[:,0].unique()
    return {
        'data': [{
            'x': df1.columns,
            'y': [df1.iloc[0,i] for i in range(df1.shape[1]-1)],
            'type': 'bar'
        }],
        'layout': {
                    'title': 'List of all categories',
                    'plot_bgcolor':'rgba(0,0,0,0)',
                    'paper_bgcolor':'rgba(0,0,0,0)',
                }
    },df.iloc[:,0].unique()
      
################################################# Catagory Pie garpah (pi category)       
@app.callback(
    [Output(component_id='catPi', component_property='figure'),
     Output(component_id='dd', component_property='options'),],
    [Input(component_id='datatable-upload-container', component_property='data')]
)

def display_graph(rows):
    df = pd.DataFrame(rows)
    df1=pd.DataFrame([Counter(df.iloc[:,0])])
    labels = df1.columns
    values = [df1.iloc[0,i] for i in range(df1.shape[1]-1)]

# Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)],
                          layout=go.Layout(
                            title=go.layout.Title(text="categories distribution over total transaction (%)"),
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)'
                        )
                          ) 
    return (fig),[{'label': i, 'value': i} for i in labels]



################################################# sub category bar graph
@app.callback(
    Output("datatable-upload-graph3", "figure"),
    [Input("dd", "value"), Input("datatable-upload-container", "data")],
)
def update_output1(input1, rows):
    df = pd.DataFrame(rows)
    df=df[df['catagory_name']==input1]
    df1=pd.DataFrame([Counter(df.iloc[:,1])])
    labels = df1.columns
    values = [df1.iloc[0,i] for i in range(df1.shape[1]-1)]
    fig = go.Figure(data=[go.Bar(x=values,y=labels,orientation='h')],
                          layout=go.Layout(
                            title=go.layout.Title(text="sub categories for selected category"),
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)'
                        )
                          ) 
    return (fig)



######################################## FOR MArket bakset heatmap
@app.callback([
    dash.dependencies.Output('output9', 'children'),
    dash.dependencies.Output('my-graph1', 'figure'),],
    [dash.dependencies.Input('button1', 'n_clicks')],
    [dash.dependencies.State('datatable-upload-container', 'data')])
def read_csv(n_clicks, value):
    df = pd.DataFrame(value)
    # df.groupby(['catagory_name','sum_bill_no']).unstack().reset_index().fillna(0).set_index('catagory_name')dff
    df['Name'] = df['catagory_name'].str.cat(df['sub_catagory_name'], sep =" ") 
    dff=pd.concat([df['sum_bill_no'] , df['Name'] ], axis=1, sort=False)
    # df1=df.groupby(['sum_bill_no','catagory_name'])
   
    one_val=np.ones(len(dff),dtype = int)
    one_val
    
    dff["attt"] = one_val
    df=dff
    df1=df.groupby(['sum_bill_no','Name'])['attt'].sum().unstack().reset_index().fillna(0).set_index('sum_bill_no')
    # df1.first() 
    
    def en(x):
        if x<=0:
            return 0;
        if x>=1:
            return 1;
    bb=df1.applymap(en)
          
    ff=apriori(bb,min_support=0.015,use_colnames=True)
    rules=association_rules(ff, metric="lift",min_threshold=1)
    # rules.head()
    rules["antecedents"] = rules["antecedents"].apply(lambda x: list(x)[0]).astype("unicode")
    rules["consequents"] = rules["consequents"].apply(lambda x: list(x)[0]).astype("unicode")
    aaaa=rules.nlargest(20, ['lift'])
    
    
    tc1=pd.concat([aaaa['antecedents'] , aaaa['consequents'],aaaa['lift'] ], axis=1, sort=False)
    # flights = sns.load_dataset("flights")
    flights = tc1.pivot("antecedents", "consequents", "lift")
#    flights.to_csv('ttil.csv')
    ifBuy=str(aaaa.iloc[1,1])
    thenBuy=str(aaaa.iloc[1,0])
    Popu1=Counter(dff.Name)
    Popu11 = list(Popu1.keys())[0] 
    

    return u'Total No of Rows in data set is : {}. Products from Categories {} are Popular over all the products  and if {} is bought then definitely {} will be purchesed as this two are having maximunm lift'.format(
        len(df),Popu11,ifBuy,thenBuy
        
    ),{
            'data': [go.Heatmap(
                   x=aaaa['antecedents'],
                   y=aaaa['consequents'],
                   z=aaaa['lift'],
             name = 'Market Basket Analysis',
             
             colorscale=[[0, 'navy'], [1, 'plum']],
             reversescale=True
             ),
            
    
                ],
             'layout': go.Layout(
             xaxis = dict(title = 'antecedents'),
             yaxis = dict( title = 'consequents'),
             paper_bgcolor='rgba(0,0,0,0)',
             plot_bgcolor='rgba(0,0,0,0)',
             title='Heat Map for MBA',
             height=600,
             )
            
            
            
            }




     
        
        

################################################# dropdown for connection  
@app.callback(
    dash.dependencies.Output('db-input', 'style'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_output(value):
#    return 'You have selected {}'.format(value)
    if(value==1):
        return {'display':'block'}
    else:
        return {'display':'none'}


####################################################
@app.callback(
    dash.dependencies.Output('csv-input', 'style'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_output2(value):
#    return 'You have selected {}'.format(value)
    if(value==0):
        return {'display':'block'}
    else:
        return {'display':'none'}

##########################################
@app.callback(
    Output("output", "children"),
    [Input("input1", "value"), Input("input2", "value")],
)
def update_output1(input1, input2):
    return u'Input 1 db name {} and Input 2 user name {}'.format(input1, input2)



#
#    




if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    



    
			