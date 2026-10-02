"""Run fixed-input startup and separate open-loop jacket steps."""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from model import Parameters, rhs, conversion

p = Parameters()
out = Path(__file__).resolve().parents[1] / 'results'
out.mkdir(exist_ok=True)
scale = np.array([p.CA_feed, p.CA_feed, 10.0])

def steady(u, guess):
    sol = root(lambda x: rhs(0, x, u, p) / scale, guess)
    if not sol.success or np.max(np.abs(rhs(0, sol.x, u, p) / scale)) > 1e-8:
        raise RuntimeError('Steady-state root did not converge')
    return sol.x

def integrate(u, x0, tol=1e-9):
    sol = solve_ivp(lambda t,x: rhs(t,x,u,p), (0,300), x0,
                    t_eval=np.linspace(0,300,1201), rtol=tol, atol=tol*0.01)
    if not sol.success:
        raise RuntimeError(sol.message)
    if sol.y[:2].min() < -1e-8 or sol.y[2].min() <= 0:
        raise RuntimeError('Nonphysical state')
    return sol

def jacobian(x,u):
    h = 1e-5
    return np.column_stack([(rhs(0,x+np.eye(3)[i]*h,u,p)-rhs(0,x-np.eye(3)[i]*h,u,p))/(2*h) for i in range(3)])

u0 = 330.0
base = steady(u0, [0.5,0.5,325])
startup = integrate(u0,[1.0,0.0,320.0])
checks = {}
runs = [('startup',u0,startup,base)]
for name,u in [('warming_step',340.0),('cooling_step',320.0)]:
    target = steady(u,base)
    sol = integrate(u,base)
    runs.append((name,u,sol,target))
    change = conversion(target,p)-conversion(base,p)
    assert change > 0 if u > u0 else change < 0

fig,axs = plt.subplots(4,1,figsize=(9,11),sharex=True)
for name,u,sol,target in runs:
    err = np.max(np.abs((sol.y-target[:,None])/scale[:,None]),axis=0)
    # Settled means within 1% of the state scales and remaining there.
    outside = np.flatnonzero(err > 0.01)
    settle_idx = int(outside[-1]+1) if outside.size else 0
    settling = float(sol.t[settle_idx]) if settle_idx < len(sol.t) else None
    residual = float(np.max(np.abs(rhs(0,sol.y[:,-1],u,p)/scale)))
    endpoint = float(err[-1])
    fine = integrate(u, sol.y[:,0],tol=1e-11)
    repeat_diff = float(np.max(np.abs((fine.y-sol.y)/scale[:,None])))
    eig = np.linalg.eigvals(jacobian(target,u))
    # CA+CP obeys a separate total pseudo-component transport balance.
    total0 = np.sum(sol.y[:2,0]); total_feed = p.CA_feed+p.CP_feed
    exact_total = total_feed+(total0-total_feed)*np.exp(-p.q/p.V*sol.t)
    inventory_error = float(np.max(np.abs(sol.y[0]+sol.y[1]-exact_total)))
    assert endpoint < 1e-6 and residual < 1e-7 and repeat_diff < 1e-6
    assert inventory_error < 1e-7 and np.all(eig.real < 0) and settling is not None
    checks[name] = dict(jacket_K=u,steady_state=target.tolist(),
        apparent_conversion=float(conversion(target,p)),settling_min=settling,
        scaled_endpoint_error=endpoint,scaled_rhs_residual_per_min=residual,
        tolerance_repeat_difference=repeat_diff,total_inventory_error_mol_L=inventory_error,
        local_eigenvalues_per_min=[{'real':float(e.real),'imag':float(e.imag)} for e in eig])
    np.savetxt(out/f'{name}.csv',np.column_stack([sol.t,sol.y.T,conversion(sol.y,p)]),
               fmt='%.10g',delimiter=',',header='time_min,CA_mol_L,CP_mol_L,T_K,apparent_conversion',comments='')
    for ax,values in zip(axs,[sol.y[0],sol.y[1],sol.y[2],conversion(sol.y,p)]):
        ax.plot(sol.t,values,label=name)
for ax,label in zip(axs,['Precursor (mol/L)','Lumped products (mol/L)','Reactor T (K)','Apparent conversion']):
    ax.set_ylabel(label); ax.grid(alpha=0.3); ax.legend()
axs[-1].set_xlabel('Time since startup or jacket step (min)')
fig.suptitle('Illustrative model: fixed-input startup and separate jacket steps')
fig.tight_layout(); fig.savefig(out/'open_loop.png',dpi=160)
(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
