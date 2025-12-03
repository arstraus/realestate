import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Tuple, Optional
import numpy_financial as npf
import json
from pathlib import Path
from datetime import datetime
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT

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
class Tenant:
    """Individual tenant details"""
    name: str
    square_feet: float
    annual_rent_psf: float
    lease_expiration_year: int
    
    @property
    def annual_rent(self) -> float:
        return self.square_feet * self.annual_rent_psf


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
    
    # Tax Assumptions
    tax_rate: float
    land_value_pct: float
    depreciation_period: int
    
    # Exit Assumptions
    hold_period_years: int
    exit_cap_rate: float
    sale_costs_pct: float
    discount_rate: float
    
    # Tenant Details (with defaults - must be last)
    use_detailed_tenants: bool = False
    tenants: List[Tenant] = field(default_factory=list)
    
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


def analyze_debt_optimization(base_inputs: PropertyInputs) -> pd.DataFrame:
    """Analyze IRR across different leverage levels"""
    results = []
    
    # Test leverage from 0% to 90% in 5% increments
    for ltv in np.arange(0.0, 0.95, 0.05):
        # Create modified inputs with different leverage
        test_inputs = PropertyInputs(**asdict(base_inputs))
        test_inputs.down_payment_pct = 1 - ltv
        
        # Skip if down payment is less than minimum
        if test_inputs.down_payment_pct < 0.05:
            continue
        
        # Calculate returns
        try:
            analyzer = CREAnalyzer(test_inputs)
            analyzer.calculate_pro_forma()
            returns = analyzer.calculate_returns()
            
            # Collect metrics
            results.append({
                'LTV': ltv * 100,
                'Down_Payment_Pct': test_inputs.down_payment_pct * 100,
                'Equity_Required': test_inputs.equity_required,
                'Loan_Amount': test_inputs.loan_amount,
                'After_Tax_IRR': returns['after_tax_irr'] * 100,
                'Pre_Tax_IRR': returns['pre_tax_irr'] * 100,
                'After_Tax_EM': returns['after_tax_equity_multiple'],
                'Year1_DSCR': returns['year1_dscr'],
                'After_Tax_CoC': returns['year1_after_tax_coc'] * 100,
                'Debt_Service': test_inputs.annual_debt_service
            })
        except:
            # Skip if calculation fails (e.g., negative cash flow)
            continue
    
    return pd.DataFrame(results)


def generate_pdf_report(inputs: PropertyInputs, returns: Dict, pro_forma: pd.DataFrame) -> bytes:
    """Generate PDF executive summary report"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           topMargin=0.5*inch, bottomMargin=0.5*inch,
                           leftMargin=0.75*inch, rightMargin=0.75*inch)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1a202c'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    # Title
    elements.append(Paragraph("Commercial Real Estate", title_style))
    elements.append(Paragraph("Investment Analysis Summary", title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Property Overview
    elements.append(Paragraph("Property Overview", heading_style))
    property_data = [
        ['Building Size', f"{inputs.building_size:,.0f} SF"],
        ['Purchase Price', f"${inputs.purchase_price:,.0f}"],
        ['Price per SF', f"${inputs.price_per_sf:.2f}"],
        ['Total Acquisition Cost', f"${inputs.total_acquisition_cost:,.0f}"],
    ]
    
    property_table = Table(property_data, colWidths=[3*inch, 2*inch])
    property_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f7fafc')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1a202c')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0'))
    ]))
    elements.append(property_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Financing Structure
    elements.append(Paragraph("Financing Structure", heading_style))
    financing_data = [
        ['Equity Required', f"${inputs.equity_required:,.0f}"],
        ['Loan Amount', f"${inputs.loan_amount:,.0f}"],
        ['LTV', f"{(1-inputs.down_payment_pct)*100:.1f}%"],
        ['Interest Rate', f"{inputs.interest_rate*100:.2f}%"],
        ['Loan Term', f"{inputs.loan_term_years} years"],
        ['Annual Debt Service', f"${inputs.annual_debt_service:,.0f}"],
    ]
    
    financing_table = Table(financing_data, colWidths=[3*inch, 2*inch])
    financing_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f7fafc')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1a202c')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0'))
    ]))
    elements.append(financing_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Investment Returns - After-Tax
    elements.append(Paragraph("After-Tax Investment Returns", heading_style))
    returns_data = [
        ['After-Tax IRR', f"{returns['after_tax_irr']*100:.2f}%"],
        ['Equity Multiple', f"{returns['after_tax_equity_multiple']:.2f}x"],
        ['Avg Cash-on-Cash', f"{returns['after_tax_avg_coc']*100:.2f}%"],
        ['After-Tax NPV', f"${returns['after_tax_npv']:,.0f}"],
        ['Total Profit', f"${returns['after_tax_profit']:,.0f}"],
    ]
    
    returns_table = Table(returns_data, colWidths=[3*inch, 2*inch])
    returns_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f4ff')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1a202c')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTSIZE', (1, 0), (1, 0), 12),
        ('TEXTCOLOR', (1, 0), (1, 0), colors.HexColor('#667eea')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0'))
    ]))
    elements.append(returns_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Year 1 Metrics
    elements.append(Paragraph("Year 1 Performance Metrics", heading_style))
    year1_data = [
        ['Year 1 NOI', f"${returns['year1_noi']:,.0f}"],
        ['Going-In Cap Rate', f"{returns['going_in_cap_rate']*100:.2f}%"],
        ['Year 1 DSCR', f"{returns['year1_dscr']:.2f}"],
        ['Year 1 After-Tax CoC', f"{returns['year1_after_tax_coc']*100:.2f}%"],
    ]
    
    year1_table = Table(year1_data, colWidths=[3*inch, 2*inch])
    year1_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f7fafc')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1a202c')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0'))
    ]))
    elements.append(year1_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Exit Analysis
    elements.append(Paragraph("Exit Analysis", heading_style))
    exit_data = [
        ['Gross Sale Price', f"${returns['gross_sale_price']:,.0f}"],
        ['Net Sale Proceeds', f"${returns['net_sale_proceeds']:,.0f}"],
        ['Loan Balance at Exit', f"${returns['loan_balance']:,.0f}"],
        ['Total Tax on Sale', f"${returns['total_tax_on_sale']:,.0f}"],
        ['Net Cash from Sale', f"${returns['net_cash_from_sale']:,.0f}"],
    ]
    
    exit_table = Table(exit_data, colWidths=[3*inch, 2*inch])
    exit_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f7fafc')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1a202c')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0'))
    ]))
    elements.append(exit_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Add footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#64748b'),
        alignment=TA_CENTER
    )
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", footer_style))
    elements.append(Paragraph("Commercial Real Estate Investment Analyzer", footer_style))
    
    # Build PDF
    doc.build(elements)
    
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


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
    inputs_dict = asdict(inputs)
    
    # Convert tenant objects to dicts if present
    if 'tenants' in inputs_dict and inputs_dict['tenants']:
        inputs_dict['tenants'] = [asdict(t) if hasattr(t, '__dict__') else t for t in inputs_dict['tenants']]
    
    scenario_data = {
        'name': scenario_name,
        'created_at': datetime.now().isoformat(),
        'inputs': inputs_dict
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
    
    # Convert tenant dicts to Tenant objects if present
    if 'tenants' in inputs_dict and inputs_dict['tenants']:
        inputs_dict['tenants'] = [Tenant(**t) for t in inputs_dict['tenants']]
    else:
        inputs_dict['tenants'] = []
    
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
        
        # Calculate depreciable basis (building value only, excluding land)
        depreciable_basis = self.inputs.purchase_price * (1 - self.inputs.land_value_pct)
        annual_depreciation = depreciable_basis / self.inputs.depreciation_period
        
        # Track cumulative principal paid for loan balance calculation
        remaining_balance = self.inputs.loan_amount
        
        for year in years:
            year_data = {'Year': year}
            
            # Revenue calculations
            if self.inputs.use_detailed_tenants and self.inputs.tenants:
                # Tenant-by-tenant revenue calculation
                if year == 0:
                    gross_rental_income = 0
                    occupied_sf = 0
                    rent_psf = 0
                else:
                    gross_rental_income = 0
                    occupied_sf = 0
                    
                    for tenant in self.inputs.tenants:
                        # Check if lease has expired
                        if year <= tenant.lease_expiration_year:
                            # Tenant still in place
                            tenant_rent = tenant.annual_rent * ((1 + self.inputs.rent_growth_rate) ** (year - 1))
                            gross_rental_income += tenant_rent
                            occupied_sf += tenant.square_feet
                        else:
                            # Lease expired - assume re-leased at market after 6 months vacancy
                            market_rent = tenant.annual_rent_psf * ((1 + self.inputs.rent_growth_rate) ** (year - 1))
                            # 50% of year vacant, 50% at market
                            tenant_rent = tenant.square_feet * market_rent * 0.5
                            gross_rental_income += tenant_rent
                            occupied_sf += tenant.square_feet * 0.5
                    
                    # Calculate weighted average rent
                    rent_psf = gross_rental_income / occupied_sf if occupied_sf > 0 else 0
                
                other_income = gross_rental_income * self.inputs.other_income_pct
                total_revenue = gross_rental_income + other_income
            else:
                # Simple single-tenant/blended calculation
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
            
            # Debt Service and Amortization
            if year == 0:
                debt_service = 0
                interest_expense = 0
                principal_payment = 0
            else:
                debt_service = self.inputs.annual_debt_service
                # Calculate interest on remaining balance
                interest_expense = remaining_balance * self.inputs.interest_rate
                principal_payment = debt_service - interest_expense
                # Update remaining balance for next year
                remaining_balance -= principal_payment
            
            # Tax Calculations
            if year == 0:
                depreciation = 0
                taxable_income = 0
                tax_liability = 0
            else:
                depreciation = annual_depreciation
                # Taxable Income = NOI - Interest - Depreciation
                taxable_income = noi - interest_expense - depreciation
                # Tax only on positive taxable income
                tax_liability = max(0, taxable_income * self.inputs.tax_rate)
            
            # Cash Flow Calculations
            pre_tax_cash_flow = noi - debt_service - total_capex
            after_tax_cash_flow = pre_tax_cash_flow - tax_liability
            
            # Debt metrics
            if year > 0 and debt_service > 0:
                dscr = noi / debt_service
                pre_tax_coc = pre_tax_cash_flow / self.inputs.equity_required
                after_tax_coc = after_tax_cash_flow / self.inputs.equity_required
            else:
                dscr = 0
                pre_tax_coc = 0
                after_tax_coc = 0
            
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
                'Interest_Expense': interest_expense,
                'Principal_Payment': principal_payment,
                'Loan_Balance': remaining_balance,
                'Depreciation': depreciation,
                'Taxable_Income': taxable_income,
                'Tax_Liability': tax_liability,
                'Pre_Tax_Cash_Flow': pre_tax_cash_flow,
                'After_Tax_Cash_Flow': after_tax_cash_flow,
                'DSCR': dscr,
                'Pre_Tax_CoC': pre_tax_coc,
                'After_Tax_CoC': after_tax_coc
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
        
        # Loan balance at exit (from pro forma tracking)
        loan_balance = self.pro_forma.loc[final_year, 'Loan_Balance']
        
        # Calculate tax on sale
        # Capital Gain = Sale Price - Original Basis
        original_basis = self.inputs.purchase_price
        capital_gain = gross_sale_price - original_basis
        
        # Depreciation Recapture
        total_depreciation = self.pro_forma.loc[1:final_year, 'Depreciation'].sum()
        depreciation_recapture = total_depreciation
        
        # Tax on sale (simplified: depreciation recapture at 25%, capital gains at ordinary rate)
        depreciation_recapture_tax = depreciation_recapture * 0.25
        capital_gains_tax = (capital_gain - depreciation_recapture) * self.inputs.tax_rate
        total_tax_on_sale = depreciation_recapture_tax + capital_gains_tax
        
        # Net cash from sale (after paying off loan and taxes)
        net_cash_from_sale = net_sale_proceeds - loan_balance - total_tax_on_sale
        
        # Pre-Tax Return calculations
        pre_tax_total_cash_flow = self.pro_forma.loc[1:final_year, 'Pre_Tax_Cash_Flow'].sum()
        pre_tax_cash_flows = [-self.inputs.equity_required]
        pre_tax_cash_flows.extend(self.pro_forma.loc[1:final_year, 'Pre_Tax_Cash_Flow'].tolist())
        pre_tax_cash_flows[-1] += (net_sale_proceeds - loan_balance)  # Pre-tax sale proceeds
        
        pre_tax_total_returned = pre_tax_total_cash_flow + (net_sale_proceeds - loan_balance)
        pre_tax_profit = pre_tax_total_returned - self.inputs.equity_required
        pre_tax_equity_multiple = pre_tax_total_returned / self.inputs.equity_required
        pre_tax_avg_coc = self.pro_forma.loc[1:final_year, 'Pre_Tax_CoC'].mean()
        pre_tax_irr = npf.irr(pre_tax_cash_flows)
        pre_tax_npv = npf.npv(self.inputs.discount_rate, pre_tax_cash_flows)
        
        # After-Tax Return calculations
        after_tax_total_cash_flow = self.pro_forma.loc[1:final_year, 'After_Tax_Cash_Flow'].sum()
        after_tax_cash_flows = [-self.inputs.equity_required]
        after_tax_cash_flows.extend(self.pro_forma.loc[1:final_year, 'After_Tax_Cash_Flow'].tolist())
        after_tax_cash_flows[-1] += net_cash_from_sale  # After-tax sale proceeds
        
        after_tax_total_returned = after_tax_total_cash_flow + net_cash_from_sale
        after_tax_profit = after_tax_total_returned - self.inputs.equity_required
        after_tax_equity_multiple = after_tax_total_returned / self.inputs.equity_required
        after_tax_avg_coc = self.pro_forma.loc[1:final_year, 'After_Tax_CoC'].mean()
        after_tax_irr = npf.irr(after_tax_cash_flows)
        after_tax_npv = npf.npv(self.inputs.discount_rate, after_tax_cash_flows)
        
        # Year 1 metrics
        year1_noi = self.pro_forma.loc[1, 'NOI']
        going_in_cap_rate = year1_noi / self.inputs.purchase_price
        year1_dscr = self.pro_forma.loc[1, 'DSCR']
        year1_pre_tax_coc = self.pro_forma.loc[1, 'Pre_Tax_CoC']
        year1_after_tax_coc = self.pro_forma.loc[1, 'After_Tax_CoC']
        
        self.returns = {
            'year_after_noi': year_after_noi,
            'gross_sale_price': gross_sale_price,
            'sale_costs': sale_costs,
            'net_sale_proceeds': net_sale_proceeds,
            'loan_balance': loan_balance,
            'total_depreciation': total_depreciation,
            'depreciation_recapture_tax': depreciation_recapture_tax,
            'capital_gains_tax': capital_gains_tax,
            'total_tax_on_sale': total_tax_on_sale,
            'net_cash_from_sale': net_cash_from_sale,
            
            # Pre-Tax Returns
            'pre_tax_total_cash_flow': pre_tax_total_cash_flow,
            'pre_tax_total_returned': pre_tax_total_returned,
            'pre_tax_profit': pre_tax_profit,
            'pre_tax_equity_multiple': pre_tax_equity_multiple,
            'pre_tax_avg_coc': pre_tax_avg_coc,
            'pre_tax_irr': pre_tax_irr,
            'pre_tax_npv': pre_tax_npv,
            
            # After-Tax Returns
            'after_tax_total_cash_flow': after_tax_total_cash_flow,
            'after_tax_total_returned': after_tax_total_returned,
            'after_tax_profit': after_tax_profit,
            'after_tax_equity_multiple': after_tax_equity_multiple,
            'after_tax_avg_coc': after_tax_avg_coc,
            'after_tax_irr': after_tax_irr,
            'after_tax_npv': after_tax_npv,
            
            # Year 1 Metrics
            'year1_noi': year1_noi,
            'going_in_cap_rate': going_in_cap_rate,
            'year1_dscr': year1_dscr,
            'year1_pre_tax_coc': year1_pre_tax_coc,
            'year1_after_tax_coc': year1_after_tax_coc,
            
            # For backwards compatibility
            'total_cash_flow': after_tax_total_cash_flow,
            'total_cash_returned': after_tax_total_returned,
            'total_profit': after_tax_profit,
            'equity_multiple': after_tax_equity_multiple,
            'avg_cash_on_cash': after_tax_avg_coc,
            'irr': after_tax_irr,
            'npv': after_tax_npv,
            'year1_coc': year1_after_tax_coc,
            'cash_flows': after_tax_cash_flows
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
        use_detailed_tenants = st.checkbox(
            "Use Detailed Tenant Input",
            value=default_inputs.use_detailed_tenants if default_inputs else False,
            help="Model individual tenants with specific lease terms"
        )
        
        tenants = []
        
        if use_detailed_tenants:
            st.markdown("**Tenant Details**")
            num_tenants = st.number_input("Number of Tenants", min_value=1, max_value=20, value=1, step=1)
            
            for i in range(num_tenants):
                st.markdown(f"*Tenant {i+1}*")
                col1, col2 = st.columns(2)
                with col1:
                    tenant_sf = st.number_input(
                        f"SF",
                        min_value=0,
                        value=int(building_size / num_tenants) if building_size else 10000,
                        step=1000,
                        key=f"tenant_{i}_sf"
                    )
                    tenant_rent = st.number_input(
                        f"Rent/SF ($)",
                        min_value=0.0,
                        value=18.0,
                        step=0.5,
                        key=f"tenant_{i}_rent"
                    )
                with col2:
                    tenant_name = st.text_input(
                        f"Name",
                        value=f"Tenant {i+1}",
                        key=f"tenant_{i}_name"
                    )
                    lease_exp = st.number_input(
                        f"Lease Exp (Year)",
                        min_value=1,
                        max_value=30,
                        value=5,
                        step=1,
                        key=f"tenant_{i}_exp"
                    )
                
                tenants.append(Tenant(
                    name=tenant_name,
                    square_feet=tenant_sf,
                    annual_rent_psf=tenant_rent,
                    lease_expiration_year=lease_exp
                ))
            
            # Show total
            total_sf = sum(t.square_feet for t in tenants)
            total_rent = sum(t.annual_rent for t in tenants)
            avg_rent_psf = total_rent / total_sf if total_sf > 0 else 0
            
            st.metric("Total Leased SF", f"{total_sf:,.0f}")
            st.metric("Avg Rent/SF", f"${avg_rent_psf:.2f}")
            
            # Use weighted average for blended calculations
            annual_rent_psf = avg_rent_psf
            year1_occupancy = total_sf / building_size if building_size > 0 else 0.9
            stabilized_occupancy = year1_occupancy
        else:
            # Simple mode
            annual_rent_psf = st.number_input(
                "Annual Base Rent per SF (NNN) ($)",
                min_value=1.0,
                value=float(default_inputs.annual_rent_psf) if default_inputs else 18.0,
                step=0.5
            )
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
        
        rent_growth_rate = st.slider(
            "Rent Growth Rate (Annual %)",
            min_value=0.0,
            max_value=10.0,
            value=float(default_inputs.rent_growth_rate * 100) if default_inputs else 3.0,
            step=0.25
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
    
    with st.sidebar.expander("TAX ASSUMPTIONS (LLC)", expanded=True):
        st.markdown("*LLC is typically pass-through to owner's tax rate*")
        tax_rate = st.slider(
            "Tax Rate (%)",
            min_value=0.0,
            max_value=50.0,
            value=float(default_inputs.tax_rate * 100) if default_inputs else 37.0,
            step=1.0,
            help="Combined federal + state tax rate (e.g., 37% federal + state)"
        ) / 100
        land_value_pct = st.slider(
            "Land Value (% of Purchase Price)",
            min_value=0.0,
            max_value=50.0,
            value=float(default_inputs.land_value_pct * 100) if default_inputs else 20.0,
            step=5.0,
            help="Land is not depreciable; typical range 15-25%"
        ) / 100
        depreciation_period = st.number_input(
            "Depreciation Period (Years)",
            min_value=1,
            max_value=50,
            value=int(default_inputs.depreciation_period) if default_inputs else 39,
            step=1,
            help="Commercial real estate: 39 years (IRS)"
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
        use_detailed_tenants=use_detailed_tenants,
        tenants=tenants,
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
        tax_rate=tax_rate,
        land_value_pct=land_value_pct,
        depreciation_period=depreciation_period,
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
    st.markdown('<div class="sub-header">After-Tax Investment Returns</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "After-Tax IRR",
            f"{returns['after_tax_irr']*100:.2f}%",
            help="Internal Rate of Return (after taxes)"
        )
    
    with col2:
        st.metric(
            "Equity Multiple",
            f"{returns['after_tax_equity_multiple']:.2f}x",
            help="Total after-tax cash / Equity invested"
        )
    
    with col3:
        st.metric(
            "Avg Cash-on-Cash",
            f"{returns['after_tax_avg_coc']*100:.2f}%",
            help="Average annual after-tax cash return"
        )
    
    with col4:
        st.metric(
            "After-Tax NPV",
            f"${returns['after_tax_npv']:,.0f}",
            help="Net Present Value (after taxes)"
        )
    
    with col5:
        st.metric(
            "Total Profit",
            f"${returns['after_tax_profit']:,.0f}",
            help="Total after-tax profit"
        )
    
    # Pre-Tax Comparison
    st.markdown('<div class="sub-header">Pre-Tax Returns (for comparison)</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Pre-Tax IRR",
            f"{returns['pre_tax_irr']*100:.2f}%",
            delta=f"{(returns['pre_tax_irr'] - returns['after_tax_irr'])*100:.2f}%",
            delta_color="off"
        )
    
    with col2:
        st.metric(
            "Pre-Tax Multiple",
            f"{returns['pre_tax_equity_multiple']:.2f}x",
            delta=f"{(returns['pre_tax_equity_multiple'] - returns['after_tax_equity_multiple']):.2f}x",
            delta_color="off"
        )
    
    with col3:
        st.metric(
            "Pre-Tax CoC",
            f"{returns['pre_tax_avg_coc']*100:.2f}%",
            delta=f"{(returns['pre_tax_avg_coc'] - returns['after_tax_avg_coc'])*100:.2f}%",
            delta_color="off"
        )
    
    with col4:
        total_taxes = returns['pre_tax_profit'] - returns['after_tax_profit']
        st.metric(
            "Total Taxes Paid",
            f"${total_taxes:,.0f}",
            help="Total tax liability over hold period + exit"
        )
    
    # Year 1 metrics
    st.markdown('<div class="sub-header">Year 1 Metrics</div>', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Year 1 NOI", f"${returns['year1_noi']:,.0f}")
    
    with col2:
        st.metric("Going-In Cap Rate", f"{returns['going_in_cap_rate']*100:.2f}%")
    
    with col3:
        st.metric("Year 1 DSCR", f"{returns['year1_dscr']:.2f}")
    
    with col4:
        st.metric(
            "Y1 After-Tax CoC", 
            f"{returns['year1_after_tax_coc']*100:.2f}%",
            help="Year 1 After-Tax Cash-on-Cash"
        )
    
    with col5:
        st.metric(
            "Y1 Pre-Tax CoC", 
            f"{returns['year1_pre_tax_coc']*100:.2f}%",
            help="Year 1 Pre-Tax Cash-on-Cash"
        )


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


def plot_annual_cash_flow(pro_forma: pd.DataFrame):
    """Plot annual cash flow distribution (pre-tax and after-tax)"""
    # Filter out Year 0
    annual_df = pro_forma[pro_forma['Year'] > 0].copy()
    
    fig = go.Figure()
    
    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    
    # Pre-tax cash flow
    fig.add_trace(go.Bar(
        x=annual_df['Year'],
        y=annual_df['Pre_Tax_Cash_Flow'],
        name='Pre-Tax',
        marker_color='#9467bd',
        opacity=0.7
    ))
    
    # After-tax cash flow
    fig.add_trace(go.Bar(
        x=annual_df['Year'],
        y=annual_df['After_Tax_Cash_Flow'],
        name='After-Tax',
        marker_color='#667eea'
    ))
    
    fig.update_layout(
        title='Annual Cash Flow to Equity (Pre-Tax vs After-Tax)',
        xaxis_title='Year',
        yaxis_title='Cash Flow ($)',
        hovermode='x unified',
        template='plotly_white',
        height=400,
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    fig.update_yaxes(tickformat='$,.0f')
    fig.update_xaxes(dtick=1)
    
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


def compare_scenarios(current_inputs: PropertyInputs, saved_inputs: PropertyInputs) -> pd.DataFrame:
    """Compare two scenarios and return a difference dataframe"""
    
    # Calculate returns for both
    analyzer_curr = CREAnalyzer(current_inputs)
    analyzer_curr.calculate_pro_forma()
    returns_curr = analyzer_curr.calculate_returns()
    
    analyzer_saved = CREAnalyzer(saved_inputs)
    analyzer_saved.calculate_pro_forma()
    returns_saved = analyzer_saved.calculate_returns()
    
    # Define metrics to compare
    metrics = [
        ('Purchase Price', current_inputs.purchase_price, saved_inputs.purchase_price, 'currency'),
        ('Equity Required', current_inputs.equity_required, saved_inputs.equity_required, 'currency'),
        ('Loan Amount', current_inputs.loan_amount, saved_inputs.loan_amount, 'currency'),
        ('Interest Rate', current_inputs.interest_rate, saved_inputs.interest_rate, 'percent'),
        ('IRR (After-Tax)', returns_curr['after_tax_irr'], returns_saved['after_tax_irr'], 'percent'),
        ('Equity Multiple', returns_curr['after_tax_equity_multiple'], returns_saved['after_tax_equity_multiple'], 'decimal'),
        ('NPV', returns_curr['after_tax_npv'], returns_saved['after_tax_npv'], 'currency'),
        ('Avg Cash-on-Cash', returns_curr['after_tax_avg_coc'], returns_saved['after_tax_avg_coc'], 'percent'),
        ('Year 1 DSCR', returns_curr['year1_dscr'], returns_saved['year1_dscr'], 'decimal'),
        ('Total Profit', returns_curr['after_tax_profit'], returns_saved['after_tax_profit'], 'currency'),
    ]
    
    data = []
    for name, curr, saved, fmt in metrics:
        diff = curr - saved
        
        # Format values
        if fmt == 'currency':
            curr_str = f"${curr:,.0f}"
            saved_str = f"${saved:,.0f}"
            diff_str = f"${diff:,.0f}"
        elif fmt == 'percent':
            curr_str = f"{curr*100:.2f}%"
            saved_str = f"{saved*100:.2f}%"
            diff_str = f"{diff*100:.2f}%"
        else:
            curr_str = f"{curr:.2f}"
            saved_str = f"{saved:.2f}"
            diff_str = f"{diff:.2f}"
            
        data.append({
            'Metric': name,
            'Current Scenario': curr_str,
            'Saved Scenario': saved_str,
            'Difference': diff_str,
            'raw_diff': diff  # For styling
        })
        
    return pd.DataFrame(data)


def generate_investment_memo(inputs: PropertyInputs, returns: Dict) -> str:
    """Generate a rule-based investment memo"""
    
    irr = returns['after_tax_irr']
    em = returns['after_tax_equity_multiple']
    dscr = returns['year1_dscr']
    coc = returns['year1_after_tax_coc']
    
    # Analyze Deal Quality
    strengths = []
    risks = []
    
    # IRR Analysis
    if irr > 0.15:
        strengths.append(f"Strong Internal Rate of Return ({irr*100:.1f}%) exceeds typical market targets.")
    elif irr < 0.08:
        risks.append(f"IRR of {irr*100:.1f}% is below typical core real estate thresholds.")
        
    # DSCR Analysis
    if dscr < 1.20:
        risks.append(f"Year 1 DSCR of {dscr:.2f}x is below standard lender requirements (1.25x), indicating cash flow risk.")
    elif dscr > 1.5:
        strengths.append(f"Healthy debt service coverage ({dscr:.2f}x) provides significant safety margin.")
        
    # Cash Flow Analysis
    if coc < 0.04:
        risks.append(f"Low initial cash-on-cash return ({coc*100:.1f}%) means heavy reliance on appreciation.")
    elif coc > 0.08:
        strengths.append(f"Strong Year 1 cash yield ({coc*100:.1f}%) provides immediate income.")
        
    # Leverage Analysis
    ltv = 1 - inputs.down_payment_pct
    if ltv > 0.75:
        risks.append(f"High leverage ({ltv*100:.0f}% LTV) increases sensitivity to market downturns.")
    elif ltv < 0.50:
        strengths.append(f"Conservative leverage ({ltv*100:.0f}% LTV) reduces foreclosure risk.")
        
    # Recommendation
    if len(risks) == 0 and irr > 0.12:
        recommendation = "STRONG BUY"
        summary = "This investment presents a compelling opportunity with strong returns and minimal flagged risks."
    elif len(risks) > len(strengths):
        recommendation = "HOLD / PASS"
        summary = "This investment carries significant risks that may outweigh the projected returns. Re-evaluation of purchase price or financing terms is recommended."
    else:
        recommendation = "BUY (With Caution)"
        summary = "The deal shows promise but has specific risk factors that should be mitigated."
        
    # Construct Memo
    memo = f"""
### 📝 Investment Memorandum

**Recommendation: {recommendation}**

{summary}

#### 🟢 Key Strengths
"""
    for s in strengths:
        memo += f"- {s}\n"
        
    if not strengths:
        memo += "- No significant financial strengths identified based on current inputs.\n"
        
    memo += "\n#### ⚠️ Key Risks\n"
    for r in risks:
        memo += f"- {r}\n"
        
    if not risks:
        memo += "- No major financial red flags identified.\n"
        
    memo += f"""
#### 📊 Deal Metrics Summary
- **IRR**: {irr*100:.2f}%
- **Equity Multiple**: {em:.2f}x
- **Year 1 DSCR**: {dscr:.2f}x
- **Cash-on-Cash**: {coc*100:.2f}%
- **Entry Price**: ${inputs.purchase_price:,.0f} (${inputs.price_per_sf:.0f}/SF)
"""

    return memo


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
        'Year', 'Gross_Rental_Income', 'Total_Revenue', 'Total_Landlord_Expenses', 'NOI',
        'Debt_Service', 'Interest_Expense', 'Depreciation', 'Taxable_Income', 'Tax_Liability',
        'Pre_Tax_Cash_Flow', 'After_Tax_Cash_Flow', 'DSCR', 'After_Tax_CoC'
    ]
    
    display_df = pro_forma[display_columns].copy()
    
    # Format for display
    display_df['Gross_Rental_Income'] = display_df['Gross_Rental_Income'].apply(lambda x: f"${x:,.0f}")
    display_df['Total_Revenue'] = display_df['Total_Revenue'].apply(lambda x: f"${x:,.0f}")
    display_df['Total_Landlord_Expenses'] = display_df['Total_Landlord_Expenses'].apply(lambda x: f"${x:,.0f}")
    display_df['NOI'] = display_df['NOI'].apply(lambda x: f"${x:,.0f}")
    display_df['Debt_Service'] = display_df['Debt_Service'].apply(lambda x: f"${x:,.0f}")
    display_df['Interest_Expense'] = display_df['Interest_Expense'].apply(lambda x: f"${x:,.0f}")
    display_df['Depreciation'] = display_df['Depreciation'].apply(lambda x: f"${x:,.0f}")
    display_df['Taxable_Income'] = display_df['Taxable_Income'].apply(lambda x: f"${x:,.0f}")
    display_df['Tax_Liability'] = display_df['Tax_Liability'].apply(lambda x: f"${x:,.0f}")
    display_df['Pre_Tax_Cash_Flow'] = display_df['Pre_Tax_Cash_Flow'].apply(lambda x: f"${x:,.0f}")
    display_df['After_Tax_Cash_Flow'] = display_df['After_Tax_Cash_Flow'].apply(lambda x: f"${x:,.0f}")
    display_df['DSCR'] = display_df['DSCR'].apply(lambda x: f"{x:.2f}" if x > 0 else "-")
    display_df['After_Tax_CoC'] = display_df['After_Tax_CoC'].apply(lambda x: f"{x*100:.2f}%" if x != 0 else "-")
    
    # Rename columns for display
    display_df.columns = [
        'Year', 'Rental Income', 'Total Revenue', 'Op Expenses', 'NOI',
        'Debt Service', 'Interest', 'Depreciation', 'Taxable Inc', 'Taxes',
        'Pre-Tax CF', 'After-Tax CF', 'DSCR', 'AT CoC %'
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
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Executive Summary",
        "Cash Flow Analysis",
        "Debt Optimization",
        "Sensitivity Analysis",
        "Detailed Pro Forma",
        "⚖️ Compare",
        "🤖 AI Memo"
    ])
    
    with tab1:
        # PDF Export button at top
        col1, col2, col3 = st.columns([3, 1, 1])
        with col3:
            pdf_bytes = generate_pdf_report(inputs, returns, pro_forma)
            st.download_button(
                label="Export PDF Report",
                data=pdf_bytes,
                file_name=f"investment_summary_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )
        
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
            st.metric("Net Sale Proceeds", f"${returns['net_sale_proceeds']:,.0f}")
        
        with col3:
            st.metric("Loan Balance", f"${returns['loan_balance']:,.0f}")
        
        with col4:
            st.metric(
                "Net Cash (After Tax)", 
                f"${returns['net_cash_from_sale']:,.0f}",
                help="After paying off loan and taxes on sale"
            )
        
        # Tax details on sale
        st.markdown('<div class="sub-header">Tax on Sale Details</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Depreciation", f"${returns['total_depreciation']:,.0f}")
        
        with col2:
            st.metric("Depreciation Recapture Tax", f"${returns['depreciation_recapture_tax']:,.0f}")
        
        with col3:
            st.metric("Capital Gains Tax", f"${returns['capital_gains_tax']:,.0f}")
        
        with col4:
            st.metric("Total Tax on Sale", f"${returns['total_tax_on_sale']:,.0f}")
    
    with tab2:
        st.plotly_chart(plot_revenue_expense_stack(pro_forma), use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(plot_annual_cash_flow(pro_forma), use_container_width=True)
        
        with col2:
            st.plotly_chart(plot_cumulative_cash_flow(pro_forma, inputs), use_container_width=True)
        
        # Cash-on-Cash by year
        st.markdown('<div class="sub-header">Annual Cash-on-Cash Returns (After-Tax)</div>', unsafe_allow_html=True)
        coc_df = pro_forma[pro_forma['Year'] > 0][['Year', 'After_Tax_CoC']].copy()
        
        fig = px.bar(
            coc_df,
            x='Year',
            y='After_Tax_CoC',
            title='After-Tax Cash-on-Cash Return by Year',
            labels={'After_Tax_CoC': 'After-Tax CoC (%)'},
            color='After_Tax_CoC',
            color_continuous_scale='RdYlGn'
        )
        fig.update_yaxes(tickformat='.1%')
        fig.update_layout(template='plotly_white', height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown('<div class="sub-header">Debt Optimization Analysis</div>', unsafe_allow_html=True)
        st.info("This analysis shows how different leverage levels impact your returns. Find the optimal debt-to-equity ratio for maximum IRR while maintaining acceptable risk levels.")
        
        # Run optimization
        with st.spinner("Analyzing leverage scenarios..."):
            opt_df = analyze_debt_optimization(inputs)
        
        if not opt_df.empty:
            # Find optimal leverage
            optimal_row = opt_df.loc[opt_df['After_Tax_IRR'].idxmax()]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Optimal LTV",
                    f"{optimal_row['LTV']:.0f}%",
                    help="Loan-to-Value ratio that maximizes IRR"
                )
            
            with col2:
                st.metric(
                    "Max After-Tax IRR",
                    f"{optimal_row['After_Tax_IRR']:.2f}%",
                    help="Highest achievable IRR at optimal leverage"
                )
            
            with col3:
                st.metric(
                    "Equity at Optimal",
                    f"${optimal_row['Equity_Required']:,.0f}",
                    help="Equity required at optimal leverage"
                )
            
            with col4:
                st.metric(
                    "DSCR at Optimal",
                    f"{optimal_row['Year1_DSCR']:.2f}",
                    help="Debt service coverage at optimal leverage"
                )
            
            # IRR vs Leverage Chart
            st.markdown("**IRR vs Leverage Level**")
            
            fig = go.Figure()
            
            # After-Tax IRR line
            fig.add_trace(go.Scatter(
                x=opt_df['LTV'],
                y=opt_df['After_Tax_IRR'],
                mode='lines+markers',
                name='After-Tax IRR',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8)
            ))
            
            # Pre-Tax IRR line
            fig.add_trace(go.Scatter(
                x=opt_df['LTV'],
                y=opt_df['Pre_Tax_IRR'],
                mode='lines+markers',
                name='Pre-Tax IRR',
                line=dict(color='#9467bd', width=3, dash='dash'),
                marker=dict(size=8)
            ))
            
            # Mark optimal point
            fig.add_trace(go.Scatter(
                x=[optimal_row['LTV']],
                y=[optimal_row['After_Tax_IRR']],
                mode='markers',
                name='Optimal Point',
                marker=dict(size=15, color='#2ca02c', symbol='star')
            ))
            
            fig.update_layout(
                xaxis_title='Loan-to-Value (%)',
                yaxis_title='IRR (%)',
                hovermode='x unified',
                template='plotly_white',
                height=400,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Equity Multiple vs Leverage
            st.markdown("**Equity Multiple vs Leverage Level**")
            
            fig2 = go.Figure()
            
            fig2.add_trace(go.Scatter(
                x=opt_df['LTV'],
                y=opt_df['After_Tax_EM'],
                mode='lines+markers',
                name='After-Tax EM',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8),
                fill='tozeroy'
            ))
            
            fig2.update_layout(
                xaxis_title='Loan-to-Value (%)',
                yaxis_title='Equity Multiple (x)',
                hovermode='x unified',
                template='plotly_white',
                height=400
            )
            
            st.plotly_chart(fig2, use_container_width=True)
            
            # Risk vs Return Trade-off
            st.markdown("**Risk vs Return Trade-off**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # DSCR vs LTV
                fig3 = go.Figure()
                
                # Color code by DSCR level
                colors_dscr = ['#2ca02c' if dscr >= 1.25 else '#ff7f0e' if dscr >= 1.1 else '#d62728' 
                              for dscr in opt_df['Year1_DSCR']]
                
                fig3.add_trace(go.Scatter(
                    x=opt_df['LTV'],
                    y=opt_df['Year1_DSCR'],
                    mode='lines+markers',
                    name='DSCR',
                    line=dict(color='#ff7f0e', width=3),
                    marker=dict(size=10, color=colors_dscr)
                ))
                
                # Add DSCR threshold line
                fig3.add_hline(y=1.25, line_dash="dash", line_color="green", 
                              annotation_text="Lender Min (1.25x)")
                
                fig3.update_layout(
                    title='Debt Service Coverage Ratio',
                    xaxis_title='Loan-to-Value (%)',
                    yaxis_title='DSCR (x)',
                    template='plotly_white',
                    height=350
                )
                
                st.plotly_chart(fig3, use_container_width=True)
            
            with col2:
                # Cash-on-Cash vs LTV
                fig4 = go.Figure()
                
                fig4.add_trace(go.Scatter(
                    x=opt_df['LTV'],
                    y=opt_df['After_Tax_CoC'],
                    mode='lines+markers',
                    name='After-Tax CoC',
                    line=dict(color='#1f77b4', width=3),
                    marker=dict(size=10)
                ))
                
                fig4.update_layout(
                    title='Year 1 Cash-on-Cash Return',
                    xaxis_title='Loan-to-Value (%)',
                    yaxis_title='Cash-on-Cash (%)',
                    template='plotly_white',
                    height=350
                )
                
                st.plotly_chart(fig4, use_container_width=True)
            
            # Detailed Table
            st.markdown("**Leverage Scenario Comparison**")
            
            display_opt_df = opt_df.copy()
            display_opt_df['Current'] = display_opt_df['LTV'].apply(
                lambda x: '→' if abs(x - (1-inputs.down_payment_pct)*100) < 2 else ''
            )
            
            # Format columns
            display_opt_df['LTV'] = display_opt_df['LTV'].apply(lambda x: f"{x:.0f}%")
            display_opt_df['Equity_Required'] = display_opt_df['Equity_Required'].apply(lambda x: f"${x:,.0f}")
            display_opt_df['After_Tax_IRR'] = display_opt_df['After_Tax_IRR'].apply(lambda x: f"{x:.2f}%")
            display_opt_df['After_Tax_EM'] = display_opt_df['After_Tax_EM'].apply(lambda x: f"{x:.2f}x")
            display_opt_df['Year1_DSCR'] = display_opt_df['Year1_DSCR'].apply(lambda x: f"{x:.2f}")
            display_opt_df['After_Tax_CoC'] = display_opt_df['After_Tax_CoC'].apply(lambda x: f"{x:.2f}%")
            
            display_columns = ['Current', 'LTV', 'Equity_Required', 'After_Tax_IRR', 
                             'After_Tax_EM', 'Year1_DSCR', 'After_Tax_CoC']
            display_opt_df = display_opt_df[display_columns]
            display_opt_df.columns = ['', 'LTV', 'Equity Req', 'AT IRR', 'EM', 'DSCR', 'Y1 CoC']
            
            st.dataframe(display_opt_df, use_container_width=True, hide_index=True)
            
        else:
            st.error("Unable to generate debt optimization analysis. Please check your inputs.")
    
    with tab4:
        display_sensitivity_analysis(inputs)
        
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.markdown("**Sensitivity Analysis Notes**")
        st.info("""
        - **IRR Sensitivity**: Shows how your internal rate of return varies with different exit cap rates and purchase prices
        - **Cash-on-Cash Sensitivity**: Shows Year 1 cash returns based on rent per SF and occupancy levels
        - **Green** indicates higher returns, **Red** indicates lower returns
        - Use these tables to understand which variables have the greatest impact on your returns
        """)
    
    with tab5:
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

    with tab6:
        st.markdown('<div class="sub-header">Scenario Comparison</div>', unsafe_allow_html=True)
        
        saved_scenarios = get_saved_scenarios()
        if not saved_scenarios:
            st.warning("No saved scenarios found. Please save a scenario first to compare.")
        else:
            # Scenario selector
            scenario_options = []
            for filepath in saved_scenarios:
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        name = data.get('name', 'Unnamed')
                        scenario_options.append((name, filepath))
                except:
                    continue
            
            selected_name = st.selectbox(
                "Select Scenario to Compare Against Current Inputs",
                options=[opt[0] for opt in scenario_options]
            )
            
            if selected_name:
                # Find file path
                selected_file = next(opt[1] for opt in scenario_options if opt[0] == selected_name)
                _, saved_inputs = load_scenario(selected_file)
                
                # Generate comparison
                comp_df = compare_scenarios(inputs, saved_inputs)
                
                # Display table with styling
                st.dataframe(
                    comp_df.drop(columns=['raw_diff']),
                    use_container_width=True,
                    hide_index=True
                )
                
                # Visual comparison of IRR
                st.markdown("**IRR Comparison**")
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=['Current', 'Saved'],
                    y=[returns['after_tax_irr'], 
                       CREAnalyzer(saved_inputs).calculate_returns()['after_tax_irr']],
                    marker_color=['#667eea', '#a0aec0']
                ))
                fig.update_layout(
                    yaxis_tickformat='.1%',
                    template='plotly_white',
                    height=300,
                    title="Internal Rate of Return (IRR)"
                )
                st.plotly_chart(fig, use_container_width=True)

    with tab7:
        st.markdown('<div class="sub-header">AI Investment Memo</div>', unsafe_allow_html=True)
        st.info("This memo is automatically generated based on your deal metrics and standard underwriting criteria.")
        
        memo_text = generate_investment_memo(inputs, returns)
        st.markdown(memo_text)
        
        # Copy button (simulated with code block)
        st.markdown("### Copy to Clipboard")
        st.code(memo_text, language="markdown")


if __name__ == "__main__":
    main()

