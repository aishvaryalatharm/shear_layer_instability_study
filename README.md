# Numerical Investigation of Shear Layer Sensitivity in Cavity Flows

**Author:** Aishvaryalatha R M

**Status:** In Development

## Project Overview
This repository contains a Python based computational framework designed to interface with commercial CFD solvers (ANSYS Fluent) for hydrodynamic stability analysis.

The primary objective is to develop a hybrid workflow that uses robust commercial solvers for steady state base flow generation, coupled with custom Python scripts for Linearized Navier Stokes (LNS) analysis. This approach aims to reduce the computational cost of identifying critical Reynolds numbers and absolute instability modes in open cavity flows.

## Repository Structure

### 1. Pre Processing & Data Ingestion (src/)
* **01_process_ansys_data.py:** A module to parse ASCII velocity and pressure fields exported from ANSYS Fluent. It handles the mapping of unstructured finite volume data onto structured grids suitable for finite difference differentiation matrices.

* **02_fft_analysis.py**: Performs spectral analysis (PSD via Welch's method) on lift/drag history to compute the Strouhal number ($St$). Used to benchmark URANS results against Global Stability predictions.

### 2. Global Stability Solver (src/)
* **03_eigenvalue_solver_demo.py:** A prototype solver for the discretized diffusion-advection operator. It utilizes sparse matrix algebra and the Arnoldi iterative method (via `scipy.sparse.linalg`) to extract the least stable eigenmodes. This script serves as the validation step for the matrix assembly logic before full 2D implementation.

### 3. Multiphase Extension (microfluidics_proof/)
* **droplet_shape_calc.py:** A standalone utility for calculating Capillary (Ca) and Weber (We) numbers in microfluidic channels. This module is designed to predict flow regimes (dripping vs. jetting) in T junction and flow focusing geometries, supporting parallel investigations into interfacial instabilities.

## Implementation Details
* **Base Flow:** Steady state laminar solutions are generated in ANSYS Fluent to ensure strict convergence.
* **Linearization:** The Jacobian matrix is assembled in Python using `scipy.sparse`.
* **Eigenvalue Problem:** The system is solved using the shift-invert Arnoldi method to isolate physically relevant global modes.

## Dependencies
* Python 3.x
* NumPy, SciPy, Pandas
* ANSYS Fluent (Base flow generation)
