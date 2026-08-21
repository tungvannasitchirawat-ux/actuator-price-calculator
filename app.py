import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="DOMINIC vs Rotork vs AUMA Pricing Calculator",
    page_icon="⚡",
    layout="wide"
)

# Title & Header
st.title("⚡ DOMINIC Actuator Price & Competitor Comparison")
st.markdown("ระบบคำนวณและเปรียบเทียบราคาขายในประเทศไทยสำหรับ **DOMINIC**, **ROTORK** และ **AUMA**")

# Sidebar Controls
st.sidebar.header("⚙️ การตั้งค่าราคา (Settings)")
cny_rate = st.sidebar.number_input("อัตราแลกเปลี่ยน (THB/CNY)", value=5.0, step=0.1, format="%.2f")
margin_factor = st.sidebar.number_input("ตัวคูณกำไร (Margin Factor)", value=2.75, step=0.05, format="%.2f")

st.sidebar.markdown("---")
st.sidebar.info(f"**สูตรคำนวณราคาขาย DOMINIC:**\n\n`ราคา THB = ราคา CNY x {cny_rate:.2f} x {margin_factor:.2f}`")

# Raw Data Setup
mt_data = [
    {"Model": "D08", "RPM": 26, "Torque": 105, "ISO": "F10", "RMB_Min": 6800, "RMB_Max": 7010, "Thrust_RMB": 600, "Rotork": "IQ10 / IQ12", "AUMA": "SA 07.2 / 07.6", "Market_Price": "180,000 - 250,000"},
    {"Model": "D10", "RPM": 26, "Torque": 205, "ISO": "F10", "RMB_Min": 7200, "RMB_Max": 7200, "Thrust_RMB": 600, "Rotork": "IQ18", "AUMA": "SA 10.2", "Market_Price": "220,000 - 300,000"},
    {"Model": "D12", "RPM": 26, "Torque": 305, "ISO": "F10", "RMB_Min": 7600, "RMB_Max": 7920, "Thrust_RMB": 600, "Rotork": "IQ20", "AUMA": "SA 14.2", "Market_Price": "250,000 - 350,000"},
    {"Model": "D15", "RPM": 25, "Torque": 455, "ISO": "F14", "RMB_Min": 8900, "RMB_Max": 9250, "Thrust_RMB": 930, "Rotork": "IQ25", "AUMA": "SA 14.2", "Market_Price": "300,000 - 420,000"},
    {"Model": "D20", "RPM": 25, "Torque": 605, "ISO": "F14", "RMB_Min": 9300, "RMB_Max": 9680, "Thrust_RMB": 930, "Rotork": "IQ35", "AUMA": "SA 14.6", "Market_Price": "350,000 - 480,000"},
    {"Model": "D25", "RPM": 18, "Torque": 905, "ISO": "F16", "RMB_Min": 9830, "RMB_Max": 9830, "Thrust_RMB": 2600, "Rotork": "IQ40", "AUMA": "SA 16.2", "Market_Price": "400,000 - 550,000"},
    {"Model": "D30", "RPM": 18, "Torque": 1205, "ISO": "F25", "RMB_Min": 10320, "RMB_Max": 10320, "Thrust_RMB": 2600, "Rotork": "IQ70", "AUMA": "SA 25.1", "Market_Price": "480,000 - 650,000"},
    {"Model": "D40", "RPM": 24, "Torque": 2100, "ISO": "F25", "RMB_Min": 13600, "RMB_Max": 13600, "Thrust_RMB": 3100, "Rotork": "IQ90", "AUMA": "SA 25.1", "Market_Price": "600,000 - 800,000"},
    {"Model": "D45", "RPM": 24, "Torque": 2550, "ISO": "F30", "RMB_Min": 14100, "RMB_Max": 14100, "Thrust_RMB": 3100, "Rotork": "IQ91", "AUMA": "SA 30.1", "Market_Price": "700,000 - 950,000"},
    {"Model": "D50", "RPM": 24, "Torque": 3100, "ISO": "F35", "RMB_Min": 14780, "RMB_Max": 14780, "Thrust_RMB": 3100, "Rotork": "IQ95", "AUMA": "SA 35.1", "Market_Price": "850,000 - 1,100,000"},
    {"Model": "D55", "RPM": 24, "Torque": 4010, "ISO": "F35", "RMB_Min": 15300, "RMB_Max": 15300, "Thrust_RMB": 3100, "Rotork": "-", "AUMA": "SA 40.1", "Market_Price": "1,000,000 - 1,300,000"}
]

at_data = [
    {"Model": "D08", "RPM": 0.5, "Torque": 105, "ISO": "F07/F10", "RMB": 5850, "Rotork": "IQT125", "AUMA": "SQ 05.2", "Market_Price": "150,000 - 220,000"},
    {"Model": "D10", "RPM": 0.5, "Torque": 205, "ISO": "F07/F10", "RMB": 6030, "Rotork": "IQT250", "AUMA": "SQ 07.2", "Market_Price": "165,000 - 240,000"},
    {"Model": "D12", "RPM": 0.5, "Torque": 305, "ISO": "F10", "RMB": 6250, "Rotork": "IQT500", "AUMA": "SQ 07.2", "Market_Price": "180,000 - 260,000"},
    {"Model": "D15", "RPM": 0.5, "Torque": 455, "ISO": "F10/F12", "RMB": 6470, "Rotork": "IQT500", "AUMA": "SQ 10.2", "Market_Price": "195,000 - 280,000"},
    {"Model": "D20", "RPM": 0.5, "Torque": 605, "ISO": "F12", "RMB": 6640, "Rotork": "IQT1000", "AUMA": "SQ 10.2", "Market_Price": "210,000 - 300,000"},
    {"Model": "D25", "RPM": 0.5, "Torque": 905, "ISO": "F12/F14", "RMB": 7110, "Rotork": "IQT1000", "AUMA": "SQ 12.2", "Market_Price": "230,000 - 330,000"},
    {"Model": "D30", "RPM": 0.5, "Torque": 1205, "ISO": "F14", "RMB": 7260, "Rotork": "IQT1500", "AUMA": "SQ 12.2", "Market_Price": "250,000 - 360,000"},
    {"Model": "D35", "RPM": 0.17, "Torque": 1405, "ISO": "F14/F16", "RMB": 7890, "Rotork": "IQT2000", "AUMA": "SQ 14.2", "Market_Price": "280,000 - 400,000"},
    {"Model": "D40", "RPM": 0.17, "Torque": 2100, "ISO": "F16", "RMB": 8100, "Rotork": "IQT2000 + Gear", "AUMA": "SQ 14.2", "Market_Price": "300,000 - 430,000"},
    {"Model": "D45", "RPM": 0.17, "Torque": 2550, "ISO": "F16/F25", "RMB": 8310, "Rotork": "IQT3000", "AUMA": "SQ 15.2", "Market_Price": "330,000 - 470,000"},
    {"Model": "D50", "RPM": 0.17, "Torque": 3100, "ISO": "F25", "RMB": 8520, "Rotork": "IQT3000", "AUMA": "SQ 15.2", "Market_Price": "360,000 - 500,000"}
]

tab1, tab2 = st.tabs(["🔄 Multi-Turn Actuator", "🔄 Angular Travel (Part-Turn)"])

def calc_price(rmb, ex_proof=False):
    base = rmb * cny_rate * margin_factor
    if ex_proof:
        base *= 1.10
    return base

with tab1:
    st.subheader("Multi-Turn Price Comparison Table")
    rows = []
    for item in mt_data:
        if item["RMB_Min"] == item["RMB_Max"]:
            p_std = f"{calc_price(item['RMB_Min']):,.0f}"
            p_ex = f"{calc_price(item['RMB_Min'], True):,.0f}"
        else:
            p_std = f"{calc_price(item['RMB_Min']):,.0f} - {calc_price(item['RMB_Max']):,.0f}"
            p_ex = f"{calc_price(item['RMB_Min'], True):,.0f} - {calc_price(item['RMB_Max'], True):,.0f}"
        
        rows.append({
            "DOMINIC Model": item["Model"],
            "Torque (Nm)": item["Torque"],
            "ISO Flange": item["ISO"],
            "DOMINIC Standard (THB)": p_std,
            "DOMINIC Ex-proof (+10%) (THB)": p_ex,
            "ROTORK Model": item["Rotork"],
            "AUMA Model": item["AUMA"],
            "Rotork/AUMA Market Price (THB)": item["Market_Price"]
        })
    df_mt = pd.DataFrame(rows)
    st.dataframe(df_mt, use_container_width=True)

with tab2:
    st.subheader("Angular Travel (Part-Turn) Price Comparison Table")
    rows_at = []
    for item in at_data:
        p_std = f"{calc_price(item['RMB']):,.0f}"
        p_ex = f"{calc_price(item['RMB'], True):,.0f}"
        rows_at.append({
            "DOMINIC Model": item["Model"],
            "Torque (Nm)": item["Torque"],
            "ISO Flange": item["ISO"],
            "DOMINIC Standard (THB)": p_std,
            "DOMINIC Ex-proof (+10%) (THB)": p_ex,
            "ROTORK Model": item["Rotork"],
            "AUMA Model": item["AUMA"],
            "Rotork/AUMA Market Price (THB)": item["Market_Price"]
        })
    df_at = pd.DataFrame(rows_at)
    st.dataframe(df_at, use_container_width=True)
