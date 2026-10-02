"""Illustrative lumped cyclization CSTR; not fitted Iso E Super kinetics.
Units: L, mol, min, kg, kJ, K. Fixed catalyst activity is absorbed in k.
"""
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Parameters:
    V: float = 100.0
    q: float = 100.0 / 30.0
    CA_feed: float = 1.0
    CP_feed: float = 0.0
    T_feed: float = 320.0
    rho: float = 0.85
    cp: float = 2.0
    UA: float = 1.5
    delta_H: float = -20.0
    k_ref: float = 0.05
    T_ref: float = 330.0
    Ea: float = 60.0
    R: float = 0.008314462618


def rate(CA, T, p):
    if T <= 0:
        raise ValueError('Temperature must be absolute and positive')
    return p.k_ref * np.exp(-p.Ea / p.R * (1 / T - 1 / p.T_ref)) * CA


def rhs(t, state, jacket_temperature, p):
    CA, CP, T = state
    r = rate(CA, T, p)
    D = p.q / p.V
    return np.array([
        D * (p.CA_feed - CA) - r,
        D * (p.CP_feed - CP) + r,
        D * (p.T_feed - T) - p.delta_H * r / (p.rho * p.cp)
        + p.UA * (jacket_temperature - T) / (p.rho * p.cp * p.V),
    ])


def conversion(state, p):
    """Concentration-based apparent conversion; steady-feed CSTR convention.
    During startup this can reflect inventory dilution as well as reaction.
    """
    return 1 - np.asarray(state)[0] / p.CA_feed
