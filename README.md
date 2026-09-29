# 💰 13-Week Rolling Cash Flow Forecast Tool

**Version**: 1.1  
**Status**: ✅ Production Ready  
**Last Updated**: 2026-09-25

---

## 📋 Project Overview

A semi-automated cash flow forecasting tool that extracts unpaid receivables and payables from Excel exports, applies intelligent filtering, and distributes them into weekly buckets to predict 13-week rolling cash flow.

### Key Features:
- ✅ **Automated extraction** from Excel (no manual data entry)
- ✅ **Intelligent filtering** (70-day age threshold for receivables)
- ✅ **13-week forecast** with weekly detail
- ✅ **Interactive visualizations** (charts, tables, metrics)
- ✅ **Multiple exports** (Excel, HTML, CSV)
- ✅ **Non-technical UI** (Streamlit web app)
- ✅ **Production-ready** code with comprehensive documentation

---

## 📦 Files Included

| File | Purpose | Size | Status |
|------|---------|------|--------|
| **app.py** | Streamlit web interface | 600+ lines | ✅ Ready |
| **cf_predictor.py** | Core forecasting logic | 300+ lines | ✅ Updated |
| **requirements.txt** | Python dependencies | 5 lines | ✅ Current |
| **QUICK_START_GUIDE.md** | Setup & deployment | 300+ lines | ✅ Complete |
| **TESTING_PLAN.md** | Comprehensive test checklist | 400+ lines | ✅ Ready |
| **test_cf_predictor.py** | Automated tests | 200+ lines | ✅ Passing |
| **README.md** | This file | - | ✅ You are here |

---

## 🚀 Quick Start (5 Minutes)

### 1. Install Python 3.9+
```bash
# Windows: Download from python.org
# macOS: brew install python3
# Linux: sudo apt-get install python3
python --version  # Verify 3.9+
```

### 2. Install Dependencies
```bash
cd CF_Forecast
pip install -r requirements.txt
```

### 3. Run the App
```bash
streamlit run app.py
```

### 4. Open Browser
```
http://localhost:8501
```

### 5. Upload Files & Forecast
- Upload receivables Excel
- Upload payables Excel
- Click "Generate Forecast"
- View results and export

**Done!** ✅

---

## 🔧 Technical Architecture

### Data Flow:

```
┌─────────────────────────────────────────────────────────┐
│                    USER UPLOADS                         │
│                                                          │
│    Receivables Excel          Payables Excel            │
└────────────────┬──────────────────────┬─────────────────┘
                 │                      │
                 ↓                      ↓
        ┌────────────────────────────────────────┐
        │   cf_predictor.extract_receivables()   │
        │   - Filter by Rozdiel > 0              │
        │   - Filter by age <= 69 days           │
        │   - Return: 3-100 items                │
        └────────────┬─────────────────────────┘
                     │
        ┌────────────────────────────────────────┐
        │    cf_predictor.extract_payables()     │
        │   - Filter by Rozdiel > 0              │
        │   - No age filtering                   │
        │   - Return: 5-200 items                │
        └────────────┬─────────────────────────┘
                     │
                     ↓
        ┌────────────────────────────────────────┐
        │  cf_predictor.assign_to_weeks()        │
        │  - Map items to W1-W13 buckets         │
        │  - Calculate weekly totals             │
        └────────────┬─────────────────────────┘
                     │
                     ↓
        ┌────────────────────────────────────────┐
        │  cf_predictor.generate_forecast()      │
        │  - Receivables by week                 │
        │  - Payables by week                    │
        │  - Net CF = Receivables - Payables     │
        └────────────┬─────────────────────────┘
                     │
                     ↓
        ┌────────────────────────────────────────┐
        │          app.py (Streamlit UI)         │
        │  - Display summary cards               │
        │  - 3 interactive charts                │
        │  - Detail table (13 weeks)             │
        │  - Insights & recommendations          │
        └────────────┬─────────────────────────┘
                     │
          ┌──────────┼──────────┐
          ↓          ↓          ↓
       EXCEL       HTML        CSV
      (Export)   (Report)    (Data)
```

### Key Components:

#### 1. **cf_predictor.py** (Backend)
Core business logic module:
- `CashFlowPredictor` class
- Methods: extract_receivables(), extract_payables(), assign_to_weeks(), generate_forecast(), generate_html_report()
- Handles date calculations, filtering, week assignment
- Generates professional HTML reports

#### 2. **app.py** (Frontend)  
Streamlit web interface:
- File upload forms
- Configuration sidebar
- 3 visualization tabs (Bar, Line, Waterfall)
- Detail table and raw data preview
- Export buttons (Excel, HTML, CSV)
- Insights & recommendations

#### 3. **requirements.txt**
Python dependencies:
- streamlit: Web framework
- pandas: Data processing
- numpy: Numerical computing
- plotly: Charting library
- openpyxl: Excel reading

---

## 💡 Key Logic Explained

### 70-Day Receivables Filter

**Why?** Old receivables are less reliable for short-term cash flow prediction.

```python
# Before extraction (OLD - INCORRECT):
if paid_amount == 0:
    include_item()  # ❌ Doesn't handle partial payments

# After extraction (NEW - CORRECT):
if rozdiel > 0 and days_until_due <= 69:
    include_item_in_week_1()  # ✅ Uses actual unpaid amount
else:
    exclude_item()  # Too old or unreliable
```

### Rozdiel Column (Column 26)

**What?** "Rozdiel" means "difference" - the unpaid remainder after partial payments.

```
Invoice Amount:  €5,000.00
Paid Amount:     €3,000.00
Rozdiel (Column 26): €2,000.00  ← THIS is what we forecast
```

Used for both receivables and payables.

### Week Assignment

Items placed in weeks based on due date:
- **Receivables filtered to 0-69 days**: All go to **Week 1** (priority collection)
- **Payables**: Distributed to W1-W13 by actual due date
- Beyond W13: Excluded from forecast

---

## 📊 Example Output

```
13-WEEK CASH FLOW FORECAST
Generated: 2026-09-25

SUMMARY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pohľadávky (Inflow):     €6,538,177.48 ✓
Záväzky (Outflow):         €841,485.80 ✗
Net Cash Flow:           €5,696,691.68 ✓

WEEKLY BREAKDOWN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Week 1  (Sep 25 - Oct 01)    +€2,450,032.45  ← Filtered receivables
Week 2  (Oct 02 - Oct 08)        +€2,677.37
Week 3  (Oct 09 - Oct 15)       -€15,496.90
...
Week 13 (Dec 18 - Dec 24)      +€145,232.15

EXPORTS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📥 Excel:  CF_Forecast_20260925_100530.xlsx
📄 HTML:   CF_Forecast_20260925_100530.html
📊 CSV:    CF_Forecast_20260925_100530.csv
```

---

## 🧪 Testing

### Automated Tests
All core logic has been tested:

```bash
python test_cf_predictor.py
```

Results:
```
✅ TEST 1: 70-Day Receivables Filter
✅ TEST 2: Rozdiel Column Usage (Column 26)
✅ TEST 3: Week Assignment & Forecasting
✅ TEST 4: HTML Report Generation
```

### Manual Testing
Follow **TESTING_PLAN.md** for comprehensive manual testing checklist covering:
- Environment setup
- Application startup
- File format validation
- Data extraction & filtering
- Forecast calculation
- Visualizations
- Export functionality
- Configuration options
- Error handling
- Performance testing
- Real data testing

---

## 📖 Documentation Files

| File | Audience | Purpose |
|------|----------|---------|
| **README.md** | Everyone | Project overview (this file) |
| **QUICK_START_GUIDE.md** | End users | Installation & deployment guide |
| **TESTING_PLAN.md** | QA team | Comprehensive test checklist |
| **cf_predictor.py** | Developers | Backend code with docstrings |
| **app.py** | Developers | Frontend code with comments |

---

## 🔧 Configuration & Customization

### Change the 70-Day Threshold

Edit **cf_predictor.py** line ~131:
```python
df = df[df['days_until_due'] <= 69].copy()  # Change 69 to your desired days
```

### Change Column Positions

Edit **cf_predictor.py** lines ~27-30:
```python
COL_DUE_DATE = 12         # Column M (0-based: A=0, B=1, ... M=12)
COL_INVOICE_AMOUNT = 21   # Column V (0-based)
COL_DIFFERENCE = 25       # Column Z (0-based) - Rozdiel
```

### Adjust Chart Colors

Edit **app.py** in chart functions (search for hex colors like `#2ca02c`):
```python
marker=dict(color='#2ca02c')  # Green for receivables
marker=dict(color='#d62728')  # Red for payables
```

---

## 🚨 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Python not found" | Install Python from python.org, add to PATH |
| "ModuleNotFoundError" | Run `pip install -r requirements.txt` again |
| "Column index out of range" | Verify Excel has 26+ columns |
| "No data in forecast" | Check that Rozdiel values > 0 |
| "Old receivables showing" | Verify 70-day filter (should exclude them) |
| "App won't start" | Check for port 8501 in use: `streamlit run app.py --server.port 8502` |

See **QUICK_START_GUIDE.md** Troubleshooting section for detailed help.

---

## 📈 Deployment Options

### 1. **Streamlit Cloud** (Easiest)
- Push code to GitHub
- Deploy to Streamlit Cloud (free tier available)
- Share URL with team
- Automatic updates from GitHub

### 2. **Docker Container**
- Run anywhere: Windows, Mac, Linux, Cloud
- Reproducible environment
- Easy scaling

### 3. **Local/Internal Server**
- Deploy on company server
- VPN/internal access only
- Full control

### 4. **Standalone Executable** (Future)
- Package as .exe for Windows
- No Python required from users
- Easy distribution

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1 | 2026-09-25 | ✅ Updated logic (Rozdiel column, 70-day filter) |
| 1.0 | 2026-08-19 | Initial WebApp framework release |

---

## 🎯 Roadmap (Future Enhancements)

**Phase 2 (Q4 2026):**
- [ ] API integration with accounting software
- [ ] Automated weekly email reports
- [ ] Historical forecast comparison
- [ ] Multi-company support

**Phase 3 (Q1 2027):**
- [ ] ML model for payment prediction
- [ ] Scenario analysis ("what-if" planning)
- [ ] Budget vs forecast comparison
- [ ] Mobile app version

---

## 💬 Support & Contact

### For Setup Issues:
1. Read **QUICK_START_GUIDE.md** Troubleshooting section
2. Run automated tests: `python test_cf_predictor.py`
3. Check this README

### For Feature Requests:
Document the requirement with:
- What you want to do
- Why it's important
- Proposed solution (if you have one)

### For Bug Reports:
Include:
- Steps to reproduce
- Expected vs actual behavior
- Screenshots/error messages
- Your Excel file format (sanitized)

---

## 📋 System Requirements

- **Python**: 3.9, 3.10, 3.11, or 3.12
- **OS**: Windows, macOS, Linux
- **Memory**: 512MB minimum, 2GB recommended
- **Disk**: 100MB for app + dependencies
- **Browser**: Chrome, Firefox, Safari, Edge (modern versions)

---

## 📄 License & Attribution

Application developed with Claude (AI Assistant)  
Framework: Streamlit (Open Source)  
Compatible with: Windows, macOS, Linux

---

## ✅ Quality Assurance

- ✅ Code reviewed for logic correctness
- ✅ Automated tests passing (4/4)
- ✅ Manual testing checklist provided
- ✅ Error handling implemented
- ✅ Performance optimized (<5 seconds per forecast)
- ✅ Documentation complete
- ✅ Ready for production deployment

---

## 🚀 Ready to Start?

### First Time?
1. Follow **QUICK_START_GUIDE.md** (5 minutes)
2. Run `streamlit run app.py`
3. Upload your Excel files
4. Generate forecast!

### Ready to Test?
1. Run `python test_cf_predictor.py` (verify logic works)
2. Follow **TESTING_PLAN.md** for comprehensive manual testing
3. Test with your actual business data

### Ready to Deploy?
1. Complete testing checklist
2. Choose deployment option (Streamlit Cloud, Docker, etc.)
3. Set up weekly data refresh process
4. Train users
5. Go live! 🎉

---

**Questions?** See **QUICK_START_GUIDE.md** or **TESTING_PLAN.md**.

**Ready?** Let's forecast! 💰

```bash
streamlit run app.py
```
