import numpy as np
import soundfile as sf
import librosa
from scipy.signal import fftconvolve

dry_sound_file = 'beat.wav'  # Dry sound file (e.g., footsteps)

# IR files (impulse responses) with fade settings: (file_path, fade_start_time, fade_duration)
# For each transition:
# - First IR starts immediately at full volume.
# - At (start, start+duration), fade from one IR to the next.
# - The last IR stays active at full volume after fading in.
ir_files = [
    ('impulse_responses/open_site.wav', 8.0, 8.0),   # Transition to env1 at t=8 over 8 seconds
    ('impulse_responses/nashville_church_close.wav', 16.0, 10.0),  # Transition to env2 at t=16 over 10 seconds
    ('impulse_responses/tight_space.wav', 0.0, 0.0)     # Last environment, no transitions
]

output_file = 'output.wav'

# Load Dry Sound
dry_sound, sr = sf.read(dry_sound_file)
if len(dry_sound.shape) > 1:
    dry_sound = np.mean(dry_sound, axis=1)  

# Load IRs and Convolve with Dry Sound
convolved_signals = []
for ir_file, start, duration in ir_files:
    ir, sr_ir = sf.read(ir_file)
    # Resample IR to match dry sound sample rate
    if sr_ir != sr:
        ir = librosa.resample(ir, orig_sr=sr_ir, target_sr=sr)
    if len(ir.shape) > 1:
        ir = np.mean(ir, axis=1)  # Convert to mono if stereo
    
    # Normalize the IR
    if np.max(np.abs(ir)) > 0:
        ir = ir / np.max(np.abs(ir))
    
    # Apply convolution
    convolved_signal = fftconvolve(dry_sound, ir, mode='full')
    convolved_signals.append(convolved_signal)

# Pad Signals to Equal Length
# Ensure all convolved signals are the same length
max_len = max(len(sig) for sig in convolved_signals)
for i in range(len(convolved_signals)):
    if len(convolved_signals[i]) < max_len:
        convolved_signals[i] = np.pad(convolved_signals[i], (0, max_len - len(convolved_signals[i])))


# Crossfade between impulse responses based on start and duration
time = np.linspace(0, max_len / sr, max_len)
N = len(convolved_signals)
fade_curves = np.zeros((N, max_len))

# First IR starts at full volume
fade_curves[0, :] = 1.0

# Define fades for each transition
for i in range(N - 1):
    start = ir_files[i][1]
    duration = ir_files[i][2]
    next_env = i + 1

    for j, t in enumerate(time):
        if t < start:
            pass  # Before transition, current IR stays fully on
        elif t > (start + duration):
            fade_curves[i, j] = 0.0  # After transition, current IR is off
            fade_curves[next_env, j] = 1.0  # Next IR is fully on
        else:
            # During the transition: linear crossfade
            alpha = (t - start) / duration
            fade_curves[i, j] = 1.0 - alpha  # Current IR fades out
            fade_curves[next_env, j] = alpha  # Next IR fades in

    # Ensure IR states remain correct after the transition
    end_time = start + duration
    fade_curves[i, time > end_time] = 0.0
    fade_curves[next_env, (time > end_time) & (fade_curves[next_env, :] == 0.0)] = 1.0


# Blend the Signals
# Combine the convolved signals using the fade curves
blended = np.zeros(max_len)
for i in range(N):
    blended += convolved_signals[i] * fade_curves[i]


# Normalize and Save
max_val = np.max(np.abs(blended))
if max_val > 0:
    blended = blended / max_val * 0.9

sf.write(output_file, blended, sr)
print(f"Output saved to {output_file}")
