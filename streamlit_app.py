import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="RiskMap AI Intelligence Platform",
                   page_icon="🌍", layout="wide",
                   initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background-color: #0a0e1a; color: #e8eaf6; }
.metric-card {
    background: linear-gradient(145deg,#12172b,#1a2035);
    border:1px solid #2a3050; border-radius:14px;
    padding:20px; text-align:center;
    box-shadow:0 4px 20px rgba(0,0,0,0.3);
}
.metric-title{font-size:11px;color:#8892b0;text-transform:uppercase;letter-spacing:1.5px;}
.metric-value{font-size:2rem;font-weight:700;color:#64ffda;margin:8px 0 4px 0;}
.metric-sub{font-size:11px;color:#6272a4;}
.section-header{
    background:linear-gradient(90deg,#1a2035,transparent);
    border-left:4px solid #64ffda;padding:10px 18px;
    margin:24px 0 14px 0;font-size:15px;font-weight:600;
    color:#e8eaf6;border-radius:0 8px 8px 0;
}
.alert-high{background:#1f0f0f;border:1px solid #e74c3c;border-radius:10px;padding:12px 16px;color:#e74c3c;margin:6px 0;}
.alert-medium{background:#1f1a0f;border:1px solid #f39c12;border-radius:10px;padding:12px 16px;color:#f39c12;margin:6px 0;}
.alert-low{background:#0f1f0f;border:1px solid #2ecc71;border-radius:10px;padding:12px 16px;color:#2ecc71;margin:6px 0;}
.demo-badge{background:#1a2035;border:1px solid #64ffda;border-radius:20px;
    padding:4px 14px;font-size:11px;color:#64ffda;display:inline-block;margin-bottom:12px;}
section[data-testid="stSidebar"]{background:#0d1120;border-right:1px solid #1e2540;}
.stButton>button{
    background:linear-gradient(135deg,#64ffda,#00b4d8)!important;
    color:#0a0e1a!important;font-weight:600!important;
    border:none!important;border-radius:10px!important;
}
</style>
""", unsafe_allow_html=True)

# ── COMPANY DATABASE ──────────────────────────────────────────────
COMPANIES = {
    'AWS': {
        'full_name':'Amazon Web Services','password':'aws2026',
        'sector':'Cloud Computing / Technology','hq':'Seattle, USA',
        'revenue_2024':'$91B (estimated)',
        'exposure':{
            'United States':38.0,'Germany':9.0,'United Kingdom':7.0,
            'Japan':7.0,'China':5.0,'India':6.0,'Singapore':5.0,
            'Canada':5.0,'Australia':4.0,'France':4.0,'Brazil':3.0,'Other':7.0,
        },
        'supply_chain':['United States','Ireland','Germany','Singapore','India'],
        'color':'#FF9900',
        'report_note':'📋 Source: AWS Annual Report 2024 (public). In a live system, data would be auto-fetched from SEC EDGAR / company IR pages.',
    },
    'NVIDIA': {
        'full_name':'NVIDIA Corporation','password':'nvidia2026',
        'sector':'Semiconductors / AI Hardware','hq':'Santa Clara, USA',
        'revenue_2024':'$60B',
        'exposure':{
            'China':25.0,'United States':30.0,'Taiwan':15.0,
            'Korea, Rep.':10.0,'Japan':8.0,'Germany':5.0,
            'Singapore':4.0,'Other':3.0,
        },
        'supply_chain':['Taiwan','Korea, Rep.','China','United States'],
        'color':'#76B900',
        'report_note':'📋 Source: NVIDIA Annual Report 2024 (public). TSMC is primary fab partner.',
    },
    'Microsoft': {
        'full_name':'Microsoft Corporation','password':'msft2026',
        'sector':'Software / Cloud / AI','hq':'Redmond, USA',
        'revenue_2024':'$245B',
        'exposure':{
            'United States':45.0,'Germany':10.0,'United Kingdom':8.0,
            'Japan':7.0,'China':6.0,'India':6.0,'France':5.0,
            'Canada':5.0,'Australia':4.0,'Other':4.0,
        },
        'supply_chain':['United States','Ireland','India','Singapore'],
        'color':'#00A4EF',
        'report_note':'📋 Source: Microsoft Annual Report FY2024 (public).',
    },
}

# ── SESSION STATE ─────────────────────────────────────────────────
for key, default in [('logged_in',False),('company',None)]:
    if key not in st.session_state:
        st.session_state[key] = default

# ════════════════════════════════════════════════════════════════
# LOGIN PAGE
# ════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    _, col_m, _ = st.columns([1,1.2,1])
    with col_m:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align:center;margin-bottom:8px'><span style='font-size:3.5rem'>🌍</span></div>
        <div style='text-align:center;font-size:2rem;font-weight:700;
            background:linear-gradient(135deg,#64ffda,#00b4d8);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent'>
            RiskMap AI Intelligence
        </div>
        <div style='text-align:center;color:#8892b0;font-size:0.9rem;margin-bottom:32px'>
            AI-Powered Geopolitical Risk &amp; Investment Platform
        </div>""", unsafe_allow_html=True)

        mode = st.radio("", ["🔐 Login","📝 Sign Up (Demo)"],
                        horizontal=True, label_visibility="collapsed")

        if mode == "🔐 Login":
            st.markdown("<br>", unsafe_allow_html=True)
            co = st.selectbox("🏢 Company",list(COMPANIES.keys()),
                              format_func=lambda x:f"{x} — {COMPANIES[x]['full_name']}")
            pw = st.text_input("🔑 Password",type="password",placeholder="Enter password")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Login →", use_container_width=True):
                if pw == COMPANIES[co]['password']:
                    st.session_state.logged_in = True
                    st.session_state.company   = co
                    st.rerun()
                else:
                    st.error("❌ Wrong password. Demo: aws2026 / nvidia2026 / msft2026")
            st.markdown("""
            <div style='background:#0d1120;border:1px solid #2a3050;border-radius:10px;
                        padding:12px;font-size:0.8rem;color:#8892b0;margin-top:12px'>
                <strong style='color:#64ffda'>Demo credentials:</strong><br>
                AWS → aws2026 &nbsp;|&nbsp; NVIDIA → nvidia2026 &nbsp;|&nbsp; Microsoft → msft2026
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background:#0d1120;border:1px solid #64ffda;border-radius:12px;
                        padding:16px;margin-bottom:16px'>
                <div class='demo-badge'>📌 DEMO MODE</div><br>
                <span style='color:#ccd6f6;font-size:0.9rem'>
                In a production system, this would:<br><br>
                ✅ Verify company via business email<br>
                ✅ Auto-fetch annual reports from SEC EDGAR<br>
                ✅ Extract revenue by geography using NLP<br>
                ✅ Build company-specific risk profile automatically<br><br>
                <span style='color:#64ffda'>Use Login tab with pre-loaded company data for demo.</span>
                </span>
            </div>""", unsafe_allow_html=True)
            nc = st.text_input("Company Name", placeholder="e.g. Tesla, Infosys...")
            ne = st.text_input("Business Email", placeholder="you@company.com")
            if st.button("Request Access →", use_container_width=True):
                if nc:
                    st.success(f"✅ Demo: Access would be granted to {nc}. Use Login tab.")
    st.stop()

# ════════════════════════════════════════════════════════════════
# MAIN DASHBOARD
# ════════════════════════════════════════════════════════════════
ck   = st.session_state.company
ci   = COMPANIES[ck]

@st.cache_data
def load_data():
    for fname in ['final_predictions.csv','ai_risk_ml_results.csv']:
        if os.path.exists(fname):
            return pd.read_csv(fname), fname
    st.error("❌ No data file found. Run the Colab pipeline first and copy CSVs here.")
    st.stop()

@st.cache_data
def load_news():
    if os.path.exists('news_headlines.csv'):
        return pd.read_csv('news_headlines.csv')
    return pd.DataFrame(columns=['Country','Headline','Risk_Delta','Alert','Source'])

df, dsrc = load_data()
news_df  = load_news()

ALL_FEATURES = [f for f in [
    'GDP_growth','Inflation','Unemployment','FDI','R&D_%GDP',
    'HighTech_exports','Imports_%GDP','Exports_%GDP','Internet_users',
    'Political_Stability','conflict_count','total_deaths',
    'trade_exposure','tech_strength','conflict_intensity'
] if f in df.columns]

df[ALL_FEATURES] = df[ALL_FEATURES].replace([np.inf,-np.inf],np.nan)
for col in ALL_FEATURES:
    df[col] = df[col].fillna(df[col].median())

def safe_norm(s):
    mn,mx=s.min(),s.max()
    return pd.Series(np.zeros(len(s)),index=s.index) if mx==mn else (s-mn)/(mx-mn)

# Standardise risk column
if 'predicted_risk_next_year' not in df.columns:
    df['predicted_risk_next_year'] = df.get('predicted_risk', pd.Series(np.zeros(len(df))))
if 'risk_before_news' not in df.columns:
    df['risk_before_news'] = df['predicted_risk_next_year']
if 'risk_after_news' not in df.columns:
    df['risk_after_news']  = df['predicted_risk_next_year']
if 'data_type' not in df.columns:
    df['data_type'] = df['Year'].apply(lambda y:'forecast' if y>=2025 else 'historical')

RC           = 'predicted_risk_next_year'
all_years    = sorted(df['Year'].unique())
all_countries= sorted(df['Country'].unique().tolist())

# ── SIDEBAR ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center;padding:16px 0 8px 0'>
        <div style='font-size:2rem'>🏢</div>
        <div style='font-weight:700;color:#64ffda;font-size:1.1rem'>{ck}</div>
        <div style='color:#8892b0;font-size:0.8rem'>{ci['full_name']}</div>
        <div style='color:#6272a4;font-size:0.75rem'>{ci['sector']}</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")

    selected_year = st.selectbox("📅 Analysis Year",
                                  sorted(all_years,reverse=True), index=0,
                                  help="2025–2029 = Forecast | 2024 and earlier = Historical")
    is_fc = selected_year >= 2025

    st.markdown(
        f"<div style='background:{'#0f1a0f' if not is_fc else '#0a1020'};"
        f"border:1px solid {'#3498db' if not is_fc else '#64ffda'};"
        f"border-radius:8px;padding:6px 12px;font-size:0.8rem;"
        f"color:{'#3498db' if not is_fc else '#64ffda'}'>"
        f"{'📊 Historical data' if not is_fc else '🔮 AI Forecast (t+1 model)'}</div>",
        unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎯 Country Focus")
    sel_countries = st.multiselect("Compare countries",all_countries,
                                    default=all_countries[:5])
    st.markdown("---")
    st.markdown("### ⚡ Scenario Simulator")
    sc_country = st.selectbox("Country to shock",all_countries)
    with st.expander("🔴 Conflict"):
        sh_conf = st.slider("Conflict intensity",0.0,1.0,0.0,0.05,key="shc")
        sh_dead = st.slider("Casualties",        0.0,1.0,0.0,0.05,key="shd")
    with st.expander("📉 Economy"):
        sh_gdp  = st.slider("GDP Growth",        0.0,1.0,0.5,0.05,key="shg")
        sh_inf  = st.slider("Inflation",         0.0,1.0,0.3,0.05,key="shi")
    with st.expander("🚢 Trade"):
        sh_imp  = st.slider("Import disruption", 0.0,1.0,0.0,0.05,key="shim")
        sh_exp  = st.slider("Export disruption", 0.0,1.0,0.0,0.05,key="she")

    apply_sc = st.button("🔄 Apply Scenario",type="primary",use_container_width=True)
    reset_sc = st.button("↩ Reset",use_container_width=True)
    st.markdown("---")
    if st.button("🚪 Logout",use_container_width=True):
        st.session_state.logged_in=False; st.session_state.company=None; st.rerun()

# ── HEADER ────────────────────────────────────────────────────────
yr_df = df[df['Year']==selected_year].copy()
if len(yr_df)==0: yr_df = df[df['Year']==df['Year'].max()].copy()

high_n = len(yr_df[yr_df[RC]>0.40])
med_n  = len(yr_df[(yr_df[RC]>=0.20)&(yr_df[RC]<=0.40)])
low_n  = len(yr_df[yr_df[RC]<0.20])
avg_r  = yr_df[RC].mean()

# Company weighted risk
exp = ci['exposure']
cr_sum,w_sum = 0.0,0.0
for cty,pct in exp.items():
    m  = yr_df[yr_df['Country'].str.contains(cty.split()[0],case=False,na=False)]
    cr = float(m[RC].values[0]) if len(m)>0 else avg_r
    cr_sum+=cr*pct/100; w_sum+=pct/100
comp_risk = (cr_sum/w_sum) if w_sum>0 else avg_r
comp_color= "#e74c3c" if comp_risk>0.40 else "#f39c12" if comp_risk>0.20 else "#2ecc71"
st.markdown(f"""
<div style='display:flex;align-items:center;justify-content:space-between;
            padding:20px 0 10px 0;border-bottom:1px solid #1e2540;margin-bottom:20px'>
    <div>
        <h1 style='color:#64ffda;font-size:1.8rem;margin:0;font-weight:700'>
            🌍 RiskMap AI Intelligence Platform
        </h1>
        <p style='color:#8892b0;margin:4px 0 0 0;font-size:0.9rem'>
            {selected_year} {'🔮 Forecast' if is_fc else '📊 Historical'} &nbsp;|&nbsp; {ck} Dashboard
        </p>
    </div>
    <div style='text-align:right'>
        <div style='color:#64ffda;font-weight:600'>{ck} &nbsp;
            <span style='color:{comp_color};font-size:0.85rem'>Risk: {comp_risk:.3f}</span>
        </div>
        <div style='color:#8892b0;font-size:0.8rem'>{ci['hq']} | {ci['revenue_2024']}</div>
    </div>
</div>""", unsafe_allow_html=True)

c1,c2,c3,c4,c5 = st.columns(5)
for col,title,val,sub,color in [
    (c1,"🔴 High Risk",str(high_n),"risk > 0.65","#e74c3c"),
    (c2,"🟡 Medium Risk",str(med_n),"risk 0.35–0.65","#f39c12"),
    (c3,"🟢 Low Risk",str(low_n),"risk < 0.35","#2ecc71"),
    (c4,"📊 Global Avg",f"{avg_r:.3f}","all countries","#64ffda"),
    (c5,f"🏢 {ck} Risk",f"{comp_risk:.3f}","weighted exposure",comp_color),
]:
    col.markdown(f"""<div class='metric-card'>
        <div class='metric-title'>{title}</div>
        <div class='metric-value' style='color:{color}'>{val}</div>
        <div class='metric-sub'>{sub}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────
t1,t2,t3,t4,t5,t6,t7 = st.tabs([
    "🔮 5-Year Forecast","📰 News Impact","🏢 Company Risk",
    "🗺️ Risk Map","📊 Allocation","⚡ Scenarios","💡 Strategic Advice"
])

# ════════ TAB 1 — 5-YEAR FORECAST ════════════════════════════════
with t1:
    st.markdown("<div class='section-header'>🔮 5-Year Geopolitical Risk Forecast (2025–2029)</div>",
                unsafe_allow_html=True)
    st.markdown("""<div class='demo-badge'>📌 t+1 Forecasting Model</div>
    <span style='color:#8892b0;font-size:0.85rem'>
    Trained on year <b>t</b> data → predicts risk in year <b>t+1</b>.
    Features for 2025–2029 generated via ARIMA. News signals applied on top.
    </span><br><br>""", unsafe_allow_html=True)

    focus = sel_countries if sel_countries else all_countries[:5]
    palette = px.colors.qualitative.Set2
    fig_fc  = go.Figure()

    for i,c in enumerate(focus):
        color  = palette[i%len(palette)]
        hist_c = df[(df['Country']==c)&(df['data_type']=='historical')][['Year',RC]].dropna()
        fore_c = df[(df['Country']==c)&(df['data_type']=='forecast')][['Year',RC]].dropna()
        if len(hist_c)>0:
            fig_fc.add_trace(go.Scatter(x=hist_c['Year'],y=hist_c[RC],
                name=f"{c}",line=dict(color=color,width=2),mode='lines'))
        if len(fore_c)>0:
            conn = pd.concat([hist_c.tail(1),fore_c])
            fig_fc.add_trace(go.Scatter(x=conn['Year'],y=conn[RC],
                name=f"{c} (forecast)",showlegend=False,
                line=dict(color=color,width=2.5,dash='dash'),
                mode='lines+markers',marker=dict(size=8,symbol='star')))

    fig_fc.add_vline(x=2024.5,line_dash="dot",line_color="#64ffda",
                     annotation_text="← History | Forecast →",
                     annotation_font_color="#64ffda")
    fig_fc.update_layout(
        title="Risk Score — Historical Trend + 5-Year Forecast",
        paper_bgcolor="#12172b",plot_bgcolor="#0d1120",
        font_color="#e8eaf6",height=480,
        legend=dict(bgcolor="#12172b",bordercolor="#2a3050",borderwidth=1),
        yaxis=dict(range=[0,1],gridcolor="#1e2540",title="Predicted Risk (t+1)"),
        xaxis=dict(gridcolor="#1e2540"))
    st.plotly_chart(fig_fc,use_container_width=True)

    # Forecast table
    st.markdown("<div class='section-header'>Forecast Table (2025–2029)</div>",
                unsafe_allow_html=True)
    ft = df[df['data_type']=='forecast'][
        ['Country','Year',RC,'risk_before_news','risk_after_news']
    ].copy()
    ft.columns=['Country','Year','Final Risk','Before News','After News']
    for col in ['Final Risk','Before News','After News']:
        ft[col]=ft[col].round(3)
    ft['Label']=ft['Final Risk'].apply(
        lambda x:'🔴 High' if x>0.65 else('🟡 Medium' if x>0.35 else '🟢 Low'))
    st.dataframe(ft.sort_values(['Year','Final Risk'],ascending=[True,False]).reset_index(drop=True),
                 use_container_width=True,height=400,
                 column_config={"Final Risk":st.column_config.ProgressColumn(
                     "Final Risk",min_value=0,max_value=1,format="%.3f")})

# ════════ TAB 2 — NEWS BEFORE vs AFTER ═══════════════════════════
with t2:
    st.markdown("<div class='section-header'>📰 News Impact — Before vs After Risk Update</div>",
                unsafe_allow_html=True)

    if len(news_df)>0:
        st.markdown("**Latest Headlines Processed:**")
        for _,row in news_df.head(10).iterrows():
            alert=str(row.get('Alert',''))
            color="#e74c3c" if "HIGH" in alert else "#f39c12" if "CAUTION" in alert else "#2ecc71"
            bg   ="#1f0f0f" if "HIGH" in alert else "#1f1a0f" if "CAUTION" in alert else "#0f1f0f"
            d    =f"{row['Risk_Delta']:+.3f}" if 'Risk_Delta' in row else ""
            st.markdown(f"""
            <div style='background:{bg};border-left:3px solid {color};
                        padding:8px 14px;margin:3px 0;border-radius:0 8px 8px 0'>
                <span style='color:{color};font-size:0.8rem;font-weight:600'>{alert} {d}</span>
                <span style='color:#8892b0;font-size:0.8rem'> — {row.get('Country','')}</span><br>
                <span style='color:#ccd6f6;font-size:0.85rem'>{row.get('Headline','')}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>")
    st.markdown("<div class='section-header'>Before vs After News (2025 Forecast)</div>",
                unsafe_allow_html=True)

    cmp = df[(df['Year']==2025)&(df['data_type']=='forecast')][
        ['Country','risk_before_news','risk_after_news']].dropna().copy()
    if len(cmp)==0:
        cmp = df[df['Year']==df['Year'].max()][
            ['Country','risk_before_news','risk_after_news']].dropna().copy()

    cmp['delta']=(cmp['risk_after_news']-cmp['risk_before_news']).round(3)
    cmp = cmp[cmp['delta'].abs()>0.01].sort_values('delta',ascending=False)

    if len(cmp)>0:
        col_c,col_d = st.columns([2,1])
        with col_c:
            fig_ba=go.Figure()
            fig_ba.add_trace(go.Bar(x=cmp['Country'],y=cmp['risk_before_news'],
                name='Before News',marker_color='#3498db',opacity=0.85))
            fig_ba.add_trace(go.Bar(x=cmp['Country'],y=cmp['risk_after_news'],
                name='After News', marker_color='#e74c3c',opacity=0.85))
            fig_ba.update_layout(barmode='group',title='Risk Before vs After News',
                paper_bgcolor="#12172b",plot_bgcolor="#0d1120",font_color="#e8eaf6",
                height=400,yaxis=dict(range=[0,1],gridcolor="#1e2540"),
                xaxis=dict(tickangle=-35),legend=dict(bgcolor="#12172b"))
            st.plotly_chart(fig_ba,use_container_width=True)
        with col_d:
            st.markdown("**Net Change:**")
            for _,row in cmp.iterrows():
                arrow="⬆" if row['delta']>0 else "⬇"
                color="#e74c3c" if row['delta']>0 else "#2ecc71"
                st.markdown(f"""
                <div style='background:#12172b;border:1px solid #2a3050;
                            border-radius:8px;padding:8px 12px;margin:4px 0'>
                    <span style='color:#ccd6f6;font-size:0.85rem'>{row['Country']}</span><br>
                    <span style='color:{color};font-weight:600'>{arrow} {row['delta']:+.3f}</span>
                    <span style='color:#6272a4;font-size:0.75rem'>
                        ({row['risk_before_news']:.3f}→{row['risk_after_news']:.3f})
                    </span>
                </div>""", unsafe_allow_html=True)
    else:
        st.info("No significant news impact detected. Run final_colab_pipeline.py to fetch live news.")

# ════════ TAB 3 — COMPANY RISK ════════════════════════════════════
with t3:
    st.markdown(f"<div class='section-header'>🏢 {ck} — Geopolitical Exposure</div>",
                unsafe_allow_html=True)
    st.markdown(f"""
    <div style='background:#0d1120;border:1px solid #2a3050;border-radius:12px;
                padding:14px 18px;margin-bottom:16px;font-size:0.85rem;color:#8892b0'>
        {ci['report_note']}
    </div>""", unsafe_allow_html=True)

    exp_rows=[]
    for cty,pct in exp.items():
        m  = yr_df[yr_df['Country'].str.contains(cty.split()[0],case=False,na=False)]
        cr = float(m[RC].values[0]) if len(m)>0 else avg_r
        exp_rows.append({'Country':cty,'Exposure_%':pct,'Country_Risk':round(cr,3),
                         'Weighted_Risk':round(cr*pct/100,4),
                         'Level':'🔴' if cr>0.65 else('🟡' if cr>0.35 else '🟢')})
    exp_df=pd.DataFrame(exp_rows).sort_values('Weighted_Risk',ascending=False)

    bcols=[("#e74c3c" if r>0.65 else "#f39c12" if r>0.35 else "#2ecc71") for r in exp_df['Country_Risk']]
    cc1,cc2=st.columns(2)
    with cc1:
        fig_exp=go.Figure(go.Bar(x=exp_df['Country'],y=exp_df['Weighted_Risk'],
            marker_color=bcols,text=[f"{p:.0f}%" for p in exp_df['Exposure_%']],
            textposition='outside'))
        fig_exp.update_layout(title=f'{ck} Weighted Risk by Country ({selected_year})',
            paper_bgcolor="#12172b",plot_bgcolor="#0d1120",font_color="#e8eaf6",
            height=380,xaxis_tickangle=-35,yaxis=dict(gridcolor="#1e2540"),showlegend=False)
        st.plotly_chart(fig_exp,use_container_width=True)
    with cc2:
        fig_pie=go.Figure(go.Pie(labels=exp_df['Country'],values=exp_df['Exposure_%'],
            marker_colors=bcols,textinfo='label+percent',hole=0.4))
        fig_pie.update_layout(title='Revenue Exposure',
            paper_bgcolor="#12172b",font_color="#e8eaf6",height=380)
        st.plotly_chart(fig_pie,use_container_width=True)

    st.dataframe(exp_df.reset_index(drop=True),use_container_width=True,
        column_config={
            "Exposure_%":st.column_config.ProgressColumn("Exposure %",min_value=0,max_value=100,format="%.1f%%"),
            "Country_Risk":st.column_config.ProgressColumn("Country Risk",min_value=0,max_value=1,format="%.3f"),
        })

    st.markdown("<div class='section-header'>Supply Chain Risk</div>",unsafe_allow_html=True)
    for sc in ci['supply_chain']:
        m  = yr_df[yr_df['Country'].str.contains(sc.split()[0],case=False,na=False)]
        cr = float(m[RC].values[0]) if len(m)>0 else 0.5
        color="#e74c3c" if cr>0.65 else "#f39c12" if cr>0.35 else "#2ecc71"
        bg   ="#1f0f0f" if cr>0.65 else "#1f1a0f" if cr>0.35 else "#0f1f0f"
        label="HIGH RISK" if cr>0.65 else "MODERATE" if cr>0.35 else "STABLE"
        st.markdown(f"""
        <div style='background:{bg};border:1px solid {color};border-radius:8px;
                    padding:10px 16px;margin:4px 0;display:flex;
                    justify-content:space-between;align-items:center'>
            <span style='color:#ccd6f6;font-weight:500'>🏭 {sc}</span>
            <span style='color:{color};font-weight:600'>{label} — {cr:.3f}</span>
        </div>""", unsafe_allow_html=True)

# ════════ TAB 4 — RISK MAP ════════════════════════════════════════
with t4:
    st.markdown("<div class='section-header'>🗺️ Global Risk Map</div>",unsafe_allow_html=True)
    fig_map=px.choropleth(yr_df,locations="Country",locationmode="country names",
        color=RC,hover_name="Country",hover_data={RC:":.3f"},
        color_continuous_scale="RdYlGn_r",range_color=[0,1],
        title=f"Predicted Geopolitical Risk — {selected_year} {'🔮' if is_fc else ''}")
    fig_map.update_layout(paper_bgcolor="#0a0e1a",plot_bgcolor="#0a0e1a",
        font_color="#e8eaf6",height=500,
        geo=dict(bgcolor="#0a0e1a",showframe=False,showcoastlines=True,
                 coastlinecolor="#2a3050",landcolor="#12172b",
                 showocean=True,oceancolor="#0a0e1a"),
        coloraxis_colorbar=dict(title="Risk",tickfont=dict(color="#e8eaf6"),
                                title_font=dict(color="#e8eaf6")))
    st.plotly_chart(fig_map,use_container_width=True)

    st.dataframe(yr_df[['Country',RC]].rename(columns={RC:'Risk Score'})
                 .sort_values('Risk Score',ascending=False)
                 .assign(**{'Risk Score':lambda d:d['Risk Score'].round(3)})
                 .reset_index(drop=True),use_container_width=True,height=350,
                 column_config={"Risk Score":st.column_config.ProgressColumn(
                     "Risk Score",min_value=0,max_value=1,format="%.3f")})

# ════════ TAB 5 — ALLOCATION ══════════════════════════════════════
with t5:
    st.markdown("<div class='section-header'>📊 Investment Allocation</div>",unsafe_allow_html=True)
    adf=yr_df.copy()
    for col in ['GDP_growth','HighTech_exports','FDI','Internet_users']:
        adf[col]=adf[col].fillna(adf[col].median())
    adf['opp'] =(0.40*safe_norm(adf['GDP_growth'])+0.25*safe_norm(adf['HighTech_exports'])+
                 0.20*safe_norm(adf['FDI'])+0.15*safe_norm(adf['Internet_users']))
    adf['alloc']=adf['opp']*(1-adf[RC])
    top15=adf.nlargest(15,'alloc').copy()
    tot=top15['alloc'].sum()
    top15['alloc_%']=(top15['alloc']/tot*100).round(2) if tot>0 else 0
    bc2=[("#2ecc71" if r<0.35 else "#f39c12" if r<0.65 else "#e74c3c") for r in top15[RC]]

    cb,cp=st.columns(2)
    with cb:
        fb=go.Figure(go.Bar(x=top15['Country'],y=top15['alloc_%'],marker_color=bc2,
            text=[f"{v:.1f}%" for v in top15['alloc_%']],textposition='outside'))
        fb.update_layout(title=f"Allocation — {selected_year}",
            paper_bgcolor="#12172b",plot_bgcolor="#0d1120",font_color="#e8eaf6",
            xaxis_tickangle=-35,yaxis_title="Allocation %",height=420,showlegend=False,
            yaxis=dict(gridcolor="#1e2540"))
        st.plotly_chart(fb,use_container_width=True)
    with cp:
        fp=go.Figure(go.Pie(labels=top15['Country'],values=top15['alloc_%'],
            marker_colors=bc2,hole=0.4,textinfo='label+percent'))
        fp.update_layout(title="Portfolio",paper_bgcolor="#12172b",font_color="#e8eaf6",height=420)
        st.plotly_chart(fp,use_container_width=True)

    st.dataframe(top15[['Country','alloc_%',RC,'opp']].rename(
        columns={'alloc_%':'Alloc %',RC:'Risk','opp':'Opportunity'}).round(3).reset_index(drop=True),
        use_container_width=True,
        column_config={
            "Alloc %":st.column_config.ProgressColumn("Alloc %",min_value=0,max_value=100,format="%.1f%%"),
            "Risk":st.column_config.ProgressColumn("Risk",min_value=0,max_value=1,format="%.3f"),
        })
    st.download_button("📥 Download Allocation CSV",
        data=top15[['Country','alloc_%',RC]].to_csv(index=False),
        file_name=f"allocation_{selected_year}.csv",mime="text/csv",use_container_width=True)

# ════════ TAB 6 — SCENARIOS ═══════════════════════════════════════
with t6:
    st.markdown("<div class='section-header'>⚡ Scenario Simulation</div>",unsafe_allow_html=True)
    st.markdown("*Use sidebar sliders → Apply Scenario*")

    sc_ov={}
    if apply_sc and not reset_sc:
        ov={}
        if sh_conf>0: ov['conflict_count']=sh_conf
        if sh_dead>0: ov['total_deaths']  =sh_dead
        if sh_gdp!=0.5: ov['GDP_growth']  =sh_gdp
        if sh_inf>0:  ov['Inflation']     =sh_inf
        if sh_imp>0:  ov['Imports_%GDP']  =sh_imp
        if sh_exp>0:  ov['Exports_%GDP']  =sh_exp
        if ov: sc_ov={sc_country:ov}

    sc_rows=[]
    for c in (sel_countries if sel_countries else all_countries[:6]):
        mb=(df['Country']==c)&(df['Year']==selected_year)
        br=float(df[mb][RC].mean()) if mb.any() else 0.0
        sr=min(br+sum(sc_ov.get(c,{}).values())*0.1,1.0) if sc_ov and c==sc_country else br
        sc_rows.append({'Country':c,'Base Risk':round(br,4),'Shocked Risk':round(sr,4),
            'Delta':round(sr-br,4),
            'Direction':"⬆ WORSE" if sr-br>0.01 else("⬇ BETTER" if sr-br<-0.01 else "➡ STABLE")})
    sc_df=pd.DataFrame(sc_rows)

    if sc_ov:
        c0=list(sc_ov.keys())[0]
        d =float(sc_df[sc_df['Country']==c0]['Delta'].values[0]) if c0 in sc_df['Country'].values else 0
        cls="alert-high" if d>0.05 else "alert-medium" if d>0 else "alert-low"
        st.markdown(f"<div class='{cls}'><strong>⚡ SCENARIO — {c0}</strong> &nbsp; Delta: <strong>{d:+.3f}</strong></div>",
                    unsafe_allow_html=True)

    fsc=go.Figure()
    fsc.add_trace(go.Bar(x=sc_df['Country'],y=sc_df['Base Risk'],name='Base Risk',
        marker_color='#3498db',opacity=0.85))
    fsc.add_trace(go.Bar(x=sc_df['Country'],y=sc_df['Shocked Risk'],name='Shocked Risk',
        marker_color='#e74c3c',opacity=0.85))
    fsc.update_layout(barmode='group',title='Base vs Shocked Risk',
        paper_bgcolor="#12172b",plot_bgcolor="#0d1120",font_color="#e8eaf6",
        height=420,yaxis=dict(range=[0,1],gridcolor="#1e2540"),
        legend=dict(bgcolor="#12172b"))
    st.plotly_chart(fsc,use_container_width=True)
    st.dataframe(sc_df.reset_index(drop=True),use_container_width=True)

# ════════ TAB 7 — STRATEGIC ADVICE ═══════════════════════════════
with t7:
    st.markdown(f"<div class='section-header'>💡 Strategic Advice for {ck} — {selected_year}</div>",
                unsafe_allow_html=True)

    risky,safe_list=[],[]
    for cty,pct in exp.items():
        if cty=='Other': continue
        m  =yr_df[yr_df['Country'].str.contains(cty.split()[0],case=False,na=False)]
        cr =float(m[RC].values[0]) if len(m)>0 else 0.5
        if cr>0.55: risky.append((cty,pct,cr))
        elif cr<0.35: safe_list.append((cty,pct,cr))

    comp_label="HIGH" if comp_risk>0.65 else "MODERATE" if comp_risk>0.35 else "LOW"
    st.markdown(f"""
    <div style='background:#12172b;border:2px solid {comp_color};border-radius:14px;
                padding:20px 24px;margin-bottom:20px'>
        <div style='font-size:1.1rem;font-weight:700;color:{comp_color}'>
            {ck} Overall Risk: {comp_risk:.3f} — {comp_label}
        </div>
        <div style='color:#8892b0;font-size:0.85rem;margin-top:6px'>
            Weighted across {len(exp)} regions | {selected_year} {'🔮 Forecast' if is_fc else '📊 Historical'}
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("#### 📌 Specific Recommendations")
    for cty,pct,cr in sorted(risky,key=lambda x:-x[2]):
        trend_df=df[df['Country'].str.contains(cty.split()[0],case=False,na=False)][['Year',RC]].sort_values('Year').tail(3)
        td="" if len(trend_df)<2 else ("↗ Rising" if trend_df[RC].iloc[-1]-trend_df[RC].iloc[-2]>0.02 else
                                       "↘ Falling" if trend_df[RC].iloc[-1]-trend_df[RC].iloc[-2]<-0.02 else "→ Stable")
        st.markdown(f"""
        <div class='alert-high'>
            <strong>⚠️ REDUCE EXPOSURE — {cty}</strong>
            <span style='font-size:0.8rem'> ({pct:.0f}% revenue | Risk: {cr:.3f} {td})</span><br>
            <span style='font-size:0.9rem'>
            Reduce {cty} exposure from {pct:.0f}% toward {max(pct-10,5):.0f}% over 2 years.
            {'Conflict risks are rising — act proactively.' if cr>0.65 else 'Monitor quarterly and prepare contingency plans.'}
            </span>
        </div>""", unsafe_allow_html=True)

    for cty,pct,cr in sorted(safe_list,key=lambda x:x[2])[:3]:
        st.markdown(f"""
        <div class='alert-low'>
            <strong>✅ INCREASE ALLOCATION — {cty}</strong>
            <span style='font-size:0.8rem'> ({pct:.0f}% current | Risk: {cr:.3f})</span><br>
            <span style='font-size:0.9rem'>
            Stable geopolitical conditions. Consider expanding {cty} from {pct:.0f}% toward {min(pct+8,40):.0f}%.
            </span>
        </div>""", unsafe_allow_html=True)

    if len([y for y in all_years if y>=2025])>0:
        st.markdown("#### 📈 5-Year Outlook (2025–2029)")
        for cty,pct in list(exp.items())[:5]:
            if cty=='Other': continue
            ft2=df[(df['Country'].str.contains(cty.split()[0],case=False,na=False))&
                   (df['data_type']=='forecast')][['Year',RC]].sort_values('Year')
            if len(ft2)<2: continue
            mn,mx2=ft2[RC].min(),ft2[RC].max()
            d2=ft2[RC].iloc[-1]-ft2[RC].iloc[0]
            tw="DETERIORATING ⬆" if d2>0.05 else("IMPROVING ⬇" if d2<-0.05 else "STABLE →")
            tc="#e74c3c" if "DET" in tw else "#2ecc71" if "IMP" in tw else "#f39c12"
            st.markdown(f"""
            <div style='background:#12172b;border:1px solid #2a3050;border-radius:8px;
                        padding:10px 16px;margin:4px 0;display:flex;
                        justify-content:space-between;align-items:center'>
                <span style='color:#ccd6f6'><strong>{cty}</strong>
                    <span style='color:#6272a4;font-size:0.8rem'> ({pct:.0f}% exposure)</span>
                </span>
                <span>
                    <span style='color:#8892b0;font-size:0.8rem'>Range: {mn:.2f}–{mx2:.2f}</span>
                    &nbsp;<span style='color:{tc};font-weight:600;font-size:0.85rem'>{tw}</span>
                </span>
            </div>""", unsafe_allow_html=True)

    adv=pd.DataFrame(
        [{'Company':ck,'Year':selected_year,'Country':c,'Exposure_%':p,
          'Risk':r,'Action':'REDUCE'} for c,p,r in risky]+
        [{'Company':ck,'Year':selected_year,'Country':c,'Exposure_%':p,
          'Risk':r,'Action':'INCREASE'} for c,p,r in safe_list])
    if len(adv)>0:
        st.markdown("<br>")
        st.download_button("📥 Download Strategic Advice CSV",
            data=adv.to_csv(index=False),
            file_name=f"{ck}_advice_{selected_year}.csv",
            mime="text/csv",use_container_width=True)

# ── FOOTER ────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(f"""
<p style='text-align:center;color:#2a3050;font-size:0.75rem'>
RiskMap AI Intelligence Platform &nbsp;|&nbsp; {ck} Dashboard &nbsp;|&nbsp;
Data: World Bank + UCDP &nbsp;|&nbsp; Model: Gradient Boosting t+1 Forecasting &nbsp;|&nbsp;
Forecast: 2025–2029 via ARIMA &nbsp;|&nbsp; Built with Streamlit + Plotly
</p>""", unsafe_allow_html=True)
