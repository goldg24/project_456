"""Launch with: python -m streamlit run app.py"""
import sys
from pathlib import Path
from dataclasses import asdict
import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
sys.path.insert(0,str(Path(__file__).resolve().parent/'src'))
from model import Parameters, rate
from experiment import Experiment, solve_experiment

st.set_page_config(page_title='Cyclization Lab | CHE 456',page_icon='🧪',layout='wide')
st.markdown('''<style>
.stApp {background: #f6f8fb;} h1 {letter-spacing:-1.4px;}
.block-container {padding-top:2rem;} .process {background:#101e31;color:#e5eefc;border-radius:16px;padding:25px;display:flex;align-items:center;justify-content:space-around;gap:20px;flex-wrap:wrap;}
.process .vessel {border:3px solid #5dd9cf;border-radius:18px;background:#173b48;padding:22px 35px;text-align:center;}
.process .stream {font-size:15px;line-height:1.9;} .process small {color:#aabbd3;}
</style>''',unsafe_allow_html=True)
st.caption('CHE 456 · OPEN-LOOP DYNAMICS')
st.title('Cyclization lab')
st.write('Adjust the jacket input. Watch thermal energy and material inventories respond over time.')
st.warning('Illustrative parameters: this is a learning model, not validated Iso E Super kinetics. Lumped products do not indicate purity.')

with st.sidebar:
    st.header('Set up an experiment')
    with st.form('inputs'):
        start=st.selectbox('Initial condition',['Feed-filled reactor (startup)','Settled at initial jacket temperature'])
        u0=st.slider('Initial jacket temperature (K)',300.,360.,330.,1.)
        step=st.checkbox('Apply a jacket-temperature step',True)
        u1=st.slider('Jacket temperature after step (K)',300.,360.,340.,1.)
        duration=st.slider('Simulation duration (min)',60,600,300,30)
        step_time=st.slider('Step time (min)',5,550,90,5)
        with st.expander('Feed and reactor parameters'):
            volume=st.number_input('Working volume (L)',min_value=10.,max_value=1000.,value=100.)
            flow=st.number_input('Feed flow (L/min)',min_value=0.1,max_value=50.,value=100./30.)
            caf=st.number_input('Feed precursor (mol/L)',min_value=0.1,max_value=3.,value=1.)
            tf=st.slider('Feed temperature (K)',300.,350.,320.,1.)
            ua=st.number_input('UA (kJ/min/K)',min_value=0.1,max_value=10.,value=1.5,step=0.1)
        run=st.form_submit_button('Run simulation',type='primary',width='stretch')
    st.caption('Inputs are held fixed between steps. No feedback controller is active. Change controls and press Run simulation to apply them.')

if run or 'experiment' not in st.session_state:
    try:
        p=Parameters(V=volume,q=flow,CA_feed=caf,T_feed=tf,UA=ua)
        cfg=Experiment(u0,u1,float(step_time),float(duration),step,start.startswith('Settled'))
        result=solve_experiment(p,cfg)
        st.session_state.experiment=(p,cfg,result)
    except (ValueError,RuntimeError,FloatingPointError) as e:
        st.error(str(e))
        if 'experiment' not in st.session_state:
            st.stop()
        st.info('The previous successful run remains displayed.')
p,cfg,r=st.session_state.experiment
t,y,u,X=r['t'],r['y'],r['u'],r['conversion']

st.subheader('Inspect the reactor')
time=st.slider('Inspection time (min)',0.,float(cfg.duration),min(90.,float(cfg.duration)),0.5,key=f'inspect_{cfg.duration}')
i=int(np.argmin(np.abs(t-time)))
cols=st.columns(4)
for c,label,value in zip(cols,['Jacket input','Reactor temperature','Apparent conversion','Lumped product'],[f'{u[i]:.1f} K',f'{y[2,i]:.2f} K',f'{100*X[i]:.1f}%',f'{y[1,i]:.3f} mol/L']):
    c.metric(label,value)
st.markdown(f'''<div class="process"><div class="stream"><small>FIXED FEED →</small><br>{p.q:.2f} L/min<br>Precursor {p.CA_feed:.2f} mol/L<br>{p.T_feed:.1f} K</div><div class="vessel"><small>WELL-MIXED CSTR · {p.V:.0f} L</small><br><strong>{y[2,i]:.2f} K</strong><br>Precursor {y[0,i]:.3f} mol/L<br>Products {y[1,i]:.3f} mol/L<br><small>Jacket {u[i]:.1f} K</small></div><div class="stream"><small>→ OUTLET</small><br>{p.q:.2f} L/min<br>Same composition as vessel<br>Conversion {100*X[i]:.1f}%</div></div>''',unsafe_allow_html=True)
st.caption(f'Snapshot at {t[i]:.1f} min. Move the inspection slider to update the vessel and readouts; chart playback below animates the trajectories separately.')

st.subheader('Input and output trajectories')
fig=make_subplots(rows=2,cols=2,subplot_titles=['Jacket input','Reactor temperature','Material inventories','Apparent conversion'])
series=[(u,'Jacket temperature','#875af5',1,1),(y[2],'Reactor temperature','#ee8450',1,2),(y[0],'Precursor','#347fe4',2,1),(y[1],'Lumped products','#12a79e',2,1),(100*X,'Conversion','#12a79e',2,2)]
for values,name,color,row,col in series:
    fig.add_trace(go.Scatter(x=t,y=values,name=name,line=dict(color=color,width=3,shape='hv' if name=='Jacket temperature' else 'linear')),row=row,col=col)
for row in [1,2]:
    for col in [1,2]:
        fig.update_xaxes(title_text='Time (min)',range=[0,cfg.duration],row=row,col=col)
        if cfg.apply_step:
            fig.add_vline(x=cfg.step_time,line_dash='dot',line_color='#8996a7',row=row,col=col)
        fig.add_vline(x=float(t[i]),line_color='#cad3df',row=row,col=col)
for row,col,label in [(1,1,'K'),(1,2,'K'),(2,1,'mol/L'),(2,2,'%')]:
    fig.update_yaxes(title_text=label,row=row,col=col)
# Fixed axes ensure playback does not distort the apparent response.
for values,_,_,row,col in series:
    combined=np.r_[y[0],y[1]] if row==2 and col==1 else values
    lo,hi=float(combined.min()),float(combined.max()); pad=max((hi-lo)*.12,.05)
    fig.update_yaxes(range=[lo-pad,hi+pad],row=row,col=col)
frame_indices=np.unique(np.r_[np.linspace(0,len(t)-1,61,dtype=int),len(t)-1])
fig.frames=[go.Frame(name=str(j),data=[go.Scatter(x=t[:j+1],y=values[:j+1]) for values,*_ in series],traces=list(range(5))) for j in frame_indices]
fig.update_layout(height=620,template='plotly_white',margin=dict(l=20,r=20,t=55,b=80),legend=dict(orientation='h',y=-.15),
    updatemenus=[dict(type='buttons',direction='left',x=0,y=1.18,buttons=[
        dict(label='▶ Play',method='animate',args=[None,dict(frame=dict(duration=100,redraw=False),transition=dict(duration=0),fromcurrent=False)]),
        dict(label='Pause',method='animate',args=[[None],dict(mode='immediate',frame=dict(duration=0,redraw=False))]),
        dict(label='Full result',method='animate',args=[[str(len(t)-1)],dict(mode='immediate',frame=dict(duration=0,redraw=False))])])])
st.plotly_chart(fig,width='stretch',key='trajectories')
st.caption('Dashed lines mark the scheduled input step. The pale solid line marks the inspection time. Hover for values; drag to zoom; double-click to reset.')

left,right=st.columns(2)
with left:
    st.subheader('Run checks')
    st.write(f'Residence time: **{p.V/p.q:.1f} min**')
    st.write(f'Total inventory error: **{r["balance_error"]:.2e} mol/L**')
    if r['residual']<1e-7:
        st.success('Endpoint is near a fixed-input equilibrium (scaled derivative < 1e-7 per min).')
    else:
        st.info('Still moving at the endpoint. Increase the duration to check settling.')
    st.caption('A small endpoint derivative is a settling check, not a global stability proof.')
with right:
    st.subheader('Export this experiment')
    df=pd.DataFrame(dict(time_min=t,jacket_K=u,precursor_mol_L=y[0],products_mol_L=y[1],reactor_K=y[2],apparent_conversion=X))
    st.download_button('Download trajectory CSV',df.to_csv(index=False),'reactor_experiment.csv','text/csv')
    metadata=dict(parameters=asdict(p),experiment=asdict(cfg),checks=dict(inventory_error=r['balance_error'],scaled_endpoint_derivative=r['residual']))
    st.download_button('Download inputs and checks',json.dumps(metadata,indent=2),'reactor_experiment.json','application/json')
with st.expander('Model equations and interpretation'):
    st.code('r = k_ref exp[−Ea/R (1/T − 1/T_ref)] CA\ndCA/dt = (q/V)(CA_feed − CA) − r\ndCP/dt = (q/V)(CP_feed − CP) + r\ndT/dt = (q/V)(T_feed − T) − delta_H r/(rho cp)\n        + UA(Tj − T)/(rho cp V)')
    st.write('The jacket temperature is the manipulated input. Precursor concentration, lumped product concentration, and temperature are the storage states. Conversion is inferred from precursor concentration. During startup it can reflect inventory effects; it does not measure purity.')
