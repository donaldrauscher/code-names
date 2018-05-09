import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

from gensim.models import KeyedVectors

import plotly.figure_factory as ff


# initialize app
app = dash.Dash()
server = app.server

# load model
model = 'glove/w2v.{}.txt'.format(os.getenv('GLOVE_MODEL', 'glove.6B.50d'))
word_vectors = KeyedVectors.load_word2vec_format(model, binary=False)

# precompute L2-normalized vectors (saves lots of memory)
word_vectors.init_sims(replace=True)


# pandas df to html
def generate_table(df, max_rows=10):
    return html.Table(
        # header
        [html.Tr([html.Th(col) for col in df.columns])] +

        # body
        [html.Tr([
            html.Td(df.iloc[i][col]) for col in df.columns
        ]) for i in range(min(len(df), max_rows))]
    )


# generate some clues
def generate_hints(words):
    try:
        hints = word_vectors.most_similar(positive=words)
        hints = pd.DataFrame.from_records(hints, columns=['word','similarity'])
        return generate_table(hints)
    except KeyError as e:
        return html.Div(str(e))


# generate dendrogram for word similarity
def generate_dendro(words):
    try:
        similarities = np.array([word_vectors.distances(w, words) for w in words])
        figure = ff.create_dendrogram(similarities, labels=words)
        figure['layout'].update({'width': 800, 'height': 500})
        return figure
    except KeyError as e:
        pass


# set up app layout
app.layout = html.Div(children=[
    html.H1(children='Code Names Hints'),
    html.Table([
        html.Tr([html.Td("All Words:"), html.Td("Words for Hints:")]),
        html.Tr([html.Td(dcc.Textarea(id='words-all', value='god zeus bat ball mountain cold snow', style={'width': 500})),
                 html.Td(dcc.Input(id='words', value='bat ball', type='text'))]),
        html.Tr([html.Td(dcc.Graph(id='dendro')), html.Td(html.Div(id='hints'))])
    ])
])


# set up app callbacks
@app.callback(
    Output(component_id='dendro', component_property='figure'),
    [Input(component_id='words-all', component_property='value')]
)
def update_dendro(input_value):
    words = [w.lower() for w in input_value.strip().split(' ')]
    return generate_dendro(words)

@app.callback(
    Output(component_id='hints', component_property='children'),
    [Input(component_id='words', component_property='value')]
)
def update_hints(input_value):
    words = [w.lower() for w in input_value.strip().split(' ')]
    return generate_hints(words)


# run
if __name__ == '__main__':
    app.run_server(debug=True)