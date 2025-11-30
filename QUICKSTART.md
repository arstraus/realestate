# Quick Start Guide

## Get Running in 3 Steps

### Step 1: Install Dependencies

```bash
pip install streamlit pandas numpy plotly openpyxl numpy-financial
```

### Step 2: Run the App

```bash
streamlit run app.py
```

### Step 3: Start Analyzing!

The app will open in your browser. Try these features:

## First Steps

### Adjust the Example Property
The app loads with a **$10M Industrial Warehouse** example. Modify in the sidebar:
- Building Size: 50,000 SF
- Purchase Price: $10,000,000
- Down Payment: 25%
- Rent: $18/SF NNN
- Hold Period: 10 years

### View Your Results
Navigate through the tabs:
1. **Executive Summary** - Key metrics at a glance
2. **Cash Flow Analysis** - Visualize revenue and expenses over time
3. **Sensitivity Analysis** - See how changes affect returns
4. **Detailed Pro Forma** - Full year-by-year breakdown

### Save Your Analysis
1. Click **Save** in the sidebar
2. Name it (e.g., "Downtown Warehouse Deal")
3. Scenarios are saved to `scenarios/` folder

### Load Previous Analysis
1. Click **Load** in the sidebar
2. Select from your saved scenarios
3. All inputs update automatically

## Understanding the Metrics

### Most Important Metrics

| Metric | What It Means | What's Good |
|--------|---------------|-------------|
| **IRR** | Annual return rate | 12-20% for industrial |
| **Equity Multiple** | How many times your money back | 1.8x-2.5x over 10 years |
| **Cash-on-Cash** | Year 1 cash return % | 6-10% |
| **DSCR** | Can you cover debt? | >1.25x (required by lenders) |

### Quick Interpretation

**Strong Deal Example:**
- IRR: 15%+ 
- Equity Multiple: 2.0x+
- Year 1 Cash-on-Cash: 7%+
- DSCR: 1.3x+
- Going-In Cap: 6.5-7.5%

**Red Flags:**
- IRR < 10%
- Equity Multiple < 1.5x
- DSCR < 1.25x
- Negative cash flow in Year 1

## Pro Tips

### 1. Use Sensitivity Analysis
**Before**: "Is this deal good at $10M?"  
**Better**: "At what price does IRR drop below 12%?"

→ Check the **Sensitivity Analysis** tab!

### 2. Save Multiple Scenarios
Compare different structures:
- Base Case
- Conservative (lower rent, higher vacancy)
- Aggressive (higher rent growth)
- Alternative Financing (30% vs 25% down)

### 3. Export for Presentations
- Download Pro Forma as CSV
- Take screenshots of charts
- Share scenario JSON files with team

### 4. Stress Test Assumptions
Try these variations:
- **Occupancy**: What if it's 85% instead of 95%?
- **Exit Cap**: What if cap rates expand to 7.5%?
- **Rent**: What if market rent is $16/SF not $18/SF?
- **Hold Period**: Should you sell at Year 7 vs Year 10?

## 🔄 Common Workflows

### Evaluating a New Acquisition
1. Enter actual property details
2. Use market rent data
3. Conservative occupancy (90% Year 1)
4. Realistic expense assumptions
5. Check DSCR > 1.25 for financing
6. Target IRR > hurdle rate

### Comparing Multiple Properties
1. Analyze Property A → Save as "Property_A"
2. Analyze Property B → Save as "Property_B"
3. Export both summaries to CSV
4. Compare IRR, equity multiple, risk factors

### Investor Presentation
1. Create 3 scenarios: Base, Conservative, Upside
2. Take screenshots of:
   - Key metrics
   - NOI trend chart
   - Cash flow waterfall
   - Sensitivity heatmaps
3. Export detailed pro forma
4. Save all scenarios for Q&A

### Monthly Monitoring
1. Load saved scenario for property
2. Update with actual data:
   - Current occupancy
   - Actual expenses YTD
   - New rent comps
3. Compare to original projections
4. Re-save as "Property_2024_Q4"

## ❓ FAQ

**Q: Can I analyze office or multifamily?**  
A: The app is built for industrial NNN. You can adapt by adjusting expense assumptions, but it's optimized for industrial.

**Q: How do I change the hold period?**  
A: In the sidebar under "Exit Assumptions" → "Hold Period (Years)"

**Q: What if my loan has a prepayment penalty?**  
A: The current version doesn't include prepayment penalties. You can manually adjust the "Sale Costs %" to approximate.

**Q: Can I model TI allowances?**  
A: Yes! Under "Capital Expenditures" → "Initial Tenant Improvements"

**Q: The sensitivity tables only show 5x5 grids. Can I see more?**  
A: Currently fixed at 5x5 for clarity. You can modify the code to expand the ranges.

**Q: How accurate is the loan amortization?**  
A: Uses standard financial formulas (numpy-financial) - same as Excel PMT/PV functions.

## 🛠️ Keyboard Shortcuts (Streamlit)

- `R` - Rerun the app
- `C` - Clear cache
- `?` - Show keyboard shortcuts
- `⌘/Ctrl + K` - Open command palette

## 📖 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Review the original [Excel model](warehouse_investment_model%20(2).xlsx)
- Customize inputs for your market
- Build a library of scenarios

---

**Need Help?** Check the README or Streamlit docs at https://docs.streamlit.io

