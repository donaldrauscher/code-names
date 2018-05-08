import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from gensim.models import KeyedVectors

# initialize app
app = dash.Dash()
server = app.server

# load model
model = "glove/w2v.glove.6B.50d.txt"
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

# set up app layout
app.layout = html.Div(children=[
    html.H1(children='Code Names Hints'),
    html.Label('Words:'),
    dcc.Input(id='words', value='god zeus', type='text'),
    html.Div(id='hints')
])

# set up app callbacks
@app.callback(
    Output(component_id='hints', component_property='children'),
    [Input(component_id='words', component_property='value')]
)
def update_output_div(input_value):
    words = [w.lower() for w in input_value.split(' ')]
    return generate_hints(words)

# run
if __name__ == '__main__':
    app.run_server(debug=True)