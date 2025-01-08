
# Immersive Audio Processing with Convolution Reverb

## Purpose of the Project

This project helps developers create immersive soundscapes for interactive media, such as video games or virtual reality experiences. By using impulse responses (IRs) from various environments, it transforms ordinary sounds (e.g., footsteps or music) to mimic the acoustics of different spaces. This creates a dynamic, location-based audio experience, enhancing the user’s immersion.

For example, as a player moves through a game world, the audio can evolve from the acoustics of a small room to a vast church and then to a narrow hallway, providing an enriched sense of movement through auditory spaces.

## Key Features

1. **Convolution with Real-World IRs**: 
   - Applies convolution reverb using IRs, creating the effect of sound recorded in specific environments.

2. **Chaining Multiple Environments**: 
   - Allows defining multiple acoustic transitions in a single audio file.

3. **Crossfading**: 
   - Smooth and natural time-based transitions between environments, avoiding abrupt changes.

4. **Normalization and Resampling**: 
   - Ensures consistent volume and quality across IRs with varying sample rates or amplitudes.

## Requirements

- Python version: 3.9 to 3.12
- Required libraries: `numpy`, `soundfile`, `librosa`, `scipy`

Install dependencies using:
```bash
pip install -r requirements.txt
```

## Usage Instructions

1. **Prepare Your Sound File**:
   - Have a `.wav` file (e.g., `beat.wav` or `footsteps.wav`) ready to process.

2. **Set Up Impulse Responses**:
   - Place your chosen IR files (e.g., `ancient_site.wav`, `nashville_church_close.wav`, `tight_space.wav`) in the `impulse_responses` folder.

3. **Edit the Configuration**:
   - Open `processing.py` and set the `dry_sound_file` variable to your input file.
   - Modify the `ir_files` list to define IRs, transition start times, and durations. Example:
     ```python
     dry_sound_file = 'beat.wav'
     ir_files = [
         ('impulse_responses/open_site.wav', 8.0, 8.0),
         ('impulse_responses/nashville_church_close.wav', 16.0, 10.0),
         ('impulse_responses/tight_space.wav', 0.0, 0.0)
     ]
     output_file = 'output.wav'
     ```
     - Adjust the times and durations as needed for your transitions.

4. **Run the Program**:
   ```bash
   python processing.py
   ```
   - The processed audio file (`output.wav` by default) will be generated.

## Sample Outputs

- `transformed_walking.wav`: Demonstrates footsteps transitioning from open air to a resonant interior and then to a tight space.
- `transformed_beat.wav`: Applies similar transitions to an electronic beat, ideal for background tracks in games.

## Ideal Use Cases

This project is perfect for video game developers and creators of interactive experiences who want soundtracks that reflect changing environments dynamically.
