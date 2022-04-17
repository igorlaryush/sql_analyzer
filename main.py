import os

import dash_cytoscape as cyto

import base64

import dash
from dash.dependencies import Input, Output, State
from dash import html
from sql_analyzer.functions import analyze

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
edges = []

app.layout = html.Div([dash.dcc.Upload(
    id='upload-data',
    children=html.Div([
        'Drag and Drop or ',
        html.A('Select Files')
    ]),
    style={
        'width': '100%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px'
    },
    # Allow multiple files to be uploaded
    multiple=True
),
    html.Div(id='output-data-upload'),
])


def update_graph(dir_name: str) -> html.Div:
    """
    Update html output when sql expressions are loaded.
    :param dir_name: directory with sql files
    :return: graph representation in html
    """
    structure = analyze(dir_name)
    edges = []
    for src, targets in structure.graph.items():
        if len(targets) > 0:
            for target in targets:
                edges.append((target, src))

    nodes = list(set([item for nested in edges for item in nested]))

    directed_edges = [
        {'data': {'id': src + tgt, 'source': src, 'target': tgt}}
        for src, tgt in edges
    ]

    directed_elements = [{'data': {'id': id_}} for id_ in nodes] + directed_edges

    arrow_styles = [{
        'selector': src + tgt,
        'style': {
            'source-arrow-color': 'red',
            'source-arrow-shape': 'vee',
            'line-color': 'red'
        }
    } for src, tgt in edges]

    style = [
        {
            'selector': 'node',
            'style': {
                'label': 'data(id)'
            }
        },
        {
            'selector': 'edge',
            'style': {
                'curve-style': 'bezier'
            }
        }
    ]

    style.extend(arrow_styles)

    return html.Div([
        html.Div(id='output-data-upload'),
        cyto.Cytoscape(
            id='cytoscape-styling-9',
            layout={'name': 'circle'},
            style={'width': '100%', 'height': '1200px'},
            elements=directed_elements,
            stylesheet=style
        )
    ])


@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def read_input(list_of_contents: list, list_of_names: list) -> html.Div:
    """
    Callback to read loaded sql files.
    :param list_of_contents:
    :param list_of_names:
    :return: graph representation in html
    """

    dir_name = 'uploaded_data/'

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    for file in os.listdir(dir_name):
        os.remove(dir_name + file)

    if list_of_contents is not None and list_of_names is not None:
        for contents, filename in zip(list_of_contents, list_of_names):
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            try:
                if 'sql' in filename:
                    # sql_expressions.append(decoded.decode('utf-8'))
                    with open(dir_name + filename, 'w') as f:
                        f.write(decoded.decode('utf-8'))

            except Exception as e:
                print(e)
                return html.Div([
                    'There was an error processing this file {}. Make sure that you uploaded sql file.'.format(filename)
                ])

    children = update_graph(dir_name)
    return children


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=False)
