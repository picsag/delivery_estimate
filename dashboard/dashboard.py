import pandas as pd
import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

# Read the food delivery data from the CSV file
data_file = 'data_final.csv'
df = pd.read_csv(data_file)

# Read the MSE data from the CSV files
mse_file_rf = 'mse_scores_randomforest.csv'
mse_file_fused_rf = 'mse_scores_fused_randomforest.csv'
mse_data_rf = pd.read_csv(mse_file_rf)
mse_data_fused_rf = pd.read_csv(mse_file_fused_rf)


def create_bar_chart(dataframe, column, title):
    values = dataframe[column].value_counts()

    fig = go.Figure(data=[go.Bar(x=values.index, y=values.values)])
    fig.update_layout(title=title, xaxis_title=column, yaxis_title='Count')
    return fig


def create_scatter_plot(dataframe, x_column, y_column, title):
    fig = go.Figure(data=go.Scatter(x=dataframe[x_column], y=dataframe[y_column], mode='markers'))
    fig.update_layout(title=title, xaxis_title=x_column, yaxis_title=y_column)
    return fig


def create_pie_chart(dataframe, column, title):
    values = dataframe[column].value_counts()

    fig = go.Figure(data=[go.Pie(labels=values.index, values=values.values)])
    fig.update_layout(title=title)
    return fig


def create_histogram(dataframe, column, title):
    fig = go.Figure(data=[go.Histogram(x=dataframe[column])])
    fig.update_layout(title=title, xaxis_title=column, yaxis_title='Count')
    return fig


def create_mse_grouped_bar_chart(dataframe_rf, dataframe_fused_rf):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=dataframe_rf['account_cluster_id'],
        y=dataframe_rf['mse_score'],
        name='Random Forest',
        marker=dict(color='blue')
    ))

    fig.add_trace(go.Bar(
        x=dataframe_fused_rf['account_cluster_id'],
        y=dataframe_fused_rf['mse_score'],
        name='Augmented Random Forest',
        marker=dict(color='orange')
    ))

    fig.update_layout(title='MSE Scores Comparison by Cluster ID',
                      xaxis_title='Cluster ID',
                      yaxis_title='MSE')

    return fig


# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(children=[
    dbc.Tabs([
        dbc.Tab(label="Data Analysis", children=[
            html.Div(children=[
                html.H1(children='Food Delivery Data Analysis'),

                # Add the bar chart
                html.Div(children=[
                    dcc.Graph(figure=create_bar_chart(df, 'day_of_week', 'Orders by Day of Week'))
                ], className="container mt-4"),

                # Add the scatter plot
                html.Div(children=[
                    dcc.Graph(figure=create_scatter_plot(df, 'estimated_preptime', 'actual_preptime', 'Estimated vs Actual Preparation Time'))
                ], className="container mt-4"),

                # Add the pie chart
                html.Div(children=[
                    dcc.Graph(figure=create_pie_chart(df, 'account_cluster_id', 'Account Cluster Distribution'))
                ], className="container mt-4"),

                # Add the histogram
                html.Div(children=[
                    dcc.Graph(figure=create_histogram(df, 'order_total_items', 'Order Total Items Distribution'))
                ], className="container mt-4")
            ], className="container mt-4")
        ], tab_style={'backgroundColor': '#f8f8f8'}),

        dbc.Tab(label="Predictions", children=[
            # Add the MSE grouped bar chart
            html.Div(children=[
                dcc.Graph(figure=create_mse_grouped_bar_chart(mse_data_rf, mse_data_fused_rf))
            ], className="container mt-4")
        ], tab_style={'backgroundColor': '#f8f8f8'})
    ])
])

server = app.server

if __name__ == '__main__':
    app.run_server(debug=False)
