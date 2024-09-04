import numpy as np
import scipy.io.wavfile as wavfile
from sklearn.decomposition import FastICA
from scipy.signal import butter, lfilter, find_peaks
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from pydub import AudioSegment
from pydub.playback import play

# Función para aplicar filtro de paso banda
def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    y = lfilter(b, a, data)
    return y

# Función para calcular la transformada de Fourier y obtener el espectro
def calcular_espectro(audio, fs):
    fft_audio = np.fft.fft(audio)
    freqs = np.fft.fftfreq(len(audio), 1.0 / fs)
    return fft_audio, freqs

# Función para calcular SNR
def calcular_snr(signal, noise):
    signal_power = np.mean(signal ** 2)
    noise_power = np.mean(noise ** 2)
    snr = 10 * np.log10(signal_power / noise_power)
    return snr

# Función para calcular dB
def calcular_db(signal):
    power = np.mean(signal ** 2)
    db = 10 * np.log10(power)
    return db

# Función para identificar y extraer la voz principal
def extraer_voz_principal(audio, freqs, fft_audio):
    magnitudes = np.abs(fft_audio)
    peaks, _ = find_peaks(magnitudes, height=np.max(magnitudes) * 0.1)
    lowcut = 300
    highcut = 3400
    voice_mask = (freqs > lowcut) & (freqs < highcut)
    filtered_fft_audio = fft_audio * voice_mask
    audio_filtrado = np.fft.ifft(filtered_fft_audio).real
    return audio_filtrado

# Cargar las señales de los tres micrófonos
fs1, audio1 = wavfile.read('20240827_193351.wav')
fs2, audio2 = wavfile.read('20240827_193352.wav')
fs3, audio3 = wavfile.read('20240827_193353.wav')

# Normalizar las señales
audio1 = audio1.astype(np.float32) / np.max(np.abs(audio1))
audio2 = audio2.astype(np.float32) / np.max(np.abs(audio2))
audio3 = audio3.astype(np.float32) / np.max(np.abs(audio3))

# Encontrar la longitud mínima entre las señales
min_length = min(len(audio1), len(audio2), len(audio3))

# Recortar las señales a la longitud mínima
audio1 = audio1[:min_length]
audio2 = audio2[:min_length]
audio3 = audio3[:min_length]

# Crear una matriz con las señales
signals = np.c_[audio1, audio2, audio3]

# Aplicar ICA para separar las fuentes
ica = FastICA(n_components=3, random_state=42)
sources = ica.fit_transform(signals)  # Aquí se obtienen las señales separadas

# Guardar las señales separadas
write('fuente1_separada.wav', fs1, (sources[:, 0] * 32767).astype(np.int16))
write('fuente2_separada.wav', fs1, (sources[:, 1] * 32767).astype(np.int16))
write('fuente3_separada.wav', fs1, (sources[:, 2] * 32767).astype(np.int16))

# Cargar y normalizar la señal de ruido
fs_noise, noise = wavfile.read('20240828_222252.wav')
noise = noise.astype(np.float32) / np.max(np.abs(noise))

# Calcular el espectro del ruido
fft_noise, freqs_noise = calcular_espectro(noise, fs_noise)

# Calcular el SNR antes del filtrado para todas las señales
snr_audio1_before = calcular_snr(audio1, noise)
snr_audio2_before = calcular_snr(audio2, noise)
snr_audio3_before = calcular_snr(audio3, noise)

# Extraer y filtrar la voz principal de la Persona 2
fft_audio2, freqs2 = calcular_espectro(audio2, fs2)
audio2_filtrado = butter_bandpass_filter(audio2, 300, 3400, fs2, order=6)
audio2_filtrado = butter_bandpass_filter(audio2_filtrado, 300, 3400, fs2, order=6)  # Aplicar el filtro dos veces

# Normalizar la señal filtrada final
audio2_filtrado = audio2_filtrado / np.max(np.abs(audio2_filtrado))

# Guardar la señal filtrada final
write('audio2_filtrado_final.wav', fs2, (audio2_filtrado * 32767).astype(np.int16))

# Calcular el SNR después del filtrado para todas las señales
snr_audio1_after = calcular_snr(sources[:, 0], noise)
snr_audio2_after = calcular_snr(audio2_filtrado, noise)
snr_audio3_after = calcular_snr(sources[:, 2], noise)

print(f'SNR antes del filtrado para señal 1: {snr_audio1_before:.2f} dB')
print(f'SNR después del filtrado para señal 1: {snr_audio1_after:.2f} dB')

print(f'SNR antes del filtrado para señal 2: {snr_audio2_before:.2f} dB')
print(f'SNR después del filtrado para señal 2: {snr_audio2_after:.2f} dB')

print(f'SNR antes del filtrado para señal 3: {snr_audio3_before:.2f} dB')
print(f'SNR después del filtrado para señal 3: {snr_audio3_after:.2f} dB')

# Calcular los dB antes y después del filtrado para todas las señales
db_audio1 = calcular_db(audio1)
db_audio2 = calcular_db(audio2)
db_audio3 = calcular_db(audio3)
db_audio2_filtrado = calcular_db(audio2_filtrado)
db_noise = calcular_db(noise)

print(f'dB de la señal 1: {db_audio1:.2f} dB')
print(f'dB de la señal 2: {db_audio2:.2f} dB')
print(f'dB de la señal 3: {db_audio3:.2f} dB')
print(f'dB de la señal 2 filtrada: {db_audio2_filtrado:.2f} dB')
print(f'dB del ruido: {db_noise:.2f} dB')

# Calcular el SNR del ruido
snr_ruido = calcular_snr(noise, noise)  # Comparando el ruido consigo mismo

print(f'SNR del ruido: {snr_ruido:.2f} dB')

# Graficar la señal de ruido y su espectro
plt.figure(figsize=(12, 6))
plt.plot(noise, color='gray')
plt.title('Señal de Ruido', fontsize=14, color='darkorange')
plt.xlabel('Muestras', fontsize=12, color='darkgreen')
plt.ylabel('Amplitud', fontsize=12, color='darkgreen')
plt.grid(True, linestyle='--', color='gray')
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(freqs_noise[:len(freqs_noise)//2], np.abs(fft_noise[:len(fft_noise)//2]), color='red')
plt.title('Espectro de Frecuencias del Ruido', fontsize=14, color='darkorange')
plt.xlabel('Frecuencia (Hz)', fontsize=12, color='darkgreen')
plt.ylabel('Magnitud', fontsize=12, color='darkgreen')
plt.grid(True, linestyle='--', color='gray')
plt.show()

# Graficar las señales separadas juntas
plt.figure(figsize=(12, 6))
plt.plot(sources[:, 0], label='Fuente 1', color='red')
plt.plot(sources[:, 1], label='Fuente 2', color='green')
plt.plot(sources[:, 2], label='Fuente 3', color='blue')
plt.title('Señales de las Fuentes 1, 2 y 3', fontsize=14, color='darkorange')
plt.xlabel('Muestras', fontsize=12, color='darkgreen')
plt.ylabel('Amplitud', fontsize=12, color='darkgreen')
plt.legend()
plt.grid(True, linestyle='--', color='gray')
plt.show()

# Graficar el espectro de las señales separadas juntas
plt.figure(figsize=(12, 8))

fft_source1, freqs_source1 = calcular_espectro(sources[:, 0], fs1)
fft_source2, freqs_source2 = calcular_espectro(sources[:, 1], fs2)
fft_source3, freqs_source3 = calcular_espectro(sources[:, 2], fs3)

plt.subplot(3, 1, 1)
plt.plot(freqs_source1[:len(freqs_source1)//2], np.abs(fft_source1[:len(fft_source1)//2]), color='red')
plt.title('Espectro de Frecuencias de la Fuente 1 Separada', fontsize=14, color='darkorange')
plt.xlabel('Frecuencia (Hz)', fontsize=12, color='darkgreen')
plt.ylabel('Magnitud', fontsize=12, color='darkgreen')
plt.grid(True, linestyle='--', color='gray')

plt.subplot(3, 1, 2)
plt.plot(freqs_source2[:len(freqs_source2)//2], np.abs(fft_source2[:len(fft_source2)//2]), color='green')
plt.title('Espectro de Frecuencias de la Fuente 2 Separada', fontsize=14, color='darkorange')
plt.xlabel('Frecuencia (Hz)', fontsize=12, color='darkgreen')
plt.ylabel('Magnitud', fontsize=12, color='darkgreen')
plt.grid(True, linestyle='--', color='gray')

plt.subplot(3, 1, 3)
plt.plot(freqs_source3[:len(freqs_source3)//2], np.abs(fft_source3[:len(fft_source3)//2]), color='blue')
plt.title('Espectro de Frecuencias de la Fuente 3 Separada', fontsize=14, color='darkorange')
plt.xlabel('Frecuencia (Hz)', fontsize=12, color='darkgreen')
plt.ylabel('Magnitud', fontsize=12, color='darkgreen')
plt.grid(True, linestyle='--', color='gray')

plt.tight_layout()
plt.show()

# Graficar las señales separadas individualmente
for i in range(3):
    plt.figure(figsize=(12, 6))
    plt.plot(sources[:, i], color=['red', 'green', 'blue'][i])
    plt.title(f'Señal Separada {i+1}', fontsize=14, color='darkorange')
    plt.xlabel('Muestras', fontsize=12, color='darkgreen')
    plt.ylabel('Amplitud', fontsize=12, color='darkgreen')
    plt.grid(True, linestyle='--', color='gray')
    plt.show()

# Graficar la señal 2 después del filtrado
plt.figure(figsize=(12, 6))
plt.plot(audio2_filtrado, color='green')
plt.title('Señal 2 Filtrada', fontsize=14, color='darkorange')
plt.xlabel('Muestras', fontsize=12, color='darkgreen')
plt.ylabel('Amplitud', fontsize=12, color='darkgreen')
plt.grid(True, linestyle='--', color='gray')
plt.show()

# Graficar el espectro de la señal 2 filtrada
fft_audio2_filtrado, freqs_audio2_filtrado = calcular_espectro(audio2_filtrado, fs2)
plt.figure(figsize=(12, 6))
plt.plot(freqs_audio2_filtrado[:len(freqs_audio2_filtrado)//2], np.abs(fft_audio2_filtrado[:len(fft_audio2_filtrado)//2]), color='green')
plt.title('Espectro de Frecuencias de la Señal 2 Filtrada', fontsize=14, color='darkorange')
plt.xlabel('Frecuencia (Hz)', fontsize=12, color='darkgreen')
plt.ylabel('Magnitud', fontsize=12, color='darkgreen')
plt.grid(True, linestyle='--', color='gray')
plt.show()

# Reproducir el archivo de audio filtrado
song = AudioSegment.from_wav('audio2_filtrado_final.wav')
play(song)
