import streamlit as st
import pandas as pd
import math
import io
import os
import json


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

st.set_page_config(
    page_title="EDI CALCULATOR Designer",
    page_icon="⚡",
    layout="wide"
)

# ======================================
# LOGIN
# ======================================


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:

    st.title("🔐 EDI Calculator Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if (
            username == "kamran"
            and password == "spiral123"
        ):

            st.session_state["logged_in"] = True

            st.rerun()

        else:

            st.error(
                "Invalid Username or Password"
            )

    st.stop()

if st.sidebar.button("🚪 Logout"):
    st.session_state["logged_in"] = False

    st.rerun()

####################################################################################


#Session State Initialization


defaults = {

    "edi_flow": 10.0,

    "edi_fce": 0.0,

    "edi_cond": 0.0,

    "edi_tds": 0.0,

    "edi_hardness": 0.0,

    "edi_silica": 0.0,

    "edi_co2": 0.0,

    "edi_ph": 7.0,

    "edi_na": 0.0,

    "edi_cl": 0.0,

    "edi_module": "",

    "module_family": "",

    "edi_qty": 0,

    "edi_voltage": 0,

    "edi_current": 0,

    "edi_power": 0,

    "product_cond": 0.055,

    "product_resistivity": 18.2,

    "product_silica": 0.02,

    "edi_temp": 25.0,

    "project_loaded": False,

    "module_saved": False,

    "customer": "",
    "project_no": "",
    "revision": "0"
}



for k, v in defaults.items():

    if k not in st.session_state:

        st.session_state[k] = v


#Navigation

page = st.sidebar.radio(

    "Navigation",

    [

        "🏠 Dashboard",

        "🧪 Feed Water Analysis",

        "⚡ Module Selection",

        "🔋 Power Calculator",

        "📄 Output"

    ]
)

if page == "🏠 Dashboard":

    st.title("⚡ EDI CALCULATOR Designer")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Flow",
        f"{st.session_state.get('edi_flow',0):.2f} m³/hr"
    )

    c2.metric(
        "Temperature",
        f"{st.session_state.get('edi_temp',25):.1f} °C"
    )

    c3.metric(
        "Conductivity",
        f"{st.session_state.get('edi_cond',0):.2f} µS/cm"
    )

    ##################################################

    import json

    st.subheader("💾 Project Management")

    project_name = st.text_input(
        "Project Name",
        value="Project_1"
    )

    # ==========================================
    # SAVE PROJECT
    # ==========================================

    if st.button("🆕 New Project"):

        keys_to_keep = [
            "project_loaded"
        ]

        for key in list(st.session_state.keys()):

            if key not in keys_to_keep:
                del st.session_state[key]

        st.rerun()

    import json

    project_data = {

        "edi_flow": st.session_state.get("edi_flow", 0),
        "edi_temp": st.session_state.get("edi_temp", 25),

        "edi_cond25": st.session_state.get("edi_cond25", 0),
        "edi_fce": st.session_state.get("edi_fce", 0),
        "edi_tds": st.session_state.get("edi_tds", 0),

        "edi_hardness": st.session_state.get("edi_hardness", 0),
        "edi_tea": st.session_state.get("edi_tea", 0),
        "edi_silica": st.session_state.get("edi_silica", 0),
        "edi_co2": st.session_state.get("edi_co2", 0),

        "edi_cations": st.session_state.get("edi_cations", 0),
        "edi_anions": st.session_state.get("edi_anions", 0),

        "edi_module": st.session_state.get("edi_module", ""),
        "edi_qty": st.session_state.get("edi_qty", 0),

        "edi_voltage": st.session_state.get("edi_voltage", 0),
        "edi_current": st.session_state.get("edi_current", 0),
        "edi_power": st.session_state.get("edi_power", 0),

        "product_resistivity": st.session_state.get(
            "product_resistivity",
            18.2
        ),

        "product_cond": st.session_state.get(
            "product_cond",
            0.055
        ),

        "project_no": st.session_state.get(
            "project_no",
            ""
        ),

        "customer": st.session_state.get(
            "customer",
            ""
        ),

        "revision": st.session_state.get(
            "revision",
            "0"
        )
    }

    project_json = json.dumps(
        project_data,
        indent=4
    )

    st.download_button(
        "💾 Save Project",
        data=project_json,
        file_name=f"{project_name}.edi",
        mime="application/json"
    )

    # ==========================================
    # LOAD PROJECT
    # ==========================================

uploaded_project = st.file_uploader(
    "Open Saved Project",
    type=["edi", "json"],
    key="project_loader"
)


if uploaded_project is not None and not st.session_state.get("project_loaded", False):

    project_data = json.load(uploaded_project)

    for k, v in project_data.items():
        st.session_state[k] = v

    st.session_state["project_loaded"] = True

    st.success(
        "Project Loaded Successfully"
    )





    # ==========================================
    # PROJECT DETAILS
    # ==========================================

    st.text_input(
        "Customer",
        key="customer"
    )

    st.text_input(
        "Project Number",
        key="project_no"
    )

    st.text_input(
        "Revision",
        key="revision"
    )


        ###############################################
#Feed Water Analysis
# ====================================================

#Step 1 – Upload Excel

#Flow Input Section

st.subheader("Design Inputs")

col1, col2 = st.columns(2)

with col1:

    st.session_state["edi_flow"] = st.number_input(
        "EDI Product Flow (m³/hr)",
        min_value=0.1,
        value=float(st.session_state["edi_flow"]),
        step=0.1,
        key="flow_input"
    )

with col2:

    st.session_state["edi_temp"] = st.number_input(
        "Feed Temperature (°C)",
        min_value=5.0,
        max_value=45.0,
        value=float(st.session_state["edi_temp"]),
        step=1.0,
        key="temperature_input"
    )

temperature = st.session_state["edi_temp"]


uploaded_file = st.file_uploader(
    "Upload Water Analysis Report",
    type=["xlsx"]
)

if uploaded_file is not None:

    df = pd.read_excel(
        uploaded_file,
        engine="openpyxl",
        header=1
    )

    st.dataframe(
        df,
        width="stretch"
    )

#Step 2 – Extract Water Parameters

    water = dict(
        zip(
            df["Species"].astype(str).str.strip(),
            df["Raw water"]
        )
    )

    ammonium = float(water.get("Ammonium", 0) or 0)

    na = float(water.get("Sodium", 0) or 0)

    k = float(water.get("Potassium", 0) or 0)

    mg = float(water.get("Magnesium", 0) or 0)

    ca = float(water.get("Calcium", 0) or 0)

    sr = float(water.get("Strontium", 0) or 0)

    ba = float(water.get("Barium", 0) or 0)

    f = float(water.get("Fluoride", 0) or 0)

    cl = float(water.get("Chloride", 0) or 0)

    so4 = float(water.get("Sulfate", 0) or 0)

    no3 = float(water.get("Nitrate", 0) or 0)

    co3 = float(water.get("Carbonate", 0) or 0)

    hco3 = float(water.get("Bicarbonate", 0) or 0)

    boron = float(water.get("Boron", 0) or 0)

    bromide = float(water.get("Bromide", 0) or 0)

    silica = float(water.get("Silica", 0) or 0)

    co2 = float(water.get("CO2", 0) or 0)

    ph = float(water.get("pH", 7) or 7)

#Step 3 – Convert mg/L to meq/L

    EW = {

        "NH4": 18.04,

        "Na": 22.99,

        "K": 39.10,

        "Mg": 12.15,

        "Ca": 20.04,

        "Sr": 43.81,

        "Ba": 68.67,

        "F": 19.00,

        "Cl": 35.45,

        "SO4": 48.03,

        "NO3": 62.00,

        "CO3": 30.00,

        "HCO3": 61.02,

        "Br": 79.90
    }

    nh4_meq = ammonium / EW["NH4"]

    na_meq = na / EW["Na"]

    k_meq = k / EW["K"]

    mg_meq = mg / EW["Mg"]

    ca_meq = ca / EW["Ca"]

    sr_meq = sr / EW["Sr"]

    ba_meq = ba / EW["Ba"]

    f_meq = f / EW["F"]

    cl_meq = cl / EW["Cl"]

    so4_meq = so4 / EW["SO4"]

    no3_meq = no3 / EW["NO3"]

    co3_meq = co3 / EW["CO3"]

    hco3_meq = hco3 / EW["HCO3"]

    br_meq = bromide / EW["Br"]



    #Step 4 – Calculate Total Cations
    total_cations = (

            nh4_meq +

            na_meq +

            k_meq +

            mg_meq +

            ca_meq +

            sr_meq +

            ba_meq
    )

    #Step 5 – Calculate Total Anions

    total_anions = (

            f_meq +

            cl_meq +

            so4_meq +

            no3_meq +

            co3_meq +

            hco3_meq +

            br_meq
    )

    #Step 6 – Calculate Conductivity @25°C

    COND = {

        "NH4": 73.5,

        "Na": 50.1,

        "K": 73.5,

        "Mg": 53.0,

        "Ca": 59.5,

        "Sr": 59.0,

        "Ba": 56.0,

        "F": 55.4,

        "Cl": 76.3,

        "SO4": 80.0,

        "NO3": 71.4,

        "CO3": 69.3,

        "HCO3": 44.5,

        "Br": 78.1
    }

    cond_nh4 = nh4_meq * COND["NH4"]

    cond_na = na_meq * COND["Na"]

    cond_k = k_meq * COND["K"]

    cond_mg = mg_meq * COND["Mg"]

    cond_ca = ca_meq * COND["Ca"]

    cond_sr = sr_meq * COND["Sr"]

    cond_ba = ba_meq * COND["Ba"]

    cond_f = f_meq * COND["F"]

    cond_cl = cl_meq * COND["Cl"]

    cond_so4 = so4_meq * COND["SO4"]

    cond_no3 = no3_meq * COND["NO3"]

    cond_co3 = co3_meq * COND["CO3"]

    cond_hco3 = hco3_meq * COND["HCO3"]

    cond_br = br_meq * COND["Br"]



    #Total conductivity

    conductivity25 = (

            cond_nh4 +

            cond_na +

            cond_k +

            cond_mg +

            cond_ca +

            cond_sr +

            cond_ba +

            cond_f +

            cond_cl +

            cond_so4 +

            cond_no3 +

            cond_co3 +

            cond_hco3 +

            cond_br

    )

    # Feedwater Conductivity Equivalent

    fce = (
            conductivity25 +
            (co2 * 2.8)
    )

    st.session_state["edi_fce"] = fce

    #Step 8 – Calculate TDS

    tds = (

            ammonium +

            na +

            k +

            mg +

            ca +

            sr +

            ba +

            f +

            cl +

            so4 +

            no3 +

            co3 +

            hco3 +

            boron +

            bromide +

            silica

    )

    #Step 9 – Calculate Hardness

    hardness = (

            ca * 2.497 +

            mg * 4.118

    )

    #STEP 10 : TEA Calculation

    tea_meq = (

            cl_meq +

            so4_meq +

            no3_meq +

            co3_meq +

            hco3_meq



    )

    tea_caco3 = tea_meq * 50

    #Step 11 – Store Results

    st.session_state["edi_cond25"] = conductivity25

    st.session_state["edi_fce"] = fce

    st.session_state["edi_tds"] = tds

    st.session_state["edi_hardness"] = hardness

    st.session_state["edi_silica"] = silica

    st.session_state["edi_co2"] = co2

    st.session_state["edi_ph"] = ph

    st.session_state["edi_cations"] = total_cations

    st.session_state["edi_anions"] = total_anions

    st.session_state["edi_tea"] = tea_caco3

    # Step 12 – Dashboard Output

    st.subheader("Feed Water Summary")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Conductivity @25°C",
        f"{conductivity25:.2f} µS/cm"
    )

    c2.metric(
        "FCE",
        f"{fce:.2f} µS/cm"
    )

    c3.metric(
        "TDS",
        f"{tds:.2f} ppm"
    )

    ##############################################
    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Hardness",
        f"{hardness:,.2f} ppm"
    )

    c2.metric(
        "Total Cations",
        f"{total_cations:.4f} meq/L"
    )

    c3.metric(
        "Total Anions",
        f"{total_anions:.4f} meq/L"
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "TEA",
        f"{tea_caco3:.2f} ppm as CaCO₃"
    )

    c2.metric(
        "Silica",
        f"{silica:.3f} ppm"
    )

    c3.metric(
        "CO₂",
        f"{co2:.2f} ppm"
    )

    ##################################################################




##############################################################################
# IONPURE CEDI MODULE DATABASE
##############################################################################

edi_modules = {

# ============================================================================
# MX SERIES
# ============================================================================

"MX13": {
    "family": "MX",
    "nominal_flow": 0.5,
    "max_flow": 0.8,
    "recovery": 95,
    "voltage": 100,
    "current": 1.5
},

"MX25": {
    "family": "MX",
    "nominal_flow": 1.2,
    "max_flow": 2.0,
    "recovery": 95,
    "voltage": 120,
    "current": 2.0
},

"MX45": {
    "family": "MX",
    "nominal_flow": 2.5,
    "max_flow": 4.0,
    "recovery": 95,
    "voltage": 160,
    "current": 3.0
},

"MX80": {
    "family": "MX",
    "nominal_flow": 4.0,
    "max_flow": 6.0,
    "recovery": 95,
    "voltage": 200,
    "current": 4.0
},

# ============================================================================
# LX SERIES
# ============================================================================

"LXM04Z": {
    "family": "LX",
    "nominal_flow": 2.0,
    "max_flow": 3.0,
    "recovery": 95,
    "voltage": 120,
    "current": 2.0
},

"LXM10Z": {
    "family": "LX",
    "nominal_flow": 5.0,
    "max_flow": 8.0,
    "recovery": 95,
    "voltage": 180,
    "current": 3.0
},

"LXM18Z": {
    "family": "LX",
    "nominal_flow": 8.0,
    "max_flow": 12.0,
    "recovery": 95,
    "voltage": 220,
    "current": 4.0
},

"LXM24Z": {
    "family": "LX",
    "nominal_flow": 10.0,
    "max_flow": 15.0,
    "recovery": 95,
    "voltage": 250,
    "current": 5.0
},

"LXM45Z": {
    "family": "LX",
    "nominal_flow": 15.0,
    "max_flow": 20.0,
    "recovery": 95,
    "voltage": 350,
    "current": 8.0
},

"LXM10X": {
    "family": "LX",
    "nominal_flow": 5.0,
    "max_flow": 8.0,
    "recovery": 95,
    "voltage": 180,
    "current": 3.0
},

"LXM18X": {
    "family": "LX",
    "nominal_flow": 8.0,
    "max_flow": 12.0,
    "recovery": 95,
    "voltage": 220,
    "current": 4.0
},

"LXM45X": {
    "family": "LX",
    "nominal_flow": 15.0,
    "max_flow": 20.0,
    "recovery": 95,
    "voltage": 350,
    "current": 8.0
},

# ============================================================================
# VNX SERIES
# ============================================================================

"VNX15CDIT": {
    "family": "VNX",
    "nominal_flow": 3.0,
    "max_flow": 4.5,
    "recovery": 95,
    "voltage": 180,
    "current": 3.0,
    "fce_limit": 20
},

"VNX30CDIT": {
    "family": "VNX",
    "nominal_flow": 6.0,
    "max_flow": 9.0,
    "recovery": 95,
    "voltage": 220,
    "current": 4.0,
    "fce_limit": 20
},

"VNX28EP": {
    "family": "VNX",
    "nominal_flow": 5.0,
    "max_flow": 8.0,
    "recovery": 95,
    "voltage": 220,
    "current": 4.0,
    "fce_limit": 20
},

"VNX55E": {
    "family": "VNX",
    "nominal_flow": 11.4,
    "max_flow": 17.0,
    "recovery": 95,
    "voltage": 350,
    "current": 7.0,
    "fce_limit": 10
},

"VNX55EP": {
    "family": "VNX",
    "nominal_flow": 11.4,
    "max_flow": 17.0,
    "recovery": 95,
    "voltage": 78,
    "current": 8.8,
    "fce_limit": 20
},

"VNX55EX": {
    "family": "VNX",
    "nominal_flow": 11.4,
    "max_flow": 17.0,
    "recovery": 95,
    "voltage": 350,
    "current": 7.0,
    "fce_limit": 10
},

"VNX55HH": {
    "family": "VNX",
    "nominal_flow": 11.4,
    "max_flow": 17.0,
    "recovery": 95,
    "voltage": 350,
    "current": 7.0,
    "fce_limit": 20
},

"VNX23ULTRA": {
    "family": "VNX",
    "nominal_flow": 5.0,
    "max_flow": 8.0,
    "recovery": 95,
    "voltage": 220,
    "current": 4.0,
    "fce_limit": 10,

},

"VNX55ULTRA": {
    "family": "VNX",
    "nominal_flow": 11.4,
    "max_flow": 17.0,
    "recovery": 95,
    "voltage": 350,
    "current": 7.0,
    "fce_limit": 10
},

"VNX-MINI": {
    "family": "VNX",
    "nominal_flow": 12.0,
    "max_flow": 17.9,
    "recovery": 95,
    "voltage": 350,
    "current": 7.5,
    "fce_limit": 20
},

"VNX-MAX": {
    "family": "VNX",
    "nominal_flow": 15.0,
    "max_flow": 22.7,
    "recovery": 95,
    "voltage": 400,
    "current": 8.5,
    "fce_limit": 20
}
}


##############################################
#Recommended Auto-Selection Logic
########################################

if page == "⚡ Module Selection":

    st.title("⚡ Module Selection")


################################################
    saved_module = st.session_state.get(
        "edi_module",
        ""
    )

    saved_family = "MX"

    if saved_module in edi_modules:
        saved_family = edi_modules[
            saved_module
        ]["family"]

    family = st.selectbox(
        "Module Family",
        ["MX", "LX", "VNX"],
        index=["MX", "LX", "VNX"].index(
            saved_family
        )
    )

    family_models = [

        model

        for model, data in edi_modules.items()

        if data["family"] == family

    ]
############################################################

    flow = st.session_state["edi_flow"]

    qty = st.number_input(
        "Number of Modules",
        min_value=1,
        value=max(
            1,
            int(st.session_state.get("edi_qty", 1))
        ),
        step=1
    )

    saved_module = st.session_state.get(
        "edi_module",
        ""
    )

    default_index = 0

    if saved_module in family_models:
        default_index = family_models.index(
            saved_module
        )

    selected_model = st.selectbox(
        "Module Size",
        family_models,
        index=default_index
    )
################################################################################
    flow_per_module = flow / qty

    st.text_input(
        "Flow per Module (m³/hr)",
        value=f"{flow_per_module:.2f}",
        disabled=True
    )
    module_data = edi_modules[selected_model]




    fce_limit = module_data.get(
        "fce_limit",
        20
    )

    fce = st.session_state["edi_fce"]


    if fce > fce_limit:

        st.error(
            f"FCE value should not exceed "
            f"{fce_limit:.0f} µS/cm"
        )

    else:

        st.success(
            f"FCE = {fce:.2f} µS/cm is acceptable"
        )

    nominal_flow = module_data["nominal_flow"]

    max_flow = module_data["max_flow"]
#################################################
    # ==========================================
    # PRODUCT WATER QUALITY PREDICTION
    # ==========================================

    feed_cond = st.session_state["edi_cond"]

    if feed_cond <= 20:

        product_resistivity = 18.2

    elif feed_cond <= 40:

        product_resistivity = 18.0

    elif feed_cond <= 60:

        product_resistivity = 17.0

    else:

        product_resistivity = 15.0

    product_cond = (
            1 /
            product_resistivity
    )

    st.session_state["product_resistivity"] = product_resistivity

    st.session_state["product_cond"] = product_cond

    #########################################################
    if flow_per_module > max_flow:

        st.error(
            f"Flow Per Module should not exceed "
            f"{max_flow:.1f} m³/hr"
        )

    elif flow_per_module > nominal_flow:

        st.warning(
            f"Flow Per Module exceeds nominal "
            f"flow of {nominal_flow:.1f} m³/hr"
        )

    else:

        st.success(
            "Module sizing acceptable"
        )

    st.session_state["edi_module"] = selected_model

    st.session_state["edi_qty"] = qty

###################################################################################

    st.subheader("💾 Module Selection")

    if st.button("✅ Save Module Selection"):
        st.session_state["edi_module"] = selected_model
        st.session_state["edi_qty"] = qty

        st.session_state["module_saved"] = True

        st.success(
            f"Module {selected_model} saved successfully"
        )

    if st.session_state.get("module_saved", False):
        st.info(
            f"Saved Module: "
            f"{st.session_state['edi_module']} "
            f"(Qty: {st.session_state['edi_qty']})"
        )

    if st.button("🔄 Reset Module Selection"):
        st.session_state["edi_module"] = ""
        st.session_state["edi_qty"] = 0
        st.session_state["module_saved"] = False

        st.rerun()
    ##############################################
    # ==========================================
    ########################################################
    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Selected Module",
            selected_model
        )

        st.metric(
            "Modules",
            qty
        )

    with col2:

        st.metric(
            "Flow / Module",
            f"{flow_per_module:.2f}"
        )

        st.metric(
            "Installed Capacity",
            f"{qty * nominal_flow:.2f}"
        )






#POWER CALCULATOR

if page == "🔋 Power Calculator":

    st.title("🔋 Estimated Power Requirements")

    module = st.session_state["edi_module"]

    qty = st.session_state["edi_qty"]

    flow = st.session_state["edi_flow"]

    if module != "":

        voltage = edi_modules[module]["voltage"]

        current = edi_modules[module]["current"]

        st.session_state["edi_voltage"] = voltage
        st.session_state["edi_current"] = current

        # DC power per module
        dc_power_module = (
            voltage * current
        ) / 1000

        # Assume 93% power supply efficiency
        ac_power_module = (
            dc_power_module / 0.93
        )

        total_ac_power = (
            ac_power_module * qty
        )

        total_kwh_day = (
            total_ac_power * 24
        )

        dc_energy_metric = (
            total_ac_power / flow
        )

        dc_energy_imperial = (
            dc_energy_metric * 0.003785
        )

        st.session_state["edi_power"] = total_ac_power

        st.session_state["ac_power_module"] = ac_power_module
        st.session_state["total_ac_power"] = total_ac_power
        st.session_state["total_kwh_day"] = total_kwh_day
        st.session_state["dc_energy_metric"] = dc_energy_metric


        power_df = pd.DataFrame({

            "Parameter": [

                "AC Power Consumption",

                "Total AC Power Consumption",

                "DC Energy Consumption (imperial)",

                "DC Energy Consumption (metric)",

                "DC Voltage Per Module",

                "Start-up DC Current Per Module"

            ],

            "Value": [

                f"{ac_power_module:.2f} kW/module",

                f"{total_kwh_day:.2f} kWh/day",

                f"{dc_energy_imperial:.2f} kWh/kgal",

                f"{dc_energy_metric:.2f} kWh/m³",

                f"{voltage:.0f} V",

                f"{current:.1f} A"

            ]

        })

        st.dataframe(
            power_df,
            hide_index=True,
            width="stretch"
        )




#PDF Generator

def generate_pdf():

        buffer = io.BytesIO()

        pdf = canvas.Canvas(
            buffer,
            pagesize=A4
        )

        y = 800

        pdf.setFont(
            "Helvetica-Bold",
            16
        )

        pdf.drawString(
            50,
            y,
            "EDI CALCULATOR DESIGN REPORT"
        )

        y -= 40

        pdf.setFont(
            "Helvetica",
            10
        )

        pdf.drawString(
            50,
            y,
            f"Flow: {st.session_state['edi_flow']:.2f} m3/hr"
        )

        y -= 20

        pdf.drawString(
            50,
            y,
            f"TDS: {st.session_state['edi_tds']:.2f} ppm"
        )

        y -= 20

        pdf.drawString(
            50,
            y,
            f"Conductivity @25°C: {st.session_state.get('edi_cond25',0):.2f} uS/cm"
        )

        y -= 20

        pdf.drawString(
            50,
            y,
            f"FCE: {st.session_state.get('edi_fce',0):.2f} uS/cm"
        )

        y -= 20

        pdf.drawString(
            50,
            y,
            f"Hardness: {st.session_state['edi_hardness']:.2f} ppm"
        )

        y -= 20

        pdf.drawString(
            50,
            y,
            f"Silica: {st.session_state['edi_silica']:.2f} ppm"
        )

        y -= 20

        pdf.drawString(
            50,
            y,
            f"Module: {st.session_state['edi_module']}"
        )

        y -= 20

        pdf.drawString(
            50,
            y,
            f"Quantity: {st.session_state['edi_qty']}"
        )

        y -= 20

        pdf.drawString(
            50,
            y,
            f"Power: {st.session_state['edi_power']:.2f} kW"
        )

        y -= 20

        pdf.drawString(
            50,
            y,
            f"Product Resistivity: "
            f"{st.session_state['product_resistivity']:.1f} MΩ-cm"
        )

        y -= 20

        pdf.drawString(
            50,
            y,
            f"Product Conductivity: "
            f"{st.session_state['product_cond']:.3f} µS/cm"
        )

        # =====================================================
        # PRODUCT QUALITY SUMMARY
        # =====================================================

        y -= 40

        pdf.setFont(
            "Helvetica-Bold",
            12
        )

        pdf.drawString(
            50,
            y,
            "PRODUCT QUALITY SUMMARY"
        )

        y -= 20

        pdf.setFont(
            "Helvetica",
            10
        )

        pdf.drawString(
            50,
            y,
            f"Resistivity : "
            f"{st.session_state['product_resistivity']:.1f} MΩ-cm"
        )

        y -= 20

        pdf.drawString(
            50,
            y,
            f"Conductivity : "
            f"{st.session_state['product_cond']:.3f} µS/cm"
        )

        y -= 20

        pdf.drawString(
            50,
            y,
            f"Product Silica : "
            f"{st.session_state['product_silica']:.3f} ppm"
        )

        pdf.save()

        buffer.seek(0)

        return buffer


#Output Page

if page == "📄 Output":

    st.title("📄 EDI Design Summary")
    # ======================================
    # FEED WATER SUMMARY
    # ======================================

    st.subheader("🧪 Feed Water Summary")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Conductivity @25°C",
        f"{st.session_state.get('edi_cond25', 0):.2f} µS/cm"
    )

    c2.metric(
        "FCE",
        f"{st.session_state.get('edi_fce', 0):.2f} µS/cm"
    )

    c3.metric(
        "TDS",
        f"{st.session_state.get('edi_tds', 0):.2f} ppm"
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Hardness",
        f"{st.session_state.get('edi_hardness', 0):.2f} ppm"
    )

    c2.metric(
        "TEA",
        f"{st.session_state.get('edi_tea', 0):.2f} ppm as CaCO₃"
    )

    c3.metric(
        "Silica",
        f"{st.session_state.get('edi_silica', 0):.3f} ppm"
    )
    # ======================================
    # MODULE SELECTION
    # ======================================

    st.subheader("⚡ Module Selection")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Selected Module",
        st.session_state["edi_module"]
    )

    c2.metric(
        "Quantity",
        st.session_state["edi_qty"]
    )

    c3.metric(
        "Flow",
        f"{st.session_state['edi_flow']:.2f} m³/hr"
    )

    # ======================================
    # PRODUCT QUALITY
    # ======================================

    st.subheader("💧 Product Quality Summary")

    c1, c2 = st.columns(2)

    c1.metric(
        "Resistivity",
        f"{st.session_state['product_resistivity']:.1f} MΩ-cm"
    )

    c2.metric(
        "Conductivity",
        f"{st.session_state['product_cond']:.3f} µS/cm"
    )

    # ======================================
    # POWER SUMMARY
    # ======================================

    st.subheader("🔋 Estimated Power Requirements")

    c1, c2 = st.columns(2)

    c1.metric(
        "Voltage",
        f"{st.session_state['edi_voltage']:.0f} V"
    )

    c2.metric(
        "Power",
        f"{st.session_state['edi_power']:.2f} kW"
    )

    pdf = generate_pdf()

    st.download_button(
        "📄 Download EDI Report",
        pdf,
        file_name="EDI_Report.pdf",
        mime="application/pdf"
    )

    ##################

    st.subheader("📋 System Summary")

    module_data = edi_modules[
        st.session_state["edi_module"]
    ]

    product_flow = st.session_state["edi_flow"]

    recovery = module_data["recovery"]

    feed_flow = (
            product_flow /
            (recovery / 100)
    )

    reject_flow = (
            feed_flow -
            product_flow
    )

    flow_per_module = (
            product_flow /
            st.session_state["edi_qty"]
    )

    salt_rejection = 99.7

    dilute_pressure_drop = 1.75

    summary_df = pd.DataFrame({

        "Parameter": [

            "Module Type",

            "Total Feed Flow",

            "Total Reject Flow",

            "Total Product Flow",

            "Flow Per Module",

            "Number of Modules",

            "Max Recovery",

            "Salt Rejection",

            "Dilute Pressure Drop"

        ],

        "Value": [

            st.session_state["edi_module"],

            f"{feed_flow:.2f} m³/hr",

            f"{reject_flow:.2f} m³/hr",

            f"{product_flow:.2f} m³/hr",

            f"{flow_per_module:.2f} m³/hr",

            st.session_state["edi_qty"],

            f"{recovery:.0f} %",

            f"{salt_rejection:.1f} %",

            f"{dilute_pressure_drop:.2f} bar"

        ]
    })

    st.dataframe(
        summary_df,
        hide_index=True,
        width="stretch"
    )


#######################################################

