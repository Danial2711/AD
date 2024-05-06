import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

def harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    t = np.linspace(0, 1, 500)
    harmonic = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    noise = np.random.normal(noise_mean, noise_covariance, size=len(t))
    if show_noise:
        signal_with_noise = harmonic + noise
    else:
        signal_with_noise = None
    return t, harmonic, signal_with_noise

app = dash.Dash(__name__)

initial_amplitude = 1.0
initial_frequency = 1.0
initial_phase = 0.0
initial_noise_mean = 0.0
initial_noise_covariance = 0.1

app.layout = html.Div([
    html.H1("Harmonic with Noise"),
    dcc.Graph(id='graph'),
    html.Label('Amplitude'),
    dcc.Slider(id='amplitude-slider', min=0, max=2, step=0.1, value=initial_amplitude),
    html.Label('Frequency'),
    dcc.Slider(id='frequency-slider', min=0, max=10, step=0.1, value=initial_frequency),
    html.Label('Phase'),
    dcc.Slider(id='phase-slider', min=0, max=2*np.pi, step=0.1, value=initial_phase),
    html.Label('Noise Mean'),
    dcc.Slider(id='noise-mean-slider', min=-1, max=1, step=0.1, value=initial_noise_mean),
    html.Label('Noise Covariance'),
    dcc.Slider(id='noise-covariance-slider', min=0, max=1, step=0.01, value=initial_noise_covariance),
    html.Label('Show Noise'),
    dcc.Checklist(id='show-noise-checkbox', options=[{'label': 'Show Noise', 'value': True}], value=[True]),
    html.Button('Reset', id='reset-button', n_clicks=0)
])

def custom_filter(signal, window_size):
    filtered_signal = []
    for i in range(len(signal)):
        start = max(0, i - window_size // 2)
        end = min(len(signal), i + window_size // 2 + 1)
        window_sum = sum(signal[start:end])
        window_average = window_sum / (end - start)
        filtered_signal.append(window_average)
    return np.array(filtered_signal)

@app.callback(
    Output('graph', 'figure'),
    [Input('amplitude-slider', 'value'),
     Input('frequency-slider', 'value'),
     Input('phase-slider', 'value'),
     Input('noise-mean-slider', 'value'),
     Input('noise-covariance-slider', 'value'),
     Input('show-noise-checkbox', 'value'),
     Input('reset-button', 'n_clicks')]
)
def update_graph(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise, n_clicks):
    t, harmonic, signal_with_noise = harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise)
    fig = make_subplots(rows=1, cols=1)
    if show_noise:
        fig.add_trace(go.Scatter(x=t, y=signal_with_noise, mode='lines', name='Harmonic with Noise'), row=1, col=1)
    fig.add_trace(go.Scatter(x=t, y=harmonic, mode='lines', name='Pure Harmonic'), row=1, col=1)
    filtered_signal = custom_filter(signal_with_noise, 15)
    fig.add_trace(go.Scatter(x=t, y=filtered_signal, mode='lines', name='Filtered Signal', line=dict(color='yellow')), row=1, col=1)
    fig.update_layout(title="Harmonic with Noise and Pure Harmonic", xaxis_title="Time", yaxis_title="Amplitude")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
