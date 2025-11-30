# Commercial Real Estate Investment Analyzer

A professional-grade Streamlit application for analyzing commercial real estate investments, specifically designed for industrial warehouse properties with triple-net (NNN) lease structures.

## Modern, Clean Design

This application features a contemporary, distraction-free interface with:
- **Clean Typography**: Inter font family for optimal readability
- **Gradient Accents**: Sophisticated purple-blue gradient scheme
- **Card-Based Layout**: Elevated metric cards with hover effects
- **Smooth Interactions**: Subtle animations and transitions
- **Professional Aesthetic**: No emojis or icons, just pure design

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Key Metrics](#key-metrics)
- [Excel File Analysis](#excel-file-analysis)
- [Best Practices Implemented](#best-practices-implemented)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)

## ✨ Features

### 🎯 Core Functionality

- **Comprehensive Financial Analysis**: Complete 10-year pro forma with all standard CRE metrics
- **Interactive Inputs**: User-friendly sidebar with organized input categories
- **Real-time Calculations**: Instant updates as you adjust parameters
- **Multiple Visualization Options**: Professional charts and graphs using Plotly
- **Sensitivity Analysis**: Dynamic heatmaps showing how key variables impact returns
- **Scenario Management**: Save and load scenarios as JSON files for comparison
- **Export Capabilities**: Download pro forma and summary data as CSV

### 📊 Investment Metrics Calculated

#### Returns
- **IRR (Internal Rate of Return)**: True time-weighted return on investment
- **Equity Multiple**: Total cash returned divided by equity invested
- **NPV (Net Present Value)**: Present value of all cash flows
- **Average Cash-on-Cash Return**: Average annual cash return on equity
- **Total Profit**: Absolute dollar profit over hold period

#### Year 1 Metrics
- **Going-In Cap Rate**: Year 1 NOI / Purchase Price
- **Year 1 DSCR**: Debt Service Coverage Ratio
- **Year 1 Cash-on-Cash**: First year cash return percentage

#### Exit Analysis
- **Gross Sale Price**: Based on projected Year 11 NOI and exit cap rate
- **Net Sale Proceeds**: After sale costs
- **Loan Balance**: Remaining debt at exit
- **Net Cash from Sale**: Equity proceeds after paying off debt

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download

```bash
cd /path/to/your/workspace
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `streamlit>=1.28.0` - Web application framework
- `pandas>=2.0.0` - Data manipulation
- `numpy>=1.24.0` - Numerical computing
- `plotly>=5.17.0` - Interactive visualizations
- `openpyxl>=3.1.0` - Excel file handling
- `numpy-financial>=1.0.0` - Financial calculations (IRR, NPV, PMT)

### Step 3: Run the Application

```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## 📖 Usage

### Basic Workflow

1. **Adjust Inputs** in the sidebar:
   - Property Details (size, price)
   - Financing Structure (down payment, interest rate, term)
   - Revenue Assumptions (rent, growth, occupancy)
   - Operating Expenses (NNN structure)
   - Capital Expenditures
   - Exit Assumptions (hold period, exit cap rate)

2. **Review Results** across four tabs:
   - **Executive Summary**: Key metrics and overview charts
   - **Cash Flow Analysis**: Detailed revenue/expense trends
   - **Sensitivity Analysis**: Interactive heatmaps
   - **Detailed Pro Forma**: Full 10-year projection table

3. **Save Scenarios**: Click "💾 Save" to preserve your current inputs
4. **Load Scenarios**: Click "📂 Load" to retrieve saved analyses
5. **Export Data**: Download CSV files from the Detailed Pro Forma tab

### Scenario Management

#### Saving a Scenario
1. Click the **💾 Save** button in the sidebar
2. Enter a descriptive name for your scenario
3. Click **Save** to confirm
4. Scenarios are saved to the `scenarios/` folder as JSON files

#### Loading a Scenario
1. Click the **📂 Load** button in the sidebar
2. Select from the list of saved scenarios (shows name and date)
3. Click **Load** to populate all inputs
4. All parameters will update to the saved values

#### Scenario Files
- Stored in: `scenarios/[ScenarioName]_[Timestamp].json`
- Format: JSON with metadata and all input parameters
- Portable: Can be shared with team members

## 📈 Key Metrics

### Investment Returns

| Metric | Description | Good Benchmark |
|--------|-------------|----------------|
| IRR | Internal Rate of Return - annualized return accounting for time value | 12-20% for value-add, 8-12% for core |
| Equity Multiple | Total return as a multiple of invested equity | 1.5x-2.5x over 5-10 years |
| Cash-on-Cash | Annual cash flow / Equity invested | 6-12% |
| NPV | Net Present Value at discount rate | Positive NPV indicates value creation |

### Operating Metrics

| Metric | Description | Good Benchmark |
|--------|-------------|----------------|
| Going-In Cap Rate | Year 1 NOI / Purchase Price | 5-8% for industrial |
| DSCR | Debt Service Coverage Ratio (NOI / Debt Service) | > 1.25x (lenders typically require) |
| Occupancy | Percentage of building leased | 90-95% stabilized |

## 📊 Excel File Analysis

### What We Found in Your Excel Model

**Strengths:**
- ✅ Well-organized sheet structure (Inputs, Pro Forma, Returns, Sensitivity)
- ✅ Proper NNN lease structure modeling
- ✅ Standard CRE metrics (IRR, NPV, DSCR, Cap Rates)
- ✅ 10-year pro forma with escalations
- ✅ Exit analysis with cap rate assumptions

**Areas for Improvement (Now Addressed in App):**
- ❌ **No Data Validation** → ✅ Now has input validation and reasonable ranges
- ❌ **Static Analysis** → ✅ Now real-time and interactive
- ❌ **No Visualizations** → ✅ Multiple professional charts included
- ❌ **Manual Sensitivity Tables** → ✅ Dynamic heatmaps with any parameters
- ❌ **Single Scenario** → ✅ Save/load multiple scenarios for comparison
- ❌ **Limited Export** → ✅ CSV export for pro forma and summaries

## 🎨 Best Practices Implemented

### 1. **Separation of Concerns**
- Inputs: Clean sidebar organization by category
- Calculations: Dedicated `CREAnalyzer` class
- Presentation: Modular visualization functions

### 2. **Data Validation**
- Min/max ranges on all numeric inputs
- Step increments appropriate for each parameter
- Helpful tooltips and descriptions

### 3. **Professional UI/UX**
- Clean, modern interface with custom CSS
- Organized tabs for different analysis views
- Color-coded metrics (green for good, red for poor)
- Responsive layout that works on different screen sizes

### 4. **Financial Accuracy**
- Uses numpy-financial for standard financial functions
- Proper debt service calculations (PMT formula)
- Accurate loan balance amortization
- Time-weighted IRR calculations

### 5. **Code Quality**
- Type hints throughout
- Dataclasses for clean data structures
- Comprehensive docstrings
- Modular, reusable functions
- Error handling for edge cases

### 6. **Maintainability**
- Clear variable naming
- Logical code organization
- Easy to modify or extend
- Well-commented where necessary

## 📁 Project Structure

```
realestate/
├── app.py                              # Main Streamlit application
├── requirements.txt                    # Python dependencies
├── README.md                          # This file
├── warehouse_investment_model (2).xlsx # Original Excel model
├── scenarios/                         # Saved scenarios (created automatically)
│   ├── Warehouse_Bay_Area_20241130_143022.json
│   └── Conservative_Analysis_20241130_150033.json
└── analyze_excel.py                   # Excel analysis utility script
```

## 🎯 Use Cases

### 1. **Acquisition Analysis**
- Evaluate new purchase opportunities
- Compare against investment criteria
- Justify offers with detailed pro formas

### 2. **Portfolio Management**
- Track existing assets
- Model repositioning strategies
- Evaluate hold vs. sell decisions

### 3. **Investor Reporting**
- Generate professional investment summaries
- Export data for presentations
- Create scenario comparisons

### 4. **Due Diligence**
- Stress-test assumptions with sensitivity analysis
- Model various financing structures
- Evaluate risk/return tradeoffs

### 5. **Asset Management**
- Track budget vs. actual
- Model lease-up scenarios
- Plan capital improvements

## 🔧 Customization

### Modifying Inputs

To add new input parameters:

1. Add to `PropertyInputs` dataclass
2. Add UI element in `create_inputs_sidebar()`
3. Update calculations in `CREAnalyzer` methods
4. Update saved scenario compatibility

### Adding New Metrics

1. Add calculation in `calculate_returns()` method
2. Add display in `display_key_metrics()` or create new function
3. Update export functionality if needed

### Custom Visualizations

Add new chart functions following the pattern:
```python
def plot_new_chart(data: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    # Add traces
    fig.update_layout(
        title='Chart Title',
        template='plotly_white'
    )
    return fig
```

## 🐛 Troubleshooting

### Common Issues

**"Module not found" errors**
```bash
pip install -r requirements.txt
```

**Port already in use**
```bash
streamlit run app.py --server.port 8502
```

**Scenarios not saving**
- Check write permissions in project directory
- `scenarios/` folder is created automatically

**Charts not displaying**
- Clear browser cache
- Try different browser
- Update Plotly: `pip install --upgrade plotly`

## 📝 License

This project is provided as-is for commercial real estate investment analysis.

## 🤝 Contributing

Suggestions for improvements:
- Additional property types (multifamily, office, retail)
- Tax analysis (depreciation, capital gains)
- Multiple financing scenarios
- Waterfall structures for fund analysis
- Monte Carlo simulation
- Lease-by-lease modeling

## 📞 Support

For questions or issues, refer to:
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [CRE Best Practices](https://www.ccim.com/)

## 🎓 Educational Resources

### CRE Investment Fundamentals
- **Cap Rate**: NOI / Property Value (unleveraged return)
- **Cash-on-Cash**: Cash Flow / Equity (leveraged return)
- **IRR**: Time-weighted return accounting for timing of cash flows
- **DSCR**: Lender's measure of cash flow cushion
- **Equity Multiple**: Total return ignoring time value

### NNN Lease Structure
- **Tenant pays**: Property taxes, insurance, CAM
- **Landlord receives**: Base rent + expense reimbursements
- **Landlord pays**: Property management, leasing costs, major repairs

---

**Built with ❤️ for Commercial Real Estate Professionals**

