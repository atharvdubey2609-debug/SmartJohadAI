import math
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="SmartJohad AI", page_icon="💧", layout="wide")

st.title("💧 SmartJohad AI")
st.subheader("AI-assisted preliminary design and risk screening for traditional johads")
st.caption("Ancient Indian water-harvesting wisdom • Engineering calculations • Decision support")

st.warning(
    "Educational prototype only. This tool does not certify structural safety or provide construction-ready designs. "
    "Actual projects require site surveys, design-storm analysis, geotechnical investigation, applicable standards, and qualified engineering review."
)

with st.sidebar:
    st.header("1. Site & rainfall")
    area_ha = st.number_input("Catchment area (hectares)", min_value=0.1, max_value=10000.0, value=10.0, step=0.5)
    rainfall_mm = st.number_input("Rainfall event (mm)", min_value=1.0, max_value=1000.0, value=100.0, step=5.0)
    runoff_coeff = st.slider("Runoff coefficient", 0.05, 0.95, 0.25, 0.05)
    st.caption("Choose a locally justified coefficient based on land cover, soil, slope, and rainfall characteristics.")

    st.header("2. Concept embankment")
    bund_height = st.number_input("Bund height (m)", 0.5, 8.0, 2.0, 0.25)
    crest_width = st.number_input("Crest width (m)", 0.5, 10.0, 2.0, 0.25)
    upstream_slope = st.number_input("Upstream slope (H:V)", 1.0, 5.0, 2.0, 0.25)
    downstream_slope = st.number_input("Downstream slope (H:V)", 1.0, 5.0, 2.5, 0.25)
    bund_length = st.number_input("Approximate bund length (m)", 5.0, 1000.0, 50.0, 5.0)

    st.header("3. Screening information")
    soil = st.selectbox("Indicative soil condition", [
        "Not assessed", "Relatively low permeability (clayey)",
        "Moderate permeability", "High permeability / sandy"
    ])
    spillway = st.selectbox("Spillway status", [
        "Unknown / not designed", "Conceptual spillway included", "No spillway considered"
    ])
    freeboard = st.number_input("Concept freeboard (m)", 0.0, 2.0, 0.3, 0.1)

# Event runoff approximation
catchment_m2 = area_ha * 10000
runoff_m3 = catchment_m2 * rainfall_mm / 1000 * runoff_coeff
runoff_litres = runoff_m3 * 1000

# Simplified trapezoidal embankment geometry
base_width = crest_width + bund_height * (upstream_slope + downstream_slope)
cross_section_area = ((crest_width + base_width) * bund_height) / 2
fill_volume = cross_section_area * bund_length

st.markdown("## Preliminary results")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Estimated event runoff", f"{runoff_m3:,.0f} m³")
c2.metric("Equivalent volume", f"{runoff_litres:,.0f} litres")
c3.metric("Concept base width", f"{base_width:.2f} m")
c4.metric("Approx. embankment fill", f"{fill_volume:,.1f} m³")

st.caption(
    "Runoff is an event-level estimate, not guaranteed stored or saved water. Storage capacity, hydrograph timing, "
    "evaporation, infiltration, seepage, environmental flows, and water use are not modelled."
)

left, right = st.columns([1.05, 1.25])
with left:
    st.markdown("### Conceptual cross-section")
    z = bund_height
    x = [-upstream_slope * z, 0, crest_width, crest_width + downstream_slope * z]
    y = [0, z, z, 0]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", fill="tozeroy", name="Concept embankment"))
    fig.add_trace(go.Scatter(
        x=[x[0] - 1, x[-1] + 1], y=[0, 0], mode="lines",
        line=dict(dash="dash"), name="Ground line"
    ))
    fig.update_layout(
        xaxis_title="Horizontal distance (m; schematic)",
        yaxis_title="Height (m)", height=390,
        margin=dict(l=20, r=20, t=20, b=20), showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Schematic only. It omits the basin, foundation, spillway, filters, drains, cutoff, and erosion protection.")

checks = []
def add_check(title, level, action):
    checks.append({"Screening item": title, "Attention": level, "Next action": action})

if runoff_m3 > 5000:
    add_check("Event runoff may exceed the capacity of a small structure", "High attention",
              "Survey the basin and route inflows; do not assume all runoff can be stored.")
else:
    add_check("Runoff vs. storage capacity", "Required",
              "Compare estimated runoff with surveyed storage, losses, and inflow timing.")

if freeboard < 0.3:
    add_check("Low concept freeboard input", "Review",
              "Set design freeboard using applicable standards, flood routing, waves, and settlement.")
else:
    add_check("Freeboard is unverified", "Required",
              "Verify design flood level and freeboard against local criteria.")

if spillway == "No spillway considered":
    add_check("No spillway considered", "High attention",
              "Have a safe overflow route designed; uncontrolled overtopping can cause failure.")
elif spillway == "Unknown / not designed":
    add_check("Spillway design is unknown", "High attention",
              "Calculate peak inflow and design stable spillway capacity and downstream discharge.")
else:
    add_check("Conceptual spillway indicated", "Required",
              "Verify capacity, erosion protection, and downstream conditions.")

if soil == "High permeability / sandy":
    add_check("Potential seepage or piping issue", "High attention",
              "Investigate soil profile and seepage; assess filters/cutoff if warranted.")
elif soil == "Not assessed":
    add_check("Soil properties not verified", "High attention",
              "Obtain field/lab classification, permeability, compaction, and strength data.")
elif soil == "Moderate permeability":
    add_check("Seepage behaviour needs assessment", "Review",
              "Confirm the soil profile and seepage path with a geotechnical engineer.")
else:
    add_check("Clayey condition is not proof of safety", "Review",
              "Check cracking, erosion susceptibility, compaction, and measured soil parameters.")

if bund_height > 3:
    add_check("Bund height requires site-specific design", "High attention",
              "Assess foundation, slope stability, seepage, and consequences of failure.")
else:
    add_check("Slope stability has not been calculated", "Required",
              "Use verified soil strength, pore pressure, geometry, and loading in an appropriate stability analysis.")

with right:
    st.markdown("### Risk-screening checklist")
    df = pd.DataFrame(checks)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button(
        "Download screening report (CSV)",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="smartjohad_screening_report.csv",
        mime="text/csv"
    )

st.markdown("## What makes this a smart structural-design project?")
st.markdown("""
- **Ancient technique:** adapts the traditional johad concept for modern, evidence-based restoration planning.
- **Transparent engineering:** provides a first-pass runoff estimate and simplified embankment geometry.
- **Risk-aware workflow:** flags missing information that must be investigated before design.
- **Next development step:** add verified site data and validated expert labels before training an AI model.
""")

st.info(
    "Competition positioning: a digital decision-support prototype that combines traditional rainwater harvesting with "
    "preliminary engineering calculations and risk-screening prompts. Rule-based prompts are not a trained AI model."
)
