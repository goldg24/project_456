"""Open-loop experiments shared by the visual dashboard and headless checks."""
from dataclasses import dataclass
import numpy as np
from scipy.integrate import solve_ivp
from model import Parameters, rhs

@dataclass(frozen=True)
class Experiment:
    jacket_before: float = 330.0
    jacket_after: float = 340.0
    step_time: float = 90.0
    duration: float = 300.0
    apply_step: bool = True
    start_at_steady: bool = False


def solve_experiment(p=Parameters(), cfg=Experiment()):
    if min(p.V,p.q,p.CA_feed,p.rho,p.cp,p.T_feed,cfg.jacket_before,cfg.jacket_after,cfg.duration) <= 0:
        raise ValueError('Volume, flow, feed concentration, temperatures and duration must be positive.')
    if cfg.apply_step and not 0 < cfg.step_time < cfg.duration:
        raise ValueError('Step time must be between zero and the simulation duration.')
    x0 = np.array([p.CA_feed,p.CP_feed,p.T_feed])
    def integrate(u,span,x):
        sol = solve_ivp(lambda t,y: rhs(t,y,u,p),span,x,rtol=1e-9,atol=1e-11,dense_output=True)
        if not sol.success:
            raise ValueError(sol.message)
        return sol
    if cfg.start_at_steady:
        # Approach the stable branch dynamically rather than selecting an arbitrary root.
        warmup=integrate(cfg.jacket_before,(0,100*max(p.V/p.q,1)),x0)
        x0=warmup.y[:,-1]
        if np.max(np.abs(rhs(0,x0,cfg.jacket_before,p)/np.array([p.CA_feed,p.CA_feed,10.])))>1e-7:
            raise ValueError('The initial fixed-input warmup did not settle; choose startup mode.')
    t=np.unique(np.r_[np.linspace(0,cfg.duration,601),cfg.step_time if cfg.apply_step else 0])
    if cfg.apply_step:
        a=integrate(cfg.jacket_before,(0,cfg.step_time),x0)
        b=integrate(cfg.jacket_after,(cfg.step_time,cfg.duration),a.y[:,-1])
        y=np.empty((3,len(t))); before=t<cfg.step_time
        y[:,before]=a.sol(t[before]); y[:,~before]=b.sol(t[~before])
    else:
        a=integrate(cfg.jacket_before,(0,cfg.duration),x0); y=a.sol(t)
    u=np.where(t>=cfg.step_time,cfg.jacket_after,cfg.jacket_before) if cfg.apply_step else np.full_like(t,cfg.jacket_before)
    if not np.all(np.isfinite(y)) or y[:2].min() < -1e-7 or y[2].min()<=0:
        raise ValueError('The run produced nonphysical states; review inputs and model assumptions.')
    total_feed=p.CA_feed+p.CP_feed
    exact=total_feed+(x0[0]+x0[1]-total_feed)*np.exp(-p.q/p.V*t)
    balance_error=float(np.max(np.abs(y[0]+y[1]-exact)))
    residual=float(np.max(np.abs(rhs(t[-1],y[:,-1],u[-1],p)/np.array([p.CA_feed,p.CA_feed,10.]))))
    return dict(t=t,y=y,u=u,conversion=1-y[0]/p.CA_feed,
                balance_error=balance_error,residual=residual)
