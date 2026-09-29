# 🚀 Quick Start Guide - 13-Week Cash Flow Forecast

## Prerequisites

- **Python 3.9+** installed on your computer
- **pip** (Python package manager) - comes with Python
- **Excel files** with unpaid receivables and payables data
- A command line terminal (CMD, PowerShell, or Terminal)

---

## Installation & Setup (5 minutes)

### Step 1: Install Python

**Windows:**
1. Download Python from https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT**: Check the box "Add Python to PATH" during installation
4. Click "Install Now"

**macOS:**
```bash
# Using Homebrew
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3 python3-pip
```

### Step 2: Download Application Files

Create a new folder for the application:
- Windows: `C:\CF_Forecast` or `C:\Users\YourName\Desktop\CF_Forecast`
- macOS/Linux: `~/cf_forecast` or `~/Desktop/cf_forecast`

Download these 3 files into that folder:
- `app.py`
- `cf_predictor.py`
- `requirements.txt`

### Step 3: Install Python Dependencies

Open a terminal/command prompt and navigate to your folder:

**Windows (Command Prompt):**
```cmd
cd C:\CF_Forecast
pip install -r requirements.txt
```

**Windows (PowerShell):**
```powershell
cd C:\CF_Forecast
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
cd ~/cf_forecast
pip install -r requirements.txt
```

This will install:
- Streamlit (web framework)
- Pandas (data processing)
- Numpy (numerical computing)
- Plotly (charting)
- Openpyxl (Excel reading)

**Expected output:**
```
Successfully installed streamlit-1.28.1 pandas-2.0.0 numpy-1.24.0 plotly-5.17.0 openpyxl-3.10.0
```

---

## Running the Application

### Step 1: Start the App

Open terminal/command prompt in your CF_Forecast folder and run:

**Windows:**
```cmd
streamlit run app.py
```

**macOS/Linux:**
```bash
streamlit run app.py
```

### Step 2: Access in Browser

The app will automatically open in your default browser at:
```
http://localhost:8501
```

If it doesn't open automatically, copy this URL into your browser.

### Step 3: Use the Application

1. **Upload Receivables File**
   - Click "Upload Receivables Excel" in the sidebar
   - Select your Excel file with unpaid receivables

2. **Upload Payables File**
   - Click "Upload Payables Excel" in the sidebar
   - Select your Excel file with unpaid payables

3. **Configure Settings** (Optional)
   - Change Forecast Start Date (default: today)
   - Change Number of Weeks (default: 13)
   - Set Minimum Amount filter if needed

4. **Generate Forecast**
   - Click the blue "📊 Generate Forecast" button

5. **View Results**
   - Summary cards show total receivables, payables, and net CF
   - Charts show visual trends over 13 weeks
   - Detailed table shows week-by-week breakdown

6. **Export Results**
   - Click "📥 Download Excel" for detailed spreadsheet
   - Click "📄 Download HTML" for formatted report
   - Click "📊 Download CSV" for raw data

---

## Excel File Format Requirements

Your Excel files should have at least 26 columns with this structure:

| Col | Name | Purpose | Example |
|-----|------|---------|---------|
| 1 | Company | Company/Vendor name | "ABC Ltd." |
| 13 | Due Date | Payment due date | "2026-10-15" |
| 22 | Invoice Amount | Total invoice amount | 5000.00 |
| 26 | **Rozdiel** | **Unpaid remainder** | 2500.00 |

**Key Point**: Column 26 (Rozdiel) should contain the amount still owed after partial payments.

---

## Important Filtering Rules (Updated 2026-09-25)

### Receivables (Pohľadávky)
- ✅ **Include**: Items where Rozdiel > 0 AND due date is within 0-69 days
- ❌ **Exclude**: Items where due date > 70 days in the future (old receivables)
- 📌 **Placement**: All included receivables go to **Week 1** regardless of actual due date
  
**Why?** Old receivables (>70 days) are less reliable. Recent receivables (0-69 days) get priority in Week 1.

### Payables (Záväzky)
- ✅ **Include**: All items where Rozdiel > 0
- ❌ **No age filtering** applied
- 📌 **Placement**: Distributed to weeks based on actual due date

---

## Troubleshooting

### Problem: "Python not found" or "command not recognized"

**Solution:**
- On Windows, check that you selected "Add Python to PATH" during installation
- Restart your computer after installing Python
- Try using `python3` instead of `python`

### Problem: "streamlit not found"

**Solution:**
```bash
# Install Streamlit directly
pip install streamlit==1.28.1
```

### Problem: "ModuleNotFoundError: No module named 'pandas'"

**Solution:**
```bash
# Reinstall all requirements
pip install --upgrade pip
pip install -r requirements.txt
```

### Problem: "Address already in use" when starting app

**Solution:**
The port 8501 is already in use. Either:
1. Close the previous Streamlit instance
2. Use a different port:
```bash
streamlit run app.py --server.port 8502
```

### Problem: Excel file won't load

**Solution:**
- Ensure file is in `.xlsx` format (not `.xls` or `.csv`)
- Check that file has at least 26 columns
- Verify column 26 (Rozdiel) contains numeric values
- Try opening the file in Excel to confirm it's valid

### Problem: Forecast shows no data

**Solution:**
- Check that Rozdiel (column 26) has values > 0
- Verify due dates are in valid date format
- For receivables: confirm at least some items have due_date within 0-69 days
- Check minimum amount filter isn't excluding all items

---

## Configuration Tips

### Adjusting the 70-Day Threshold

To change the receivables age filter from 70 days:

1. Open `cf_predictor.py` in a text editor
2. Find this line (around line 131):
   ```python
   df = df[df['days_until_due'] <= 69].copy()
   ```
3. Change `69` to your desired number of days (e.g., `90` for 90 days)
4. Save the file and restart the app

### Changing Column Positions

If your Excel files have different column layouts:

1. Open `cf_predictor.py`
2. Find the column definitions (lines 27-30):
   ```python
   COL_COMPANY_NAME = 0      # Column A
   COL_DUE_DATE = 12         # Column M
   COL_INVOICE_AMOUNT = 21   # Column V
   COL_DIFFERENCE = 25       # Column Z
   ```
3. Adjust the numbers to match your file structure
   - Column A = 0, B = 1, C = 2, ... Z = 25
4. Save and restart

---

## Typical Workflow

### Weekly Update (Recommended Schedule)

1. **Monday**: Export latest receivables/payables from your accounting system
2. **Monday 10 AM**: Upload files to the app
3. **Monday 10:05 AM**: Generate forecast
4. **Monday 10:10 AM**: Download HTML report and share with team
5. **Monday 11 AM**: Discuss cash flow outlook in team meeting

### Monthly Deep Dive

1. Run forecast with different minimum amount thresholds
2. Compare current week vs previous forecasts
3. Adjust collection/payment strategies based on trends
4. Export to Excel for archival and trend analysis

---

## Understanding the Output

### Summary Cards
- **Pohľadávky (Inflow)**: Expected cash coming in from receivables
- **Záväzky (Outflow)**: Expected cash going out for payables
- **Net Cash Flow**: The difference (positive = surplus, negative = deficit)

### Charts
- **Stacked Bar**: Shows inflow vs outflow for each week
- **Net CF Trend**: Shows weekly and cumulative cash flow trends
- **Waterfall**: Shows how each week contributes to the 13-week total

### Details Table
Week-by-week breakdown with exact dates and amounts

---

## Deployment Options

After testing locally, you can share the forecast with your team:

### Option 1: Streamlit Cloud (Free & Easy)
1. Create account at https://streamlit.io/cloud
2. Connect your GitHub repository
3. Deploy with one click
4. Team accesses via shared URL

### Option 2: VBA Excel Macro (Alternative)
If clients prefer Excel, we can build a VBA macro version that runs inside Excel without Python.

### Option 3: Share HTML Reports
Export as HTML and email the formatted report weekly.

---

## Support & Contact

If you encounter issues:
1. Check this Troubleshooting section first
2. Verify your Excel file format
3. Check that all Python dependencies installed correctly
4. Review the data extraction logs in the app

---

## Version History

**v1.0 (2026-09-25)**
- Initial release with updated column mapping (Rozdiel - Column 26)
- 70-day receivables age filter
- Full Streamlit web interface
- Multiple export formats (Excel, HTML, CSV)

---

**Ready to forecast? Let's go! 💰**

```bash
streamlit run app.py
```
