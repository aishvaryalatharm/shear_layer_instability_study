"""
Module: droplet_shape_calc.py
Author: Aishvaryalatha R M
Date: Jan 2026

Description: 
    Quick script to estimate Capillary (Ca) and Weber (We) numbers for 
    microfluidic T-junction experiments. 
    
    Used to check if parameters (Q_c, Q_d) fall within the stable "dripping" 
    regime vs "jetting" regime based on the Anna et al. (2003) phase diagram.
"""

import numpy as np

def get_flow_parameters(Q_ul_min, w_channel_um, h_channel_um):
    """
    Converts syringe pump flow rate (uL/min) to mean velocity (m/s).
    Assumes rectangular PDMS channel cross-section.
    """
    # Convert units to SI
    Q_m3_s = (Q_ul_min * 1e-9) / 60.0
    Area_m2 = (w_channel_um * 1e-6) * (h_channel_um * 1e-6)
    
    U_avg = Q_m3_s / Area_m2
    return U_avg

def calculate_regime_numbers(mu_c, U, sigma, rho_c, D_hyd):
    """
    Returns Ca and We.
    mu_c: viscosity (Pa.s)
    sigma: interfacial tension (N/m)
    """
    if sigma <= 0:
        print("[Warning] Zero or negative surface tension? Check inputs.")
        return None

    Ca = (mu_c * U) / sigma
    We = (rho_c * (U**2) * D_hyd) / sigma
    
    return Ca, We

if __name__ == "__main__":
    # --- Experimental Setup (Mineral Oil + Span 80) ---
    mu_oil = 0.028      # Pa.s (approx 28 cP)
    rho_oil = 850       # kg/m^3
    sigma_oil_water = 0.005 # N/m (with surfactant)
    
    # Geometry (Standard Soft Lithography Channel)
    W = 100  # microns
    H = 50   # microns
    D_hyd = (2*W*H)/(W+H) * 1e-6 # Hydraulic diameter in meters
    
    # Test Flow Rates (Sweep)
    flow_rates_ul_min = [5, 20, 100] # uL/min
    
    print(f"--- Regime Check (Channel: {W}x{H} um) ---")
    
    for Q in flow_rates_ul_min:
        U = get_flow_parameters(Q, W, H)
        Ca, We = calculate_regime_numbers(mu_oil, U, sigma_oil_water, rho_oil, D_hyd)
        
        # Simple threshold check for Dripping to Jetting transition
        # Usually occurs around Ca ~ 0.1 for T-junctions
        regime = "DRIPPING" if Ca < 0.1 else "JETTING / UNSTABLE"
        
        print(f" Q = {Q:3d} uL/min | U = {U:.3f} m/s | Ca = {Ca:.4f} -> {regime}")
