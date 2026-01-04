"""
Module: 02_fft_analysis.py
Author: Aishvaryalatha R M
Date: Jan 2026

Description: 
    Spectral analysis module for unsteady flow histories (lift/drag/velocity).
    Uses Welch's method (periodogram averaging) to extract Strouhal numbers (St)
    from URANS time-series data. 
    
    Validated against Rossiter modes for open cavity flow.
"""

import numpy as np
import scipy.signal as signal
import sys

# Optional: import matplotlib.pyplot as plt

def compute_strouhal_welch(time_array, q_fluct, L_char, U_inf):
    """
    Computes Power Spectral Density (PSD) to find shedding frequencies.
    
    Args:
        time_array: Physical time steps (s)
        q_fluct:    Fluctuating quantity (e.g., Cl' or v')
        L_char:     Characteristic length (Cavity depth/length)
        U_inf:      Free stream velocity
    """
    
    # 1. sampling check
    dt = time_array[1] - time_array[0]
    fs = 1.0 / dt
    
    # Nyquist limit check (just to be safe)
    if fs < 100: 
        print(f"[Warning] Sampling frequency is low ({fs:.1f} Hz). High modes might be aliased.")

    print(f" -> Processing signal: {len(q_fluct)} samples | fs={fs:.1f} Hz")

    # 2. Detrending (removing mean base flow component)
    q_prime = signal.detrend(q_fluct)

    # 3. Welch's Method
    # Using Hanning window with 50% overlap to smooth out noise
    freqs, psd = signal.welch(q_prime, fs, window='hann', nperseg=512)

    # 4. Extract Peak
    peak_idx = np.argmax(psd)
    f_dom = freqs[peak_idx]
    
    # 5. Non-dimensionalization
    St = (f_dom * L_char) / U_inf
    
    return f_dom, St, freqs, psd

if __name__ == "__main__":
    # --- Local Test: Synthetic Rossiter Mode Signal ---
    # In production, load via: data = pd.read_csv('../data/monitor_point.csv')
    
    U_test = 10.0   # m/s
    L_test = 0.05   # m (5cm cavity)
    
    # Generate test signal (1000 steps)
    t = np.linspace(0, 2, 2000) 
    
    # Superposition of a primary mode (St=0.6) + random turbulence noise
    # f = St * U / L = 0.6 * 10 / 0.05 = 120 Hz
    target_freq = 120.0
    signal_raw = 0.1 * np.sin(2 * np.pi * target_freq * t) + 0.02 * np.random.randn(len(t))
    
    print("[Info] Running PSD analysis on test signal...")
    f_peak, St_peak, f_axis, p_axis = compute_strouhal_welch(t, signal_raw, L_test, U_test)
    
    print(f"\n--- Spectral Results ---")
    print(f" Dominant Freq : {f_peak:.2f} Hz")
    print(f" Strouhal No   : {St_peak:.3f}")
    
    # Empirical check for Shear Layer mode
    if 0.0 < St_peak < 1.0:
        print(" -> Detected mode within Shear Layer Instability range.")
    else:
        print(" -> Frequency likely associated with acoustic resonance or noise.")
        
    # Plotting (Keep disabled for server-side runs)
    # plt.semilogy(f_axis, p_axis)
    # plt.xlabel('Frequency [Hz]')
    # plt.show()
