import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Optional
import numpy_financial as npf
import json
from pathlib import Path
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Commercial Real Estate Investment Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, crisp design
st.markdown("""
    <style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Main container */
    .main {
        background-color: #fafafa;
    }
    
    /* Header styling */
    .main-header {
        font-size: 2.75rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        padding: 2rem 0 1rem 0;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1a202c;
        margin: 2rem 0 1rem 0;
        letter-spacing: -0.01em;
    }
    
    .section-divider {
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, #e2e8f0, transparent);
        margin: 2rem 0;
    }
    
    /* Metric cards */
    div[data-testid="metric-container"] {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
    }
    
    div[data-testid="metric-container"] label {
        font-size: 0.875rem;
        font-weight: 500;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 1.875rem;
        font-weight: 700;
        color: #1a202c;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
        border-right: 1px solid #e2e8f0;
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.625rem 1.25rem;
        font-weight: 600;
        font-size: 0.875rem;
        letter-spacing: 0.025em;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(102, 126, 234, 0.2);
    }
    
    .stButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stButton button:active {
        transform: translateY(0);
    }
    
    /* Download buttons */
    .stDownloadButton button {
        background: white;
        color: #667eea;
        border: 1px solid #667eea;
        border-radius: 8px;
        padding: 0.625rem 1.25rem;
        font-weight: 600;
        font-size: 0.875rem;
        transition: all 0.2s ease;
    }
    
    .stDownloadButton button:hover {
        background: #f7fafc;
        border-color: #764ba2;
        color: #764ba2;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background-color: transparent;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        background-color: transparent;
        border-radius: 8px 8px 0 0;
        color: #64748b;
        font-weight: 600;
        font-size: 0.9rem;
        padding: 0 1.5rem;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Input fields */
    .stNumberInput input, .stTextInput input {
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        padding: 0.625rem 0.875rem;
        font-size: 0.9rem;
        transition: all 0.2s ease;
    }
    
    .stNumberInput input:focus, .stTextInput input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Sliders */
    .stSlider {
        padding: 1rem 0;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        font-weight: 600;
        color: #1a202c;
        font-size: 0.95rem;
        transition: all 0.2s ease;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #667eea;
        background-color: #f8f9fa;
    }
    
    /* Dataframe */
    .stDataFrame {
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 8px;
        border-left-width: 4px;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Section headers in sidebar */
    section[data-testid="stSidebar"] h2 {
        font-size: 1rem;
        font-weight: 700;
        color: #1a202c;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    /* Sidebar text */
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] label {
        font-size: 0.875rem;
        color: #475569;
    }
    
    /* Card-like containers */
    div[data-testid="column"] {
        background: transparent;
    }
    
    /* Success/Error messages */
    .stSuccess, .stError {
        border-radius: 8px;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

@dataclass
class PropertyInputs:
    """Store all property input parameters"""
    # Property Details
    building_size: float
    purchase_price: float
    closing_costs_pct: float
    
    # Financing
    down_payment_pct: float
    interest_rate: float
    loan_term_years: int
    
    # Revenue
    annual_rent_psf: float
    rent_growth_rate: float
    stabilized_occupancy: float
    year1_occupancy: float
    other_income_pct: float
    
    # Operating Expenses
    property_tax_psf: float
    insurance_psf: float
    cam_psf: float
    property_mgmt_pct: float
    leasing_commission_pct: float
    repairs_maintenance: float
    capex_reserve_psf: float
    initial_ti: float
    
    # Exit Assumptions
    hold_period_years: int
    exit_cap_rate: float
    sale_costs_pct: float
    discount_rate: float
    
    @property
    def price_per_sf(self) -> float:
        return self.purchase_price / self.building_size
    
    @property
    def total_acquisition_cost(self) -> float:
        return self.purchase_price * (1 + self.closing_costs_pct)
    
    @property
    def equity_required(self) -> float:
        return self.total_acquisition_cost * self.down_payment_pct
    
    @property
    def loan_amount(self) -> float:
        return self.total_acquisition_cost - self.equity_required
    
    @property
    def annual_debt_service(self) -> float:
        if self.interest_rate == 0:
            return self.loan_amount / self.loan_term_years
        return -npf.pmt(self.interest_rate, self.loan_term_years, self.loan_amount)
    
    @property
    def monthly_debt_service(self) -> float:
        return self.annual_debt_service / 12


def save_scenario(inputs: PropertyInputs, scenario_name: str, filename: Optional[str] = None) -> str:
    """Save scenario inputs to JSON file"""
    if filename is None:
        # Create scenarios directory if it doesn't exist
        scenarios_dir = Path("scenarios")
        scenarios_dir.mkdir(exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(c for c in scenario_name if c.isalnum() or c in (' ', '_', '-')).strip()
        safe_name = safe_name.replace(' ', '_')
        filename = f"scenarios/{safe_name}_{timestamp}.json"
    
    # Convert to dict and add metadata
    scenario_data = {
        'name': scenario_name,
        'created_at': datetime.now().isoformat(),
        'inputs': asdict(inputs)
    }
    
    # Save to file
    with open(filename, 'w') as f:
        json.dump(scenario_data, f, indent=2)
    
    return filename


def load_scenario(filename: str) -> Tuple[str, PropertyInputs]:
    """Load scenario from JSON file"""
    with open(filename, 'r') as f:
        scenario_data = json.load(f)
    
    scenario_name = scenario_data.get('name', 'Unnamed Scenario')
    inputs_dict = scenario_data['inputs']
    
    # Convert dict to PropertyInputs
    inputs = PropertyInputs(**inputs_dict)
    
    return scenario_name, inputs


def get_saved_scenarios() -> List[str]:
    """Get list of saved scenario files"""
    scenarios_dir = Path("scenarios")
    if not scenarios_dir.exists():
        return []
    
    scenario_files = list(scenarios_dir.glob("*.json"))
    return sorted([str(f) for f in scenario_files], reverse=True)


class CREAnalyzer:
    """Commercial Real Estate Investment Analyzer"""
    
    def __init__(self, inputs: PropertyInputs):
        self.inputs = inputs
        self.pro_forma = None
        self.returns = None
        
    def calculate_pro_forma(self) -> pd.DataFrame:
        """Generate 10-year pro forma operating statement"""
        years = range(0, self.inputs.hold_period_years + 1)
        data = []
        
        for year in years:
            year_data = {'Year': year}
            
            # Revenue calculations
            if year == 0:
                rent_psf = 0
                occupancy = 0
                occupied_sf = 0
            elif year == 1:
                rent_psf = self.inputs.annual_rent_psf
                occupancy = self.inputs.year1_occupancy
                occupied_sf = self.inputs.building_size * occupancy
            else:
                rent_psf = self.inputs.annual_rent_psf * ((1 + self.inputs.rent_growth_rate) ** (year - 1))
                occupancy = self.inputs.stabilized_occupancy
                occupied_sf = self.inputs.building_size * occupancy
            
            gross_rental_income = occupied_sf * rent_psf
            other_income = gross_rental_income * self.inputs.other_income_pct
            total_revenue = gross_rental_income + other_income
            
            # Operating Expenses (Reimbursed)
            if year == 0:
                property_taxes = 0
                insurance = 0
                cam = 0
            else:
                growth_factor = (1 + self.inputs.rent_growth_rate) ** (year - 1)
                property_taxes = self.inputs.building_size * self.inputs.property_tax_psf * growth_factor
                insurance = self.inputs.building_size * self.inputs.insurance_psf * growth_factor
                cam = self.inputs.building_size * self.inputs.cam_psf * growth_factor
            
            total_reimbursable = property_taxes + insurance + cam
            
            # Landlord Expenses
            if year == 0:
                property_mgmt = 0
                leasing_commission = 0
                repairs = 0
            else:
                property_mgmt = total_revenue * self.inputs.property_mgmt_pct
                leasing_commission = total_revenue * self.inputs.leasing_commission_pct
                repairs = self.inputs.repairs_maintenance
            
            total_landlord_exp = property_mgmt + leasing_commission + repairs
            
            # NOI
            noi = total_revenue - total_landlord_exp
            
            # Capital Expenditures
            if year == 0:
                ti = self.inputs.initial_ti
                capex_reserve = 0
            else:
                ti = 0
                capex_reserve = self.inputs.building_size * self.inputs.capex_reserve_psf
            
            total_capex = ti + capex_reserve
            
            # Cash Flow
            if year == 0:
                debt_service = 0
            else:
                debt_service = self.inputs.annual_debt_service
            
            pre_tax_cash_flow = noi - debt_service - total_capex
            
            # Debt metrics
            if year > 0 and debt_service > 0:
                dscr = noi / debt_service
                cash_on_cash = pre_tax_cash_flow / self.inputs.equity_required
            else:
                dscr = 0
                cash_on_cash = 0
            
            year_data.update({
                'Rent_PSF': rent_psf,
                'Occupancy': occupancy,
                'Occupied_SF': occupied_sf,
                'Gross_Rental_Income': gross_rental_income,
                'Other_Income': other_income,
                'Total_Revenue': total_revenue,
                'Property_Taxes': property_taxes,
                'Insurance': insurance,
                'CAM': cam,
                'Total_Reimbursable': total_reimbursable,
                'Property_Management': property_mgmt,
                'Leasing_Commission': leasing_commission,
                'Repairs_Maintenance': repairs,
                'Total_Landlord_Expenses': total_landlord_exp,
                'NOI': noi,
                'Initial_TI': ti,
                'CapEx_Reserve': capex_reserve,
                'Total_CapEx': total_capex,
                'Debt_Service': debt_service,
                'Pre_Tax_Cash_Flow': pre_tax_cash_flow,
                'DSCR': dscr,
                'Cash_on_Cash': cash_on_cash
            })
            
            data.append(year_data)
        
        self.pro_forma = pd.DataFrame(data)
        return self.pro_forma
    
    def calculate_returns(self) -> Dict:
        """Calculate investment returns and exit analysis"""
        if self.pro_forma is None:
            self.calculate_pro_forma()
        
        # Exit value calculation
        final_year = self.inputs.hold_period_years
        year_after_noi = self.pro_forma.loc[final_year, 'NOI'] * (1 + self.inputs.rent_growth_rate)
        
        gross_sale_price = year_after_noi / self.inputs.exit_cap_rate
        sale_costs = gross_sale_price * self.inputs.sale_costs_pct
        net_sale_proceeds = gross_sale_price - sale_costs
        
        # Loan balance at exit
        if self.inputs.interest_rate > 0:
            remaining_periods = self.inputs.loan_term_years - self.inputs.hold_period_years
            if remaining_periods > 0:
                loan_balance = npf.pv(
                    self.inputs.interest_rate,
                    remaining_periods,
                    -self.inputs.annual_debt_service
                )
            else:
                loan_balance = 0
        else:
            loan_balance = self.inputs.loan_amount - (self.inputs.annual_debt_service * self.inputs.hold_period_years)
        
        net_cash_from_sale = net_sale_proceeds - loan_balance
        
        # Return calculations
        total_cash_flow = self.pro_forma.loc[1:final_year, 'Pre_Tax_Cash_Flow'].sum()
        total_cash_returned = total_cash_flow + net_cash_from_sale
        total_profit = total_cash_returned - self.inputs.equity_required
        
        equity_multiple = total_cash_returned / self.inputs.equity_required
        avg_cash_on_cash = self.pro_forma.loc[1:final_year, 'Cash_on_Cash'].mean()
        
        # IRR calculation
        cash_flows = [-self.inputs.equity_required]
        cash_flows.extend(self.pro_forma.loc[1:final_year, 'Pre_Tax_Cash_Flow'].tolist())
        cash_flows[-1] += net_cash_from_sale
        irr = npf.irr(cash_flows)
        
        # NPV calculation
        npv = npf.npv(self.inputs.discount_rate, cash_flows)
        
        # Year 1 metrics
        year1_noi = self.pro_forma.loc[1, 'NOI']
        going_in_cap_rate = year1_noi / self.inputs.purchase_price
        year1_dscr = self.pro_forma.loc[1, 'DSCR']
        year1_coc = self.pro_forma.loc[1, 'Cash_on_Cash']
        
        self.returns = {
            'year_after_noi': year_after_noi,
            'gross_sale_price': gross_sale_price,
            'sale_costs': sale_costs,
            'net_sale_proceeds': net_sale_proceeds,
            'loan_balance': loan_balance,
            'net_cash_from_sale': net_cash_from_sale,
            'total_cash_flow': total_cash_flow,
            'total_cash_returned': total_cash_returned,
            'total_profit': total_profit,
            'equity_multiple': equity_multiple,
            'avg_cash_on_cash': avg_cash_on_cash,
            'irr': irr,
            'npv': npv,
            'year1_noi': year1_noi,
            'going_in_cap_rate': going_in_cap_rate,
            'year1_dscr': year1_dscr,
            'year1_coc': year1_coc,
            'cash_flows': cash_flows
        }
        
        return self.returns


def create_inputs_sidebar() -> PropertyInputs:
    """Create sidebar with all input parameters"""
    st.sidebar.markdown("## SCENARIOS")
    
    # Initialize session state for loaded inputs
    if 'loaded_inputs' not in st.session_state:
        st.session_state.loaded_inputs = None
    if 'scenario_name' not in st.session_state:
        st.session_state.scenario_name = "New Scenario"
    
    # Save/Load UI
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("Save", use_container_width=True):
            st.session_state.show_save_dialog = True
    
    with col2:
        if st.button("Load", use_container_width=True):
            st.session_state.show_load_dialog = True
    
    # Save dialog
    if st.session_state.get('show_save_dialog', False):
        with st.sidebar.expander("SAVE SCENARIO", expanded=True):
            save_name = st.text_input("Scenario Name", value=st.session_state.scenario_name)
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Save", key="save_confirm"):
                    # This will be called after inputs are created
                    st.session_state.pending_save = save_name
                    st.session_state.show_save_dialog = False
            
            with col2:
                if st.button("Cancel", key="save_cancel"):
                    st.session_state.show_save_dialog = False
                    st.rerun()
    
    # Load dialog
    if st.session_state.get('show_load_dialog', False):
        with st.sidebar.expander("LOAD SCENARIO", expanded=True):
            saved_scenarios = get_saved_scenarios()
            
            if saved_scenarios:
                # Show list of scenarios with names
                scenario_options = []
                for filepath in saved_scenarios:
                    try:
                        with open(filepath, 'r') as f:
                            data = json.load(f)
                            name = data.get('name', 'Unnamed')
                            created = data.get('created_at', '')
                            if created:
                                created_date = datetime.fromisoformat(created).strftime("%Y-%m-%d %H:%M")
                                display_name = f"{name} ({created_date})"
                            else:
                                display_name = name
                            scenario_options.append((display_name, filepath))
                    except:
                        continue
                
                if scenario_options:
                    selected_display = st.selectbox(
                        "Select Scenario",
                        options=[opt[0] for opt in scenario_options]
                    )
                    selected_idx = [opt[0] for opt in scenario_options].index(selected_display)
                    selected_file = scenario_options[selected_idx][1]
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("Load", key="load_confirm"):
                            scenario_name, loaded_inputs = load_scenario(selected_file)
                            st.session_state.loaded_inputs = loaded_inputs
                            st.session_state.scenario_name = scenario_name
                            st.session_state.show_load_dialog = False
                            st.rerun()
                    
                    with col2:
                        if st.button("Cancel", key="load_cancel"):
                            st.session_state.show_load_dialog = False
                            st.rerun()
                else:
                    st.info("No saved scenarios found")
                    if st.button("Close"):
                        st.session_state.show_load_dialog = False
                        st.rerun()
            else:
                st.info("No saved scenarios found. Save your first scenario using the Save button above.")
                if st.button("Close"):
                    st.session_state.show_load_dialog = False
                    st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("## PROPERTY INPUTS")
    st.sidebar.markdown(f"**Current Scenario:** {st.session_state.scenario_name}")
    
    # Use loaded inputs if available
    default_inputs = st.session_state.loaded_inputs if st.session_state.loaded_inputs else None
    
    with st.sidebar.expander("PROPERTY DETAILS", expanded=True):
        building_size = st.number_input(
            "Building Size (SF)",
            min_value=1000,
            value=int(default_inputs.building_size) if default_inputs else 50000,
            step=1000,
            help="Total rentable square footage"
        )
        purchase_price = st.number_input(
            "Purchase Price ($)",
            min_value=100000,
            value=int(default_inputs.purchase_price) if default_inputs else 10000000,
            step=100000,
            help="Total purchase price"
        )
        st.metric("Price per SF", f"${purchase_price/building_size:.2f}")
        closing_costs_pct = st.slider(
            "Closing Costs (%)",
            min_value=0.0,
            max_value=10.0,
            value=float(default_inputs.closing_costs_pct * 100) if default_inputs else 3.0,
            step=0.1
        ) / 100
    
    with st.sidebar.expander("FINANCING STRUCTURE", expanded=True):
        down_payment_pct = st.slider(
            "Down Payment (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(default_inputs.down_payment_pct * 100) if default_inputs else 25.0,
            step=5.0
        ) / 100
        interest_rate = st.slider(
            "Interest Rate (%)",
            min_value=0.0,
            max_value=15.0,
            value=float(default_inputs.interest_rate * 100) if default_inputs else 7.0,
            step=0.25
        ) / 100
        loan_term_years = st.number_input(
            "Loan Term (Years)",
            min_value=1,
            max_value=30,
            value=int(default_inputs.loan_term_years) if default_inputs else 25,
            step=1
        )
    
    with st.sidebar.expander("REVENUE ASSUMPTIONS", expanded=True):
        annual_rent_psf = st.number_input(
            "Annual Base Rent per SF (NNN) ($)",
            min_value=1.0,
            value=float(default_inputs.annual_rent_psf) if default_inputs else 18.0,
            step=0.5
        )
        rent_growth_rate = st.slider(
            "Rent Growth Rate (Annual %)",
            min_value=0.0,
            max_value=10.0,
            value=float(default_inputs.rent_growth_rate * 100) if default_inputs else 3.0,
            step=0.25
        ) / 100
        year1_occupancy = st.slider(
            "Year 1 Occupancy (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(default_inputs.year1_occupancy * 100) if default_inputs else 90.0,
            step=5.0
        ) / 100
        stabilized_occupancy = st.slider(
            "Stabilized Occupancy (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(default_inputs.stabilized_occupancy * 100) if default_inputs else 95.0,
            step=5.0
        ) / 100
        other_income_pct = st.slider(
            "Other Income (% of Rent)",
            min_value=0.0,
            max_value=10.0,
            value=float(default_inputs.other_income_pct * 100) if default_inputs else 2.0,
            step=0.5
        ) / 100
    
    with st.sidebar.expander("OPERATING EXPENSES (NNN)", expanded=False):
        property_tax_psf = st.number_input(
            "Property Taxes ($/SF)",
            min_value=0.0,
            value=float(default_inputs.property_tax_psf) if default_inputs else 1.5,
            step=0.1
        )
        insurance_psf = st.number_input(
            "Property Insurance ($/SF)",
            min_value=0.0,
            value=float(default_inputs.insurance_psf) if default_inputs else 0.75,
            step=0.05
        )
        cam_psf = st.number_input(
            "CAM ($/SF)",
            min_value=0.0,
            value=float(default_inputs.cam_psf) if default_inputs else 1.25,
            step=0.1
        )
        property_mgmt_pct = st.slider(
            "Property Management (% of Revenue)",
            min_value=0.0,
            max_value=10.0,
            value=float(default_inputs.property_mgmt_pct * 100) if default_inputs else 4.0,
            step=0.5
        ) / 100
        leasing_commission_pct = st.slider(
            "Leasing Commissions (% of Revenue)",
            min_value=0.0,
            max_value=10.0,
            value=float(default_inputs.leasing_commission_pct * 100) if default_inputs else 3.0,
            step=0.5
        ) / 100
        repairs_maintenance = st.number_input(
            "Repairs & Maintenance (Annual $)",
            min_value=0,
            value=int(default_inputs.repairs_maintenance) if default_inputs else 25000,
            step=1000
        )
    
    with st.sidebar.expander("CAPITAL EXPENDITURES", expanded=False):
        initial_ti = st.number_input(
            "Initial Tenant Improvements ($)",
            min_value=0,
            value=int(default_inputs.initial_ti) if default_inputs else 250000,
            step=10000
        )
        capex_reserve_psf = st.number_input(
            "Annual CapEx Reserve ($/SF)",
            min_value=0.0,
            value=float(default_inputs.capex_reserve_psf) if default_inputs else 0.75,
            step=0.05
        )
    
    with st.sidebar.expander("EXIT ASSUMPTIONS", expanded=True):
        hold_period_years = st.number_input(
            "Hold Period (Years)",
            min_value=1,
            max_value=30,
            value=int(default_inputs.hold_period_years) if default_inputs else 10,
            step=1
        )
        exit_cap_rate = st.slider(
            "Exit Cap Rate (%)",
            min_value=1.0,
            max_value=15.0,
            value=float(default_inputs.exit_cap_rate * 100) if default_inputs else 6.5,
            step=0.25
        ) / 100
        sale_costs_pct = st.slider(
            "Sale Costs (%)",
            min_value=0.0,
            max_value=10.0,
            value=float(default_inputs.sale_costs_pct * 100) if default_inputs else 2.0,
            step=0.25
        ) / 100
        discount_rate = st.slider(
            "Discount Rate for NPV (%)",
            min_value=1.0,
            max_value=20.0,
            value=float(default_inputs.discount_rate * 100) if default_inputs else 12.0,
            step=0.5
        ) / 100
    
    return PropertyInputs(
        building_size=building_size,
        purchase_price=purchase_price,
        closing_costs_pct=closing_costs_pct,
        down_payment_pct=down_payment_pct,
        interest_rate=interest_rate,
        loan_term_years=loan_term_years,
        annual_rent_psf=annual_rent_psf,
        rent_growth_rate=rent_growth_rate,
        stabilized_occupancy=stabilized_occupancy,
        year1_occupancy=year1_occupancy,
        other_income_pct=other_income_pct,
        property_tax_psf=property_tax_psf,
        insurance_psf=insurance_psf,
        cam_psf=cam_psf,
        property_mgmt_pct=property_mgmt_pct,
        leasing_commission_pct=leasing_commission_pct,
        repairs_maintenance=repairs_maintenance,
        capex_reserve_psf=capex_reserve_psf,
        initial_ti=initial_ti,
        hold_period_years=hold_period_years,
        exit_cap_rate=exit_cap_rate,
        sale_costs_pct=sale_costs_pct,
        discount_rate=discount_rate
    )


def display_acquisition_summary(inputs: PropertyInputs):
    """Display acquisition cost summary"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Purchase Price", f"${inputs.purchase_price:,.0f}")
        st.metric("Price per SF", f"${inputs.price_per_sf:.2f}")
    
    with col2:
        st.metric("Building Size", f"{inputs.building_size:,.0f} SF")
        st.metric("Closing Costs", f"${inputs.purchase_price * inputs.closing_costs_pct:,.0f}")
    
    with col3:
        st.metric("Total Acquisition", f"${inputs.total_acquisition_cost:,.0f}")
        st.metric("Equity Required", f"${inputs.equity_required:,.0f}")
    
    with col4:
        st.metric("Loan Amount", f"${inputs.loan_amount:,.0f}")
        st.metric("Annual Debt Service", f"${inputs.annual_debt_service:,.0f}")


def display_key_metrics(returns: Dict):
    """Display key investment return metrics"""
    st.markdown('<div class="sub-header">Key Investment Metrics</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "IRR",
            f"{returns['irr']*100:.2f}%",
            help="Internal Rate of Return"
        )
    
    with col2:
        st.metric(
            "Equity Multiple",
            f"{returns['equity_multiple']:.2f}x",
            help="Total cash returned / Equity invested"
        )
    
    with col3:
        st.metric(
            "Avg Cash-on-Cash",
            f"{returns['avg_cash_on_cash']*100:.2f}%",
            help="Average annual cash return on equity"
        )
    
    with col4:
        st.metric(
            "NPV",
            f"${returns['npv']:,.0f}",
            help="Net Present Value"
        )
    
    with col5:
        st.metric(
            "Total Profit",
            f"${returns['total_profit']:,.0f}",
            help="Total cash returned - Equity invested"
        )
    
    # Year 1 metrics
    st.markdown('<div class="sub-header">Year 1 Metrics</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Year 1 NOI", f"${returns['year1_noi']:,.0f}")
    
    with col2:
        st.metric("Going-In Cap Rate", f"{returns['going_in_cap_rate']*100:.2f}%")
    
    with col3:
        st.metric("Year 1 DSCR", f"{returns['year1_dscr']:.2f}")
    
    with col4:
        st.metric("Year 1 Cash-on-Cash", f"{returns['year1_coc']*100:.2f}%")


def plot_noi_trend(pro_forma: pd.DataFrame):
    """Plot NOI trend over hold period"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=pro_forma['Year'],
        y=pro_forma['NOI'],
        mode='lines+markers',
        name='NOI',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='Net Operating Income (NOI) Projection',
        xaxis_title='Year',
        yaxis_title='NOI ($)',
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    fig.update_yaxes(tickformat='$,.0f')
    
    return fig


def plot_cash_flow_waterfall(returns: Dict, inputs: PropertyInputs):
    """Plot cash flow waterfall chart"""
    values = [
        inputs.equity_required,
        returns['total_cash_flow'],
        returns['net_cash_from_sale'],
        -returns['total_cash_returned']
    ]
    
    labels = [
        'Initial Equity',
        'Operating Cash Flow',
        'Sale Proceeds',
        'Total Return'
    ]
    
    fig = go.Figure(go.Waterfall(
        x=labels,
        y=values,
        measure=['relative', 'relative', 'relative', 'total'],
        text=[f'${v:,.0f}' for v in values],
        textposition='outside',
        connector={'line': {'color': 'rgb(63, 63, 63)'}},
        decreasing={'marker': {'color': '#d62728'}},
        increasing={'marker': {'color': '#2ca02c'}},
        totals={'marker': {'color': '#1f77b4'}}
    ))
    
    fig.update_layout(
        title='Cash Flow Waterfall',
        yaxis_title='Amount ($)',
        template='plotly_white',
        height=400,
        showlegend=False
    )
    
    fig.update_yaxes(tickformat='$,.0f')
    
    return fig


def plot_revenue_expense_stack(pro_forma: pd.DataFrame):
    """Plot stacked revenue and expenses"""
    fig = go.Figure()
    
    years = pro_forma['Year'].tolist()
    
    # Revenue
    fig.add_trace(go.Bar(
        x=years,
        y=pro_forma['Total_Revenue'],
        name='Total Revenue',
        marker_color='#2ca02c'
    ))
    
    # Expenses
    fig.add_trace(go.Bar(
        x=years,
        y=pro_forma['Total_Landlord_Expenses'],
        name='Operating Expenses',
        marker_color='#d62728'
    ))
    
    # NOI line
    fig.add_trace(go.Scatter(
        x=years,
        y=pro_forma['NOI'],
        name='NOI',
        mode='lines+markers',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title='Revenue, Expenses & NOI',
        xaxis_title='Year',
        yaxis_title='Amount ($)',
        yaxis2=dict(
            title='NOI ($)',
            overlaying='y',
            side='right'
        ),
        hovermode='x unified',
        template='plotly_white',
        height=450,
        barmode='group'
    )
    
    fig.update_yaxes(tickformat='$,.0f')
    
    return fig


def plot_cumulative_cash_flow(pro_forma: pd.DataFrame, inputs: PropertyInputs):
    """Plot cumulative cash flow"""
    cash_flows = pro_forma['Pre_Tax_Cash_Flow'].tolist()
    cumulative = np.cumsum(cash_flows)
    
    # Adjust for initial equity investment
    cumulative = cumulative - inputs.equity_required
    
    fig = go.Figure()
    
    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    
    fig.add_trace(go.Scatter(
        x=pro_forma['Year'],
        y=cumulative,
        mode='lines+markers',
        name='Cumulative Cash Flow',
        fill='tozeroy',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='Cumulative Cash Flow (After Initial Equity)',
        xaxis_title='Year',
        yaxis_title='Cumulative Cash Flow ($)',
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    fig.update_yaxes(tickformat='$,.0f')
    
    return fig


def create_sensitivity_table(inputs: PropertyInputs, param1: str, param2: str, 
                             metric: str, param1_range: List[float], 
                             param2_range: List[float]) -> pd.DataFrame:
    """Create sensitivity analysis table"""
    results = []
    
    for p1_val in param1_range:
        row = {}
        for p2_val in param2_range:
            # Create modified inputs
            modified_inputs = PropertyInputs(**inputs.__dict__)
            setattr(modified_inputs, param1, p1_val)
            setattr(modified_inputs, param2, p2_val)
            
            # Calculate returns
            analyzer = CREAnalyzer(modified_inputs)
            analyzer.calculate_pro_forma()
            returns = analyzer.calculate_returns()
            
            # Get metric value
            if metric == 'IRR':
                value = returns['irr'] * 100
            elif metric == 'Cash-on-Cash':
                value = returns['year1_coc'] * 100
            elif metric == 'Equity Multiple':
                value = returns['equity_multiple']
            elif metric == 'NPV':
                value = returns['npv']
            else:
                value = 0
            
            row[f"{p2_val}"] = value
        
        row['index'] = p1_val
        results.append(row)
    
    df = pd.DataFrame(results).set_index('index')
    return df


def display_sensitivity_analysis(inputs: PropertyInputs):
    """Display interactive sensitivity analysis"""
    st.markdown('<div class="sub-header">Sensitivity Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**IRR Sensitivity: Exit Cap Rate vs Purchase Price**")
        
        # Define ranges
        purchase_prices = np.linspace(
            inputs.purchase_price * 0.8,
            inputs.purchase_price * 1.2,
            5
        )
        exit_cap_rates = np.linspace(0.055, 0.075, 5)
        
        sens_df = create_sensitivity_table(
            inputs,
            'exit_cap_rate',
            'purchase_price',
            'IRR',
            exit_cap_rates,
            purchase_prices
        )
        
        # Format as heatmap
        fig1 = go.Figure(data=go.Heatmap(
            z=sens_df.values,
            x=[f"${p/1e6:.1f}M" for p in purchase_prices],
            y=[f"{r*100:.1f}%" for r in exit_cap_rates],
            colorscale='RdYlGn',
            text=np.round(sens_df.values, 2),
            texttemplate='%{text}%',
            textfont={"size": 10},
            colorbar=dict(title="IRR (%)")
        ))
        
        fig1.update_layout(
            xaxis_title='Purchase Price',
            yaxis_title='Exit Cap Rate',
            height=350
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("**Cash-on-Cash: Rent/SF vs Occupancy**")
        
        # Define ranges
        rents = np.linspace(
            inputs.annual_rent_psf * 0.85,
            inputs.annual_rent_psf * 1.15,
            5
        )
        occupancies = np.linspace(0.85, 1.0, 5)
        
        sens_df2 = create_sensitivity_table(
            inputs,
            'year1_occupancy',
            'annual_rent_psf',
            'Cash-on-Cash',
            occupancies,
            rents
        )
        
        fig2 = go.Figure(data=go.Heatmap(
            z=sens_df2.values,
            x=[f"${r:.1f}" for r in rents],
            y=[f"{o*100:.0f}%" for o in occupancies],
            colorscale='RdYlGn',
            text=np.round(sens_df2.values, 2),
            texttemplate='%{text}%',
            textfont={"size": 10},
            colorbar=dict(title="CoC (%)")
        ))
        
        fig2.update_layout(
            xaxis_title='Rent per SF',
            yaxis_title='Year 1 Occupancy',
            height=350
        )
        
        st.plotly_chart(fig2, use_container_width=True)


def display_pro_forma_table(pro_forma: pd.DataFrame):
    """Display detailed pro forma table"""
    st.markdown('<div class="sub-header">Detailed Pro Forma</div>', unsafe_allow_html=True)
    
    # Select key columns to display
    display_columns = [
        'Year', 'Gross_Rental_Income', 'Other_Income', 'Total_Revenue',
        'Total_Landlord_Expenses', 'NOI', 'Total_CapEx', 'Debt_Service',
        'Pre_Tax_Cash_Flow', 'DSCR', 'Cash_on_Cash'
    ]
    
    display_df = pro_forma[display_columns].copy()
    
    # Format for display
    display_df['Gross_Rental_Income'] = display_df['Gross_Rental_Income'].apply(lambda x: f"${x:,.0f}")
    display_df['Other_Income'] = display_df['Other_Income'].apply(lambda x: f"${x:,.0f}")
    display_df['Total_Revenue'] = display_df['Total_Revenue'].apply(lambda x: f"${x:,.0f}")
    display_df['Total_Landlord_Expenses'] = display_df['Total_Landlord_Expenses'].apply(lambda x: f"${x:,.0f}")
    display_df['NOI'] = display_df['NOI'].apply(lambda x: f"${x:,.0f}")
    display_df['Total_CapEx'] = display_df['Total_CapEx'].apply(lambda x: f"${x:,.0f}")
    display_df['Debt_Service'] = display_df['Debt_Service'].apply(lambda x: f"${x:,.0f}")
    display_df['Pre_Tax_Cash_Flow'] = display_df['Pre_Tax_Cash_Flow'].apply(lambda x: f"${x:,.0f}")
    display_df['DSCR'] = display_df['DSCR'].apply(lambda x: f"{x:.2f}" if x > 0 else "-")
    display_df['Cash_on_Cash'] = display_df['Cash_on_Cash'].apply(lambda x: f"{x*100:.2f}%" if x != 0 else "-")
    
    # Rename columns for display
    display_df.columns = [
        'Year', 'Gross Rental', 'Other Income', 'Total Revenue',
        'Operating Exp', 'NOI', 'CapEx', 'Debt Service',
        'Pre-Tax CF', 'DSCR', 'CoC %'
    ]
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)


def main():
    """Main application"""
    st.markdown('<h1 class="main-header">Commercial Real Estate Investment Analyzer</h1>', 
                unsafe_allow_html=True)
    
    # Create inputs
    inputs = create_inputs_sidebar()
    
    # Handle pending save
    if st.session_state.get('pending_save'):
        save_name = st.session_state.pending_save
        try:
            filename = save_scenario(inputs, save_name)
            st.session_state.scenario_name = save_name
            st.sidebar.success(f"Saved as: {save_name}")
            del st.session_state.pending_save
        except Exception as e:
            st.sidebar.error(f"Error saving scenario: {str(e)}")
    
    # Calculate analysis
    analyzer = CREAnalyzer(inputs)
    pro_forma = analyzer.calculate_pro_forma()
    returns = analyzer.calculate_returns()
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Executive Summary",
        "Cash Flow Analysis",
        "Sensitivity Analysis",
        "Detailed Pro Forma"
    ])
    
    with tab1:
        st.markdown('<div class="sub-header">Investment Overview</div>', unsafe_allow_html=True)
        display_acquisition_summary(inputs)
        
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        display_key_metrics(returns)
        
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(plot_noi_trend(pro_forma), use_container_width=True)
        
        with col2:
            st.plotly_chart(plot_cash_flow_waterfall(returns, inputs), use_container_width=True)
        
        # Exit analysis
        st.markdown('<div class="sub-header">Exit Analysis</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Gross Sale Price", f"${returns['gross_sale_price']:,.0f}")
        
        with col2:
            st.metric("Sale Costs", f"${returns['sale_costs']:,.0f}")
        
        with col3:
            st.metric("Loan Balance", f"${returns['loan_balance']:,.0f}")
        
        with col4:
            st.metric("Net Cash from Sale", f"${returns['net_cash_from_sale']:,.0f}")
    
    with tab2:
        st.plotly_chart(plot_revenue_expense_stack(pro_forma), use_container_width=True)
        st.plotly_chart(plot_cumulative_cash_flow(pro_forma, inputs), use_container_width=True)
        
        # Cash-on-Cash by year
        st.markdown('<div class="sub-header">Annual Cash-on-Cash Returns</div>', unsafe_allow_html=True)
        coc_df = pro_forma[pro_forma['Year'] > 0][['Year', 'Cash_on_Cash']].copy()
        
        fig = px.bar(
            coc_df,
            x='Year',
            y='Cash_on_Cash',
            title='Cash-on-Cash Return by Year',
            labels={'Cash_on_Cash': 'Cash-on-Cash (%)'},
            color='Cash_on_Cash',
            color_continuous_scale='RdYlGn'
        )
        fig.update_yaxes(tickformat='.1%')
        fig.update_layout(template='plotly_white', height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        display_sensitivity_analysis(inputs)
        
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.markdown("**Sensitivity Analysis Notes**")
        st.info("""
        - **IRR Sensitivity**: Shows how your internal rate of return varies with different exit cap rates and purchase prices
        - **Cash-on-Cash Sensitivity**: Shows Year 1 cash returns based on rent per SF and occupancy levels
        - **Green** indicates higher returns, **Red** indicates lower returns
        - Use these tables to understand which variables have the greatest impact on your returns
        """)
    
    with tab4:
        display_pro_forma_table(pro_forma)
        
        # Export functionality
        st.markdown('<div class="sub-header">Export Data</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            # Export pro forma
            csv = pro_forma.to_csv(index=False)
            st.download_button(
                label="Download Pro Forma (CSV)",
                data=csv,
                file_name="pro_forma.csv",
                mime="text/csv"
            )
        
        with col2:
            # Export summary
            summary_data = {
                'Metric': [
                    'IRR', 'Equity Multiple', 'Avg Cash-on-Cash', 'NPV',
                    'Total Profit', 'Going-In Cap Rate', 'Exit Cap Rate',
                    'Year 1 NOI', 'Year 1 DSCR'
                ],
                'Value': [
                    f"{returns['irr']*100:.2f}%",
                    f"{returns['equity_multiple']:.2f}x",
                    f"{returns['avg_cash_on_cash']*100:.2f}%",
                    f"${returns['npv']:,.0f}",
                    f"${returns['total_profit']:,.0f}",
                    f"{returns['going_in_cap_rate']*100:.2f}%",
                    f"{inputs.exit_cap_rate*100:.2f}%",
                    f"${returns['year1_noi']:,.0f}",
                    f"{returns['year1_dscr']:.2f}"
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            csv_summary = summary_df.to_csv(index=False)
            st.download_button(
                label="Download Summary (CSV)",
                data=csv_summary,
                file_name="investment_summary.csv",
                mime="text/csv"
            )


if __name__ == "__main__":
    main()

