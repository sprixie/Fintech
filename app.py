import dash
import pandas as pd
from dash import dcc
from dash import html
from dash import dash_table

# Read the CSV file into a DataFrame
df = pd.read_csv('List of MENA fintech companies - Crunchbase pro.csv', delimiter=';')

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    children=[
        html.H1("Fintech Companies In the MENA Region"),
        dcc.Input(
            id='search-input',
            type='text',
            placeholder='Search...',
        ),
        html.Button('Search', id='search-button', n_clicks=0),
        dash_table.DataTable(
            id='datatable',
            data=df.to_dict('records'),
            columns=[{'id': col, 'name': col} for col in df.columns],
            style_table={
                'overflowX': 'auto',
                'width': '100%',
                'minWidth': '100%',
            },
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            style_data_conditional=[
                {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}
            ],
            filter_action='native',
            page_action='none',
            sort_action='native',
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
        ),
    ]
)


@app.callback(
    dash.dependencies.Output('datatable', 'data'),
    [dash.dependencies.Input('search-button', 'n_clicks')],
    [dash.dependencies.State('search-input', 'value')],
    prevent_initial_call=True
)
def update_table(n_clicks, search_value):
    if search_value:
        filtered_data = df[df.apply(lambda row: any([str(search_value).lower() in str(cell).lower() for cell in row]), axis=1)]
        return filtered_data.to_dict('records')
    else:
        return df.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=False)
