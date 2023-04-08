###############################################################################
# IMPORTS                                                                     #
###############################################################################

# Standard libraries
import os

# Third-party libraries
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import openai
import plotly.graph_objects as go

# User-defined libraries
# (none...)

###############################################################################
# APP                                                                         #
###############################################################################

app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP])

###############################################################################
# LAYOUT                                                                      #
###############################################################################

title = html.H1("OpenAI Image Generator")

prompt = html.Div(
    [
        dbc.Label("prompt"),
        dbc.Textarea(id="prompt")
    ]
)

n = html.Div(
    [
        dbc.Label("n"),
        dbc.Input(type="number", min=0, max=10, step=1, id="n")
    ]
)

size = html.Div(
    [
        dbc.Label("size"),
        dcc.Dropdown(
            [
                "256x256",
                "512x512",
                "1024x1024",
            ],
            id="size"
        )

    ]
)

submit = html.Div(
    [
        html.Br(),
        dbc.Button("Submit", id="submit")
    ]
)

output = html.Div(id="output")

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(title)
            ]
        ),
        dbc.Row(
            [
                dbc.Col(prompt)
            ]
        ),
        dbc.Row(
            [
                dbc.Col(n)
            ]
        ),
        dbc.Row(
            [
                dbc.Col(size)
            ]
        ),
        dbc.Row(
            [
                dbc.Col(submit)
            ]
        ),
        dbc.Row(
            [
                dbc.Col(output)
            ]
        )
    ],
    fluid = False,             # "True" = app expands to 100% screen width
    style = {
        "height": "100vh"
    }
)


###############################################################################
# CALLBACKS                                                                   #
###############################################################################

@app.callback(
    Output("output", "children"),
    Input("submit", "n_clicks"),
    State("prompt", "value"),
    State("n", "value"),
    State("size", "value")

)
def create_images(submit_n_clicks, prompt_value, n_value, size_value)-> html.Div:

    output_children = []

    # Ignore callback if app is loading for the 1st time

    if submit_n_clicks is None:
        return output

    openai.api_key = os.environ["OPENAI_TOKEN"]

    response = openai.Image.create(
        prompt = prompt_value,
        n = n_value,
        size = size_value
    )

    for data in response["data"]:

        url = str(data["url"])
        img = html.Img(src = url)
        output_children.append(img)

    return output_children


###############################################################################
# MAIN                                                                        #
###############################################################################

if __name__ == "__main__":

    app.run_server(debug=True)


