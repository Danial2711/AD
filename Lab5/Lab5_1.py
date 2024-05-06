import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
import numpy as np
from scipy import signal

def harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    harmonic_signal = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    if show_noise:
        noise = np.random.normal(noise_mean, noise_covariance, size=len(t))
        return harmonic_signal + noise
    else:
        return harmonic_signal

def apply_filter(signal_data, cutoff_freq, filter_type='lowpass', filter_order=4):
    fs = 1 / (t[1] - t[0])
    nyquist = 0.5 * fs
    Wn = cutoff_freq / nyquist
    b, a = signal.butter(filter_order, Wn, btype=filter_type)
    filtered_signal = signal.filtfilt(b, a, signal_data)
    return filtered_signal

initial_amplitude = 1.0
initial_frequency = 1.0
initial_phase = 0.0
initial_noise_mean = 0.0
initial_noise_covariance = 0.1
show_initial_noise = False
initial_cutoff_frequency = 5.0

t = np.linspace(0, 10, 1000)

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.5)

noisy_signal = harmonic_with_noise(t, initial_amplitude, initial_frequency, initial_phase, initial_noise_mean, initial_noise_covariance, show_initial_noise)

line_noisy, = ax.plot(t, noisy_signal, lw=2, color='purple', label='Noisy Signal')

axcolor = 'lightgoldenrodyellow'
ax_amplitude = plt.axes([0.1, 0.4, 0.65, 0.03], facecolor=axcolor)
ax_frequency = plt.axes([0.1, 0.35, 0.65, 0.03], facecolor=axcolor)
ax_phase = plt.axes([0.1, 0.3, 0.65, 0.03], facecolor=axcolor)
ax_noise_mean = plt.axes([0.1, 0.25, 0.65, 0.03], facecolor=axcolor)
ax_noise_covariance = plt.axes([0.1, 0.2, 0.65, 0.03], facecolor=axcolor)
ax_cutoff_freq = plt.axes([0.1, 0.15, 0.65, 0.03], facecolor=axcolor)

s_amplitude = Slider(ax_amplitude, 'Amplitude', 0.1, 10.0, valinit=initial_amplitude)
s_frequency = Slider(ax_frequency, 'Frequency', 0.1, 10.0, valinit=initial_frequency)
s_phase = Slider(ax_phase, 'Phase', 0.0, 2*np.pi, valinit=initial_phase)
s_noise_mean = Slider(ax_noise_mean, 'Noise Mean', -1.0, 1.0, valinit=initial_noise_mean)
s_noise_covariance = Slider(ax_noise_covariance, 'Noise Covariance', 0.01, 1.0, valinit=initial_noise_covariance)
s_cutoff_freq = Slider(ax_cutoff_freq, 'Cutoff Frequency', 0.1, 10.0, valinit=initial_cutoff_frequency)

def update(val):
    amplitude = s_amplitude.val
    frequency = s_frequency.val
    phase = s_phase.val
    noise_mean = s_noise_mean.val
    noise_covariance = s_noise_covariance.val
    cutoff_freq = s_cutoff_freq.val
    
    noisy_signal = harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_initial_noise)
    
    if show_initial_noise:
        filtered_signal = apply_filter(noisy_signal, cutoff_freq)
        line_filtered.set_ydata(filtered_signal)
    else:
        line_filtered.set_ydata(None)
    
    line_noisy.set_ydata(noisy_signal)
    line_original.set_ydata(amplitude * np.sin(2 * np.pi * frequency * t + phase))
    fig.canvas.draw_idle()

s_amplitude.on_changed(update)
s_frequency.on_changed(update)
s_phase.on_changed(update)
s_noise_mean.on_changed(update)
s_noise_covariance.on_changed(update)
s_cutoff_freq.on_changed(update)

rax = plt.axes([0.025, 0.7, 0.15, 0.1], facecolor=axcolor)
check = CheckButtons(rax, ['Show Noise'], [show_initial_noise])

def func(label):
    global show_initial_noise
    show_initial_noise = not show_initial_noise
    update(None)

check.on_clicked(func)

resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button_reset = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

def reset(event):
    s_amplitude.reset()
    s_frequency.reset()
    s_phase.reset()
    s_noise_mean.reset()
    s_noise_covariance.reset()
    s_cutoff_freq.reset()

button_reset.on_clicked(reset)

line_filtered, = ax.plot(t, apply_filter(noisy_signal, initial_cutoff_frequency), lw=2, color='orange', label='Filtered Signal')
line_original, = ax.plot(t, initial_amplitude * np.sin(2 * np.pi * initial_frequency * t + initial_phase), lw=2, color='blue', label='Original Harmonic')

plt.legend()
plt.show()