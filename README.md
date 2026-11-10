# PitchLab
A football analytics project combining Python for data work and modelling with C++ for computation-heavy simulations. This project works from shot-level models up to full season forecasts.


## Contents
| Module        | Language      | Description                                                                   | Status        |
|---------------|---------------|-------------------------------------------------------------------------------|---------------|
| `xg_model/`   | Python        | Expected goals model using logistic regression and gradient boosting          | IN PROGRESS   |
| `ratings/`    | Python        | Team attack and defence strengths from historical results (Poisson / Elo)     | PLANNED       |
| `szn_sim/`    | C++           | Monte Carlo season simulator producing title, top-four and relegation odds    | PLANNED       |
| `vzl/`        | Python        | Shot maps, pass networks, and probability charts                              | PLANNED       |
  
**Model Shots** (`xg_model`): Estimate the probability that each shot becomes a goal from location, body part, context  
**Rate Teams** (`ratings`): Fit team strengths and export parameters  
**Simulate Seasons** (`szn_sim`): Read parameters from `ratings` in C++ and run 100K+ simulated seasons  
**Visualize** (`vsl`): Plot results


## Data
Uses [StatsBomb Open Data](https://github.com/statsbomb/open-data) via the `statsbombpy` package, and historical results from [football-data.co.uk](https://www.football-data.co.uk/). Please follow the terms of use and attribution requirements of each data source.


## Getting started
    git clone https://github.com/NguyenHLam/PitchLab.git
    cd PitchLab
    pip install statsbombpy pandas numpy scikit-learn matplotlib mplsoccer
    python xg_model/xg_model.py


## Acknowledgements
Data provided by StatsBomb. Pitch plotting via mplsoccer.