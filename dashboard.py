import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="Nuxeo Operations Center",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown('<meta http-equiv="refresh" content="60">', unsafe_allow_html=True)

# ============================================
# CSS — Liner-inspired clean design
# ============================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.stApp {
    background: #F0F4FA;
}
.block-container {
    padding: 1.5rem 2.5rem !important;
    max-width: 1600px;
}

/* ── HEADER ── */
.nux-header {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 24px 32px;
    margin-bottom: 24px;
    border: 1px solid #E2E8F4;
    box-shadow: 0 2px 12px rgba(15,40,90,0.06);
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.nux-header-left { display: flex; align-items: center; gap: 16px; }
.nux-logo {
    width: 46px; height: 46px;
    background: linear-gradient(135deg, #2563EB, #1D4ED8);
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; color: white; font-weight: 800;
    box-shadow: 0 4px 14px rgba(37,99,235,0.35);
}
.nux-title { font-size: 22px; font-weight: 800; color: #0F172A; margin: 0; }
.nux-subtitle { font-size: 13px; color: #64748B; margin: 0; }
.nux-time {
    background: #F1F5F9;
    color: #475569;
    font-size: 12px;
    font-weight: 600;
    padding: 8px 16px;
    border-radius: 10px;
    border: 1px solid #E2E8F0;
}

/* ── SECTION HEADERS ── */
.sec-title {
    font-size: 17px;
    font-weight: 700;
    color: #0F172A;
    margin: 28px 0 14px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}
.sec-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #E2E8F0;
    margin-left: 8px;
}

/* ── KPI CARDS ── */
.kpi-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 14px; margin-bottom: 4px; }
.kpi-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 2px 8px rgba(15,40,90,0.05);
    transition: transform 0.15s, box-shadow 0.15s;
}
.kpi-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(15,40,90,0.1); }
.kpi-icon { font-size: 22px; margin-bottom: 10px; }
.kpi-label { font-size: 11px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.8px; }
.kpi-val { font-size: 32px; font-weight: 800; color: #0F172A; line-height: 1.1; margin: 4px 0; }
.kpi-meta { font-size: 12px; color: #64748B; font-weight: 500; }
.kpi-red .kpi-val { color: #DC2626; }
.kpi-amber .kpi-val { color: #D97706; }
.kpi-green .kpi-val { color: #16A34A; }
.kpi-blue .kpi-val { color: #2563EB; }
.kpi-red { border-top: 3px solid #DC2626; }
.kpi-amber { border-top: 3px solid #F59E0B; }
.kpi-green { border-top: 3px solid #16A34A; }
.kpi-blue { border-top: 3px solid #2563EB; }

/* ── ALERT BANNERS ── */
.alert-critical {
    background: #FEF2F2;
    border: 1.5px solid #FECACA;
    border-left: 5px solid #DC2626;
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 10px;
}
.alert-critical .alert-title { font-size: 14px; font-weight: 700; color: #991B1B; margin: 0 0 4px 0; }
.alert-critical .alert-body { font-size: 13px; color: #7F1D1D; margin: 0; }
.alert-warning {
    background: #FFFBEB;
    border: 1.5px solid #FDE68A;
    border-left: 5px solid #F59E0B;
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 10px;
}
.alert-warning .alert-title { font-size: 14px; font-weight: 700; color: #92400E; margin: 0 0 4px 0; }
.alert-warning .alert-body { font-size: 13px; color: #78350F; margin: 0; }

/* ── TAB STAT ROWS ── */
.tab-row {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 14px 18px;
    margin-bottom: 8px;
    border: 1px solid #E2E8F0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transition: box-shadow 0.15s;
}
.tab-row:hover { box-shadow: 0 4px 14px rgba(15,40,90,0.08); }
.tab-row-name { font-size: 14px; font-weight: 700; color: #0F172A; }
.tab-row-sub { font-size: 12px; color: #64748B; margin-top: 2px; }
.badges { display: flex; gap: 8px; }
.badge {
    font-size: 12px; font-weight: 700;
    padding: 4px 12px; border-radius: 20px;
}
.badge-blue { background: #EFF6FF; color: #1D4ED8; }
.badge-green { background: #F0FDF4; color: #15803D; }
.badge-red { background: #FEF2F2; color: #B91C1C; }

/* ── DEADLINE TABLE HEADERS ── */
.tbl-header-red {
    background: #FEF2F2;
    border: 1px solid #FECACA;
    border-radius: 12px;
    padding: 12px 18px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.tbl-header-red span { font-size: 14px; font-weight: 700; color: #991B1B; }
.tbl-header-amber {
    background: #FFFBEB;
    border: 1px solid #FDE68A;
    border-radius: 12px;
    padding: 12px 18px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.tbl-header-amber span { font-size: 14px; font-weight: 700; color: #92400E; }

/* ── DOWNLOAD BUTTON OVERRIDE ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    padding: 8px 20px !important;
    box-shadow: 0 3px 10px rgba(37,99,235,0.3) !important;
}
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #1D4ED8, #1E40AF) !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.45) !important;
}

/* ── SELECTBOX / RADIO ── */
div[role="radiogroup"] {
    background: white;
    padding: 8px 12px;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
    gap: 4px;
}
.stSelectbox > div > div {
    background: white !important;
    border-radius: 10px !important;
    border: 1px solid #E2E8F0 !important;
    color: #0F172A !important;
}

/* ── DATAFRAME ── */
.stDataFrame {
    border-radius: 14px !important;
    border: 1px solid #E2E8F0 !important;
    overflow: hidden;
}
iframe { border-radius: 14px !important; }

/* ── INFO / SUCCESS ── */
.stAlert { border-radius: 12px !important; }
.stSuccess { background: #F0FDF4 !important; color: #14532D !important; border-color: #BBF7D0 !important; }
.stInfo { background: #EFF6FF !important; color: #000000 !important; border-color: #BFDBFE !important; }
.stInfo p, .stInfo span, div[data-testid="stNotification"] p { color: #000000 !important; }

/* ── RADIO BUTTON LABELS BLACK ── */
div[role="radiogroup"] label p,
div[role="radiogroup"] label span,
div[role="radiogroup"] label { color: #000000 !important; font-weight: 600 !important; }

/* ── UPCOMING DEADLINES SECTION BOLD HEADERS BLACK ── */
.stMarkdown strong { color: #000000 !important; }

/* ── PLOTLY WRAPPER ── */
.js-plotly-plot { border-radius: 14px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ============================================
# EXCEL HELPER
# ============================================

def to_excel(df: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Ads")
    return output.getvalue()

# ============================================
# LOAD DATA
# ============================================

@st.cache_data(ttl=60)
def load_data():
    conn = sqlite3.connect("nuxeo_ads.db")
    df = pd.read_sql("SELECT * FROM ads", conn)
    conn.close()
    return df

try:
    raw_df = load_data()
except Exception as e:
    st.error(f"⚠️ Database error: {e}")
    st.stop()

# ============================================
# CLEAN DATA
# ============================================

df = raw_df[raw_df["Ad"].str.match(r'^(SFAD_|CL)\d+$', na=False)].copy()

if df.empty:
    st.warning("No valid ad data found in database.")
    st.stop()

df["Scan Time DT"] = pd.to_datetime(df["Scan Time"], errors="coerce")
df["Due Out Parsed"] = pd.to_datetime(df["Due Out Deadline"], format="%m/%d/%Y %I:%M:%S %p", errors="coerce")
df["Art Parsed"] = pd.to_datetime(df["Art Deadline"], format="%m/%d/%Y %I:%M:%S %p", errors="coerce")
df["Claimed By"] = df["Claimed By"].fillna("").str.strip()
df["Scan Date"] = df["Scan Time DT"].dt.date

now = datetime.now()
today = now.date()

# ── Latest state per Ad+Tab ──
latest_df = df.drop_duplicates(subset=["Ad", "Tab"], keep="last").copy()
latest_df = latest_df.loc[:, ~latest_df.columns.duplicated()]

# ── Moved ads detection ──
all_scan_times = df["Scan Time DT"].dropna().sort_values()
if len(all_scan_times) > 0:
    latest_scan_end = all_scan_times.max()
    latest_scan_start = latest_scan_end - timedelta(minutes=10)
    latest_batch_ids = set(df[df["Scan Time DT"] >= latest_scan_start]["Ad"].unique())
    prev_batch_ids = set(df[df["Scan Time DT"] < latest_scan_start]["Ad"].unique())
    moved_out_ids = prev_batch_ids - latest_batch_ids
    moved_out_df = df[df["Ad"].isin(moved_out_ids)].drop_duplicates(subset=["Ad"], keep="last")
else:
    moved_out_df = pd.DataFrame()
    latest_batch_ids = set()

today_df = latest_df[latest_df["Scan Date"] == today].copy()

next_10m = now + timedelta(minutes=10)
next_30m = now + timedelta(minutes=30)

due_out_delayed = latest_df[latest_df["Due Out Parsed"] < now].copy()
art_delayed = latest_df[latest_df["Art Parsed"] < now].copy()
critical_due_out = latest_df[(latest_df["Due Out Parsed"] >= now) & (latest_df["Due Out Parsed"] <= next_10m)].copy()
critical_art = latest_df[(latest_df["Art Parsed"] >= now) & (latest_df["Art Parsed"] <= next_10m)].copy()
upcoming_due_out = latest_df[(latest_df["Due Out Parsed"] > next_10m) & (latest_df["Due Out Parsed"] <= next_30m)].copy()
upcoming_art = latest_df[(latest_df["Art Parsed"] > next_10m) & (latest_df["Art Parsed"] <= next_30m)].copy()

if not moved_out_df.empty:
    moved_after_due_deadline = moved_out_df[moved_out_df["Due Out Parsed"] < now].copy()
    moved_after_art_deadline = moved_out_df[moved_out_df["Art Parsed"] < now].copy()
else:
    moved_after_due_deadline = pd.DataFrame()
    moved_after_art_deadline = pd.DataFrame()

# ============================================
# HEADER
# ============================================

st.markdown(f"""
<div class="nux-header">
    <div class="nux-header-left">
        <div class="nux-logo">N</div>
        <div>
            <p class="nux-title">Nuxeo Operations Center</p>
            <p class="nux-subtitle">Real-time ad workflow monitoring · alerts · workload tracking</p>
        </div>
    </div>
    <div class="nux-time">🔄 Last updated: {now.strftime('%B %d, %Y  %I:%M:%S %p')}</div>
</div>
""", unsafe_allow_html=True)

# ============================================
# LIVE ALERTS
# ============================================

has_alerts = any([len(critical_due_out), len(critical_art), len(upcoming_due_out), len(upcoming_art)])

if has_alerts:
    st.markdown('<div class="sec-title">🚨 Live Deadline Alerts</div>', unsafe_allow_html=True)
    ac1, ac2 = st.columns(2)
    with ac1:
        if len(critical_due_out):
            ads = ", ".join(critical_due_out["Ad"].head(5).tolist())
            st.markdown(f"""<div class="alert-critical">
                <p class="alert-title">🔴 CRITICAL — Due Out in &lt;10 min ({len(critical_due_out)} ads)</p>
                <p class="alert-body">{ads}{'…' if len(critical_due_out) > 5 else ''}</p>
            </div>""", unsafe_allow_html=True)
        if len(upcoming_due_out):
            ads = ", ".join(upcoming_due_out["Ad"].head(5).tolist())
            st.markdown(f"""<div class="alert-warning">
                <p class="alert-title">⚠️ Due Out within 30 min ({len(upcoming_due_out)} ads)</p>
                <p class="alert-body">{ads}{'…' if len(upcoming_due_out) > 5 else ''}</p>
            </div>""", unsafe_allow_html=True)
    with ac2:
        if len(critical_art):
            ads = ", ".join(critical_art["Ad"].head(5).tolist())
            st.markdown(f"""<div class="alert-critical">
                <p class="alert-title">🔴 CRITICAL — Art Deadline in &lt;10 min ({len(critical_art)} ads)</p>
                <p class="alert-body">{ads}{'…' if len(critical_art) > 5 else ''}</p>
            </div>""", unsafe_allow_html=True)
        if len(upcoming_art):
            ads = ", ".join(upcoming_art["Ad"].head(5).tolist())
            st.markdown(f"""<div class="alert-warning">
                <p class="alert-title">⚠️ Art Deadline within 30 min ({len(upcoming_art)} ads)</p>
                <p class="alert-body">{ads}{'…' if len(upcoming_art) > 5 else ''}</p>
            </div>""", unsafe_allow_html=True)

# ============================================
# KPI CARDS
# ============================================

st.markdown('<div class="sec-title">📈 Summary KPIs</div>', unsafe_allow_html=True)

total_critical = len(critical_due_out) + len(critical_art)
claimed_count = len(latest_df[latest_df["Claimed By"] != ""])

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card kpi-blue">
        <div class="kpi-icon">📋</div>
        <div class="kpi-label">Total Ads Live</div>
        <div class="kpi-val kpi-blue">{len(latest_df)}</div>
        <div class="kpi-meta">Across all tabs</div>
    </div>
    <div class="kpi-card kpi-green">
        <div class="kpi-icon">✅</div>
        <div class="kpi-label">Moved Out</div>
        <div class="kpi-val kpi-green">{len(moved_out_df)}</div>
        <div class="kpi-meta">Cleared from queue</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">👤</div>
        <div class="kpi-label">Claimed Ads</div>
        <div class="kpi-val">{claimed_count}</div>
        <div class="kpi-meta">Currently assigned</div>
    </div>
    <div class="kpi-card kpi-red">
        <div class="kpi-icon">⏱️</div>
        <div class="kpi-label">Due Out Delayed</div>
        <div class="kpi-val kpi-red">{len(due_out_delayed)}</div>
        <div class="kpi-meta">Past due out deadline</div>
    </div>
    <div class="kpi-card kpi-amber">
        <div class="kpi-icon">🎨</div>
        <div class="kpi-label">Art Delayed</div>
        <div class="kpi-val kpi-amber">{len(art_delayed)}</div>
        <div class="kpi-meta">Past art deadline</div>
    </div>
    <div class="kpi-card kpi-red">
        <div class="kpi-icon">⚡</div>
        <div class="kpi-label">Critical (10 min)</div>
        <div class="kpi-val kpi-red">{total_critical}</div>
        <div class="kpi-meta">Hitting deadline soon</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# PER-TAB BREAKDOWN
# ============================================

st.markdown('<div class="sec-title">🗂️ Per-Tab Breakdown</div>', unsafe_allow_html=True)

TAB_NAMES = [
    "Materials Review", "Menu Typing", "PreMedia",
    "Design", "In Progress Ads", "In House Change", "Quality Control"
]

tab_cols = st.columns(2)
for idx, tab_name in enumerate(TAB_NAMES):
    tab_df = latest_df[latest_df["Tab"] == tab_name]
    tab_moved = moved_out_df[moved_out_df["Tab"] == tab_name] if not moved_out_df.empty else pd.DataFrame()
    tab_delayed_due = tab_df[tab_df["Due Out Parsed"] < now]
    tab_delayed_art = tab_df[tab_df["Art Parsed"] < now]
    tab_claimed = tab_df[tab_df["Claimed By"] != ""]
    with tab_cols[idx % 2]:
        st.markdown(f"""
        <div class="tab-row">
            <div>
                <div class="tab-row-name">📁 {tab_name}</div>
                <div class="tab-row-sub">{len(tab_claimed)} claimed &nbsp;·&nbsp; {len(tab_delayed_due)} due delayed &nbsp;·&nbsp; {len(tab_delayed_art)} art delayed</div>
            </div>
            <div class="badges">
                <span class="badge badge-blue">📥 {len(tab_df)} ads</span>
                <span class="badge badge-green">📤 {len(tab_moved)} moved</span>
                <span class="badge badge-red">⏰ {len(tab_delayed_due) + len(tab_delayed_art)} delayed</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Per-tab chart
tab_summary = latest_df.groupby("Tab").size().reset_index(name="Total Ads")
tab_delayed_counts = latest_df[latest_df["Due Out Parsed"] < now].groupby("Tab").size().reset_index(name="Delayed")
tab_summary = tab_summary.merge(tab_delayed_counts, on="Tab", how="left").fillna(0)

fig_tab = go.Figure()
fig_tab.add_trace(go.Bar(
    name="Total Ads", x=tab_summary["Tab"], y=tab_summary["Total Ads"],
    marker_color="#3B82F6", text=tab_summary["Total Ads"],
    textposition="auto", textfont=dict(color="white", size=12)
))
fig_tab.add_trace(go.Bar(
    name="Due Out Delayed", x=tab_summary["Tab"], y=tab_summary["Delayed"],
    marker_color="#EF4444", text=tab_summary["Delayed"].astype(int),
    textposition="auto", textfont=dict(color="white", size=12)
))
fig_tab.update_layout(
    barmode="group",
    plot_bgcolor="#FAFBFE", paper_bgcolor="white",
    font=dict(family="Plus Jakarta Sans", color="#0F172A"),
    height=320,
    margin=dict(t=10, b=40, l=10, r=10),
    legend=dict(
        orientation="h", yanchor="bottom", y=1.02,
        xanchor="right", x=1,
        font=dict(size=12, color="#374151")
    ),
    xaxis=dict(tickfont=dict(size=11, color="#374151"), gridcolor="#F1F5F9"),
    yaxis=dict(tickfont=dict(size=11, color="#374151"), gridcolor="#F1F5F9"),
)
st.plotly_chart(fig_tab, use_container_width=True)

# ============================================
# CRITICAL DEADLINE MONITORING
# ============================================

st.markdown('<div class="sec-title">⏰ Critical Deadline Monitoring</div>', unsafe_allow_html=True)

d1, d2 = st.columns(2)

with d1:
    st.markdown("""<div class="tbl-header-red"><span>🔴 Due Out — Delayed Ads</span></div>""", unsafe_allow_html=True)
    if len(due_out_delayed) > 0:
        dcols = [c for c in ["Ad", "Advertiser", "Claimed By", "Tab", "Due Out Deadline"] if c in due_out_delayed.columns]
        st.dataframe(due_out_delayed[dcols], use_container_width=True, height=280)
        st.download_button(
            "⬇️ Download as Excel",
            data=to_excel(due_out_delayed[dcols]),
            file_name=f"due_out_delayed_{today}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="dl_due_delayed"
        )
    else:
        st.success("✅ No due out delays!")

with d2:
    st.markdown("""<div class="tbl-header-amber"><span>🟠 Art Deadline — Delayed Ads</span></div>""", unsafe_allow_html=True)
    if len(art_delayed) > 0:
        acols = [c for c in ["Ad", "Advertiser", "Claimed By", "Tab", "Art Deadline"] if c in art_delayed.columns]
        st.dataframe(art_delayed[acols], use_container_width=True, height=280)
        st.download_button(
            "⬇️ Download as Excel",
            data=to_excel(art_delayed[acols]),
            file_name=f"art_delayed_{today}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="dl_art_delayed"
        )
    else:
        st.success("✅ No art deadline delays!")

# ============================================
# UPCOMING DEADLINES
# ============================================

st.markdown('<div class="sec-title">🔔 Upcoming Deadlines — Next 30 Minutes</div>', unsafe_allow_html=True)

u1, u2 = st.columns(2)

with u1:
    st.markdown("**Due Out**")
    upcoming_all_due = pd.concat([critical_due_out, upcoming_due_out], ignore_index=True) if len(critical_due_out) + len(upcoming_due_out) > 0 else pd.DataFrame()
    if len(upcoming_all_due) > 0:
        upcoming_all_due["Mins Left"] = ((upcoming_all_due["Due Out Parsed"] - now).dt.total_seconds() / 60).round(1)
        ucols = [c for c in ["Ad", "Advertiser", "Tab", "Mins Left", "Due Out Deadline"] if c in upcoming_all_due.columns]
        st.dataframe(upcoming_all_due[ucols].sort_values("Mins Left"), use_container_width=True, height=230)
        st.download_button(
            "⬇️ Download as Excel",
            data=to_excel(upcoming_all_due[ucols].sort_values("Mins Left")),
            file_name=f"upcoming_due_out_{today}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="dl_upcoming_due"
        )
    else:
        st.info("No due out deadlines in the next 30 minutes.")

with u2:
    st.markdown("**Art Deadline**")
    upcoming_all_art = pd.concat([critical_art, upcoming_art], ignore_index=True) if len(critical_art) + len(upcoming_art) > 0 else pd.DataFrame()
    if len(upcoming_all_art) > 0:
        upcoming_all_art["Mins Left"] = ((upcoming_all_art["Art Parsed"] - now).dt.total_seconds() / 60).round(1)
        uacols = [c for c in ["Ad", "Advertiser", "Tab", "Mins Left", "Art Deadline"] if c in upcoming_all_art.columns]
        st.dataframe(upcoming_all_art[uacols].sort_values("Mins Left"), use_container_width=True, height=230)
        st.download_button(
            "⬇️ Download as Excel",
            data=to_excel(upcoming_all_art[uacols].sort_values("Mins Left")),
            file_name=f"upcoming_art_{today}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="dl_upcoming_art"
        )
    else:
        st.info("No art deadlines in the next 30 minutes.")

# ============================================
# DAILY DEADLINE REPORT (with per-date Excel)
# ============================================

st.markdown('<div class="sec-title">📅 Daily Deadline Report</div>', unsafe_allow_html=True)

day_col, _ = st.columns([2, 4])
with day_col:
    available_dates = sorted(df["Scan Date"].dropna().unique(), reverse=True)
    selected_date = st.selectbox(
        "Select Date",
        available_dates,
        format_func=lambda d: d.strftime("%B %d, %Y") if hasattr(d, "strftime") else str(d)
    )

day_df = df[df["Scan Date"] == selected_date].copy()

dd1, dd2 = st.columns(2)

with dd1:
    st.markdown("**Due Out — Ads Past Deadline**")
    day_due_delayed = day_df[
        day_df["Due Out Parsed"].notna() &
        (day_df["Due Out Parsed"] < pd.Timestamp(selected_date) + pd.Timedelta(days=1))
    ].drop_duplicates("Ad")
    if len(day_due_delayed) > 0:
        dcols = [c for c in ["Ad", "Advertiser", "Claimed By", "Tab", "Due Out Deadline"] if c in day_due_delayed.columns]
        st.dataframe(day_due_delayed[dcols], use_container_width=True, height=280)
        st.download_button(
            f"⬇️ Download {selected_date} Due Out Excel",
            data=to_excel(day_due_delayed[dcols]),
            file_name=f"due_out_delayed_{selected_date}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"dl_day_due_{selected_date}"
        )
    else:
        st.info("No due out delays for this date.")

with dd2:
    st.markdown("**Art Deadline — Ads Past Deadline**")
    day_art_delayed = day_df[
        day_df["Art Parsed"].notna() &
        (day_df["Art Parsed"] < pd.Timestamp(selected_date) + pd.Timedelta(days=1))
    ].drop_duplicates("Ad")
    if len(day_art_delayed) > 0:
        acols = [c for c in ["Ad", "Advertiser", "Claimed By", "Tab", "Art Deadline"] if c in day_art_delayed.columns]
        st.dataframe(day_art_delayed[acols], use_container_width=True, height=280)
        st.download_button(
            f"⬇️ Download {selected_date} Art Deadline Excel",
            data=to_excel(day_art_delayed[acols]),
            file_name=f"art_delayed_{selected_date}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"dl_day_art_{selected_date}"
        )
    else:
        st.info("No art deadline delays for this date.")

# ============================================
# MOVED AFTER DEADLINE
# ============================================

if not moved_out_df.empty:
    st.markdown('<div class="sec-title">📤 Ads Moved After Deadline</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748B; font-size:13px; margin-bottom:14px;">These ads were cleared from the queue after their deadline had passed.</p>', unsafe_allow_html=True)

    mad1, mad2 = st.columns(2)

    with mad1:
        st.markdown("**Moved After Due Out Deadline**")
        if len(moved_after_due_deadline) > 0:
            mc = [c for c in ["Ad", "Advertiser", "Tab", "Claimed By", "Due Out Deadline"] if c in moved_after_due_deadline.columns]
            st.dataframe(moved_after_due_deadline[mc], use_container_width=True, height=260)
            st.download_button(
                "⬇️ Download as Excel",
                data=to_excel(moved_after_due_deadline[mc]),
                file_name=f"moved_after_due_{today}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="dl_mad_due"
            )
        else:
            st.success("✅ All due out moves were on time!")

    with mad2:
        st.markdown("**Moved After Art Deadline**")
        if len(moved_after_art_deadline) > 0:
            mc = [c for c in ["Ad", "Advertiser", "Tab", "Claimed By", "Art Deadline"] if c in moved_after_art_deadline.columns]
            st.dataframe(moved_after_art_deadline[mc], use_container_width=True, height=260)
            st.download_button(
                "⬇️ Download as Excel",
                data=to_excel(moved_after_art_deadline[mc]),
                file_name=f"moved_after_art_{today}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="dl_mad_art"
            )
        else:
            st.success("✅ All art moves were on time!")

# ============================================
# DEPARTMENT FILTER
# ============================================

st.markdown('<div class="sec-title">🔎 Department Filter</div>', unsafe_allow_html=True)

tab_options = ["All"] + sorted(latest_df["Tab"].dropna().unique().tolist())
selected_tab = st.radio("Select Department", tab_options, horizontal=True)

filtered_df = latest_df.copy()
if selected_tab != "All":
    filtered_df = filtered_df[filtered_df["Tab"] == selected_tab]

# ============================================
# USER WORKLOAD
# ============================================

st.markdown('<div class="sec-title">👤 User Workload & Productivity</div>', unsafe_allow_html=True)

user_df = filtered_df[filtered_df["Claimed By"] != ""].copy()

if len(user_df) > 0:
    user_summary = user_df.groupby("Claimed By").agg(
        Current_Ads=("Ad", "count"),
        Tabs_Worked=("Tab", "nunique"),
    ).reset_index()
    user_delayed_due = user_df[user_df["Due Out Parsed"] < now].groupby("Claimed By").size().reset_index(name="Due_Delayed")
    user_delayed_art = user_df[user_df["Art Parsed"] < now].groupby("Claimed By").size().reset_index(name="Art_Delayed")
    user_summary = (user_summary
        .merge(user_delayed_due, on="Claimed By", how="left")
        .merge(user_delayed_art, on="Claimed By", how="left")
        .fillna(0))
    user_summary = user_summary.rename(columns={
        "Claimed By": "User", "Current_Ads": "Current Ads",
        "Tabs_Worked": "Tabs", "Due_Delayed": "Due Delayed", "Art_Delayed": "Art Delayed"
    })
    user_summary[["Due Delayed", "Art Delayed"]] = user_summary[["Due Delayed", "Art Delayed"]].astype(int)
    user_summary = user_summary.sort_values("Current Ads", ascending=False)

    uw1, uw2 = st.columns([1.2, 1.8])

    with uw1:
        st.dataframe(user_summary, use_container_width=True, height=380)
        st.download_button(
            "⬇️ Download User Workload Excel",
            data=to_excel(user_summary),
            file_name=f"user_workload_{today}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="dl_user_workload"
        )

    with uw2:
        fig_user = px.bar(
            user_summary, x="User", y="Current Ads",
            text="Current Ads", color="Due Delayed",
            color_continuous_scale=["#22C55E", "#F59E0B", "#EF4444"],
            title="Current Ad Load per User (color = Due Delayed)"
        )
        fig_user.update_layout(
            plot_bgcolor="#FAFBFE", paper_bgcolor="white",
            font=dict(family="Plus Jakarta Sans", color="#0F172A"),
            title_font=dict(size=14, color="#0F172A"),
            height=360,
            margin=dict(t=40, b=60, l=10, r=10),
            coloraxis_showscale=False,
            xaxis=dict(tickangle=-30, tickfont=dict(size=11, color="#374151")),
            yaxis=dict(tickfont=dict(size=11, color="#374151"), gridcolor="#F1F5F9"),
        )
        st.plotly_chart(fig_user, use_container_width=True)

    st.markdown("**Ads worked by user per department**")
    user_tab_pivot = user_df.groupby(["Claimed By", "Tab"]).size().reset_index(name="Count")
    user_tab_wide = user_tab_pivot.pivot(index="Claimed By", columns="Tab", values="Count").fillna(0).astype(int)
    user_tab_wide["TOTAL"] = user_tab_wide.sum(axis=1)
    user_tab_wide = user_tab_wide.sort_values("TOTAL", ascending=False)
    st.dataframe(user_tab_wide, use_container_width=True, height=320)
    st.download_button(
        "⬇️ Download User-Tab Pivot Excel",
        data=to_excel(user_tab_wide.reset_index()),
        file_name=f"user_tab_pivot_{today}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="dl_user_tab"
    )
else:
    st.info("No claimed ads in the selected department.")

# ============================================
# LIVE ADS QUEUE
# ============================================

st.markdown('<div class="sec-title">📋 Live Ads Queue</div>', unsafe_allow_html=True)

display_live = filtered_df.drop(
    columns=["Due Out Parsed", "Art Parsed", "Scan Time DT", "Scan Date"], errors="ignore"
)
st.dataframe(display_live, use_container_width=True, height=650)

col_dl1, col_dl2 = st.columns([1, 5])
with col_dl1:
    st.download_button(
        "⬇️ Download Queue Excel",
        data=to_excel(filtered_df),
        file_name=f"live_queue_{selected_tab}_{today}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="dl_live_queue"
    )

# ============================================
# FOOTER
# ============================================

st.markdown("""
<div style="text-align:center; padding: 24px 0 12px; color:#94A3B8; font-size:12px; font-weight:500;">
    🔄 Dashboard auto-refreshes every 60 seconds · Nuxeo Operations Center
</div>
""", unsafe_allow_html=True)