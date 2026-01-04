"""
Module: 03_eigenvalue_solver_demo.py
Author: Aishvaryalatha R M
Date: Jan 2026

Description: 
    Prototype solver for the 1D Diffusion-Advection operator.
    Demonstrates the matrix assembly and Arnoldi iteration workflow required 
    for the full 2D Global Stability Analysis.
"""

import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigs
import sys

def build_1d_operator(N, L, nu):
    """
    Assembles the sparse system matrix A for:
    du/dt = nu * d^2u/dx^2
    
    Discretization: 2nd Order Central Differences (FD).
    """
    # Grid parameters
    dx = L / (N - 1)
    
    # 3-point stencil coefficients for Laplacian: [1, -2, 1] / dx^2
    # We use sparse diagonals to save memory for large N
    main_diag = -2.0 * np.ones(N)
    off_diag  =  1.0 * np.ones(N-1)
    
    diagonals = [main_diag, off_diag, off_diag]
    offsets   = [0, -1, 1]
    
    # Construct CSR matrix
    A = diags(diagonals, offsets, shape=(N, N), format='csr')
    A = A * (nu / dx**2)
    
    # --- Boundary Conditions ---
    # Enforcing Homogeneous Dirichlet: u(0) = 0, u(L) = 0
    # Method: Replace boundary rows with Identity (1*u = 0) to decouple them
    
    # Left Wall
    A[0, :] = 0.0
    A[0, 0] = 1.0  
    
    # Right Wall
    A[-1, :] = 0.0
    A[-1, -1] = 1.0
    
    return A

def run_arnoldi_solver(A, k=5):
    """
    Wrapper for ARPACK via scipy.sparse.linalg.eigs
    Target: 'LR' (Largest Real part) -> Corresponds to least stable modes.
    """
    print(f" -> Starting Arnoldi iteration (seeking top {k} modes)...")
    
    try:
        vals, vecs = eigs(A, k=k, which='LR')
        return vals
    except Exception as e:
        print(f"[Error] Eigensolver failed to converge: {e}")
        return None

if __name__ == "__main__":
    # --- Physics Parameters ---
    N_points = 200     # Mesh density
    L_domain = 1.0     # Domain length
    viscosity = 1e-3   # Diffusion coeff
    
    print(f"[Info] Initializing 1D Stability Test (N={N_points}, nu={viscosity})")
    
    # 1. Build Operator
    L_op = build_1d_operator(N_points, L_domain, viscosity)
    print(f" -> Operator assembled. Matrix shape: {L_op.shape}")
    
    # 2. Solve Eigenvalue Problem
    eigenvalues = run_arnoldi_solver(L_op, k=4)
    
    if eigenvalues is not None:
        print("\n--- Computed Spectrum (Growth Rates) ---")
        for i, ev in enumerate(eigenvalues):
            # Filter out the dummy BC modes (eigenvalue ~ 1.0)
            if abs(ev.real - 1.0) > 1e-4:
                sigma_r = ev.real
                freq = ev.imag
                status = "STABLE" if sigma_r < 0 else "UNSTABLE"
                print(f" Mode {i}: {sigma_r:.4f} + {freq:.4f}j  [{status}]")
