import os
import time
import numpy as np
from sympy import Matrix
from midiutil import MIDIFile

# Hide pygame greeting
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

def run_project():
    # 1. Define Pitch Class representations for chords (C-F-G-C)
    # C Major = [0, 4, 7] | F Major = [5, 9, 0] | G Major = [7, 11, 2]
    c0 = np.array([0, 4, 7])   # I (C Major)
    c1 = np.array([5, 9, 0])   # IV (F Major)
    c2 = np.array([7, 11, 2])  # V (G Major)
    c3 = np.array([0, 4, 7])   # I (C Major)

    A_mat = np.column_stack((c0, c1, c2, c3))
    print("Matrix A (Chord Progressions):")
    print(A_mat)

    # 2. Find the null space using SymPy
    sympy_matrix = Matrix(A_mat)
    null_space_basis = sympy_matrix.nullspace()

    if not null_space_basis:
        print("No null space found for this matrix!")
        return

    # Use the first basis vector found in the null space
    if null_space_basis:
        # null_space_basis[0] grabs the first matrix vector. 
        # [float(x) for x in ...] loops through its rows to get the numbers.
        basis_vector = [float(x) for x in null_space_basis[0]]
    else:
        print("No null space found for this matrix!")
        exit()

    print(f"Using Null Space Basis Vector: {basis_vector}")


    # 3. Transform chords according to the basis vector and apply Modulo 12
    transformed_chords = []
    for idx, weight in enumerate(basis_vector):
        if weight == 0:
            continue  # Omit any zeroed-out chords
        
        original_chord = A_mat[:, idx]
        # Multiply by basis weight and apply modulo 12 arithmetic
        new_chord_pc = (original_chord * weight) % 12
        transformed_chords.append(new_chord_pc.astype(int).tolist())

    print(f"Generated Pitch Class Chords: {transformed_chords}")

    # 4. Generate the MIDI File
    track = 0
    channel = 0
    time_slot = 0     
    duration = 2      # Each chord lasts 2 beats
    volume = 100      
    base_midi = 60    # C4 root level

    midi_file = MIDIFile(1)
    midi_file.addTrackName(track, time_slot, "Null Space Cadence")
    midi_file.addTempo(track, time_slot, 80) # 80 BPM

    for chord_pcs in transformed_chords:
        for pc in chord_pcs:
            midi_note = base_midi + pc
            if pc >= 7: 
                midi_note -= 12 # Smooth out inversion spacing for clean triads
                
            midi_file.addNote(track, channel, midi_note, time_slot, duration, volume)
        time_slot += duration

    output_filename = "null_space_cadence.mid"
    with open(output_filename, "wb") as output_file:
        midi_file.writeFile(output_file)

    print(f"\nSuccessfully generated MIDI file: '{output_filename}'")

    # 5. Playback Engine
    print("▶️ Playing audio out loud inside Python...")
    pygame.mixer.init()

    try:
        pygame.mixer.music.load(output_filename)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
        print("🎵 Playback finished successfully!")
        
    except KeyboardInterrupt:
        print("\n🛑 Playback stopped by user.")
        pygame.mixer.music.stop()

if __name__ == '__main__':
    run_project()
