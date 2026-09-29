# 📋 13-Week Cash Flow Forecast - Testing Plan

**Test Date**: 2026-09-25  
**Application Version**: 1.1  
**Status**: Ready for Production Testing

---

## Pre-Testing Validation

### ✅ Core Logic Verification (Automated Tests)

All unit tests have been executed and passed:

```
✅ TEST 1: 70-Day Receivables Filter
   - Input: 5 receivables with various due dates
   - Output: 3 receivables (correctly excluded items >70 days)
   - PASS: Filter working as designed

✅ TEST 2: Rozdiel Column Usage (Column 26)  
   - Input: 4 payables with various Rozdiel values
   - Output: 3 payables (correctly excluded Rozdiel=0)
   - PASS: Column mapping correct

✅ TEST 3: Forecast Generation
   - Generated 13-week forecast
   - Calculated receivables, payables, net CF
   - PASS: Forecasting logic functional

✅ TEST 4: HTML Report Generation
   - Generated 11KB professional HTML report
   - Contains all summary sections
   - PASS: Report generation working
```

Run automated tests anytime:
```bash
python test_cf_predictor.py
```

---

## Manual Testing Checklist

### Phase 1: Environment Setup (30 minutes)

- [ ] Python 3.9+ installed: `python --version`
- [ ] pip working: `pip --version`
- [ ] Created CF_Forecast folder
- [ ] Downloaded 4 files (app.py, cf_predictor.py, requirements.txt, QUICK_START_GUIDE.md)
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] No error messages during installation
- [ ] All packages listed in requirements.txt installed successfully

**Expected Result:** All checks pass, ready for app launch.

---

### Phase 2: Application Startup (10 minutes)

- [ ] Terminal open in CF_Forecast folder
- [ ] Run: `streamlit run app.py`
- [ ] No errors in terminal output
- [ ] Browser opens automatically to http://localhost:8501
- [ ] Streamlit logo visible (top right)
- [ ] "💰 13-Week Rolling Cash Flow Forecast" title displays
- [ ] Sidebar with Configuration section visible
- [ ] File upload buttons present

**Expected Result:** App loads cleanly, UI renders correctly.

---

### Phase 3: File Format Testing (15 minutes)

#### Test 3A: Valid Excel Format
- [ ] Use actual receivables Excel export
- [ ] Verify file has at least 26 columns
- [ ] Verify Column 26 (Rozdiel) contains numeric values > 0
- [ ] Verify Column 13 (Due Date) contains valid dates
- [ ] Click "Upload Receivables Excel" → Select file
- [ ] File loads without error
- [ ] Filename displays under button

#### Test 3B: Invalid Format Handling
- [ ] Try uploading CSV file instead of Excel
- [ ] Verify error message displays
- [ ] Try uploading file with < 26 columns
- [ ] Verify warning or error message
- [ ] Try uploading corrupted Excel
- [ ] Verify graceful error handling (no crash)

**Expected Result:** Valid files accepted, invalid files handled gracefully.

---

### Phase 4: Data Extraction & Filtering (20 minutes)

#### Test 4A: Receivables Filtering
1. Upload receivables Excel file
2. Click "📊 Generate Forecast"
3. Wait for processing (< 5 seconds)
4. Check extracted receivables in "Show Raw Data" → Receivables Data:
   - [ ] Only items with Rozdiel > 0 shown
   - [ ] Only items with due date 0-69 days from today shown
   - [ ] Verify "days_until_due" column
   - [ ] Confirm no items > 69 days

#### Test 4B: Payables Extraction
1. Confirm payables also uploaded
2. Click "📊 Generate Forecast"
3. Check extracted payables in "Show Raw Data" → Payables Data:
   - [ ] Only items with Rozdiel > 0 shown
   - [ ] No date filtering applied (items of any age included)
   - [ ] Verify all unpaid items present

**Expected Result:** Data correctly extracted with proper filters applied.

---

### Phase 5: Forecast Calculation (15 minutes)

#### Test 5A: Summary Metrics
After clicking "Generate Forecast":
- [ ] Summary section displays 3 cards
- [ ] "Pohľadávky (Inflow)" shows positive value ✓ Green
- [ ] "Záväzky (Outflow)" shows positive value ✓ Red  
- [ ] "Net Cash Flow" shows correctly calculated value
- [ ] Color indicates result (green if positive, blue if total, red if negative)
- [ ] Item counts displayed (e.g., "10 items")

#### Test 5B: Weekly Distribution
- [ ] Week 1 contains items from 0-69 day receivables filter ✓
- [ ] Weeks 2-13 have reasonable distribution
- [ ] Total of all weeks matches summary total
- [ ] No data in weeks beyond forecast period

**Expected Result:** Metrics calculated correctly, distribution logical.

---

### Phase 6: Visualization Testing (20 minutes)

#### Test 6A: Stacked Bar Chart
- [ ] Chart displays with Week 1-13 on X-axis
- [ ] Green bars for Receivables (inflow)
- [ ] Red bars for Payables (outflow)
- [ ] Hover shows exact values
- [ ] Title: "Receivables vs Payables by Week"

#### Test 6B: Net CF Trend Chart
- [ ] Chart displays weekly net CF (blue line)
- [ ] Dashed line shows cumulative CF (orange)
- [ ] Hover shows both values
- [ ] Trend clear and readable
- [ ] Cumulative line shows progression

#### Test 6C: Waterfall Chart
- [ ] Each week shows as bar
- [ ] Green bars for positive weeks
- [ ] Red bars for negative weeks
- [ ] Final "Total" bar shows cumulative result
- [ ] Labels visible on bars

**Expected Result:** All charts render, data displays correctly.

---

### Phase 7: Detail Table Testing (10 minutes)

- [ ] Switch to "Details" tab
- [ ] Table displays all 13 weeks
- [ ] Columns: Week, Period, Receivables, Payables, Net CF
- [ ] Dates format correctly (YYYY-MM-DD)
- [ ] Currency values formatted with €
- [ ] Numbers align right (currency format)
- [ ] Data matches chart values

**Expected Result:** Table displays complete, accurate weekly breakdown.

---

### Phase 8: Export Functionality (20 minutes)

#### Test 8A: Excel Export
- [ ] Click "📥 Download Excel"
- [ ] File downloads (CF_Forecast_YYYYMMDD_HHMMSS.xlsx)
- [ ] Open file in Excel/LibreOffice
- [ ] Verify sheets: Summary, Forecast, Receivables Detail, Payables Detail
- [ ] Check Summary sheet has 5 rows (metrics)
- [ ] Check Forecast sheet has 13 rows (weeks)
- [ ] Values match app display
- [ ] Formatting preserves numbers (not text)

#### Test 8B: HTML Export
- [ ] Click "📄 Download HTML"  
- [ ] File downloads (CF_Forecast_YYYYMMDD_HHMMSS.html)
- [ ] Open in web browser
- [ ] Professional layout displays
- [ ] Three summary cards visible
- [ ] Table shows 13 weeks
- [ ] Colors appropriate (green=positive, red=negative)
- [ ] Can print to PDF

#### Test 8C: CSV Export
- [ ] Click "📊 Download CSV"
- [ ] File downloads (CF_Forecast_YYYYMMDD_HHMMSS.csv)
- [ ] Open in Excel/text editor
- [ ] Data properly delimited
- [ ] Headers present
- [ ] All 13 weeks included
- [ ] Numbers readable

**Expected Result:** All export formats work, files open correctly.

---

### Phase 9: Configuration Testing (15 minutes)

#### Test 9A: Forecast Start Date
- [ ] Change "Forecast Start Date" to different date
- [ ] Click "📊 Generate Forecast"
- [ ] Week 1 start date changes
- [ ] All weeks shifted accordingly
- [ ] Data redistributed to new date range

#### Test 9B: Number of Weeks
- [ ] Change "Number of Weeks" to 4
- [ ] Click "📊 Generate Forecast"
- [ ] Only 4 weeks displayed
- [ ] Change to 26 weeks
- [ ] All 26 weeks displayed
- [ ] Summary total remains same

#### Test 9C: Minimum Amount Filter
- [ ] Set "Minimum Amount (EUR)" to 1000
- [ ] Click "📊 Generate Forecast"
- [ ] Items < 1000 excluded
- [ ] Summary total reduced
- [ ] Set to 0 (default)
- [ ] All items included again

**Expected Result:** Configuration changes apply immediately.

---

### Phase 10: Error Handling (10 minutes)

- [ ] Close browser, restart app → No crash
- [ ] Clear browser cache → App still works
- [ ] Try generate without uploading files → Error message displays
- [ ] Upload same file twice → Works (no duplicate errors)
- [ ] Upload very large file (>100MB) → Handles gracefully or times out
- [ ] Click buttons rapidly → No multiple submissions
- [ ] Refresh page mid-forecast → Session state preserved

**Expected Result:** App handles errors gracefully, no crashes.

---

### Phase 11: Performance Testing (10 minutes)

#### Test 11A: Load Time
- [ ] Forecast generation time: **Target < 5 seconds**
- [ ] Chart rendering time: **Target < 2 seconds**
- [ ] Export time: **Target < 3 seconds**

#### Test 11B: Memory Usage
- [ ] App remains responsive with 10MB file
- [ ] Test with 100,000 items in Excel
- [ ] Memory doesn't leak after multiple forecasts

**Expected Result:** Performance meets targets.

---

### Phase 12: Real Data Testing (30 minutes)

Use actual receivables/payables Excel exports:

#### Test 12A: Receivables Analysis
- [ ] Upload actual receivables file
- [ ] Inspect extracted data
- [ ] Verify 70-day filter is reasonable for your business
- [ ] Check that Week 1 contains expected items
- [ ] Confirm total receivables amount is accurate

#### Test 12B: Payables Analysis
- [ ] Upload actual payables file
- [ ] Inspect extracted data
- [ ] Verify all unpaid items included
- [ ] Check distribution across weeks matches payment terms
- [ ] Confirm total payables amount is accurate

#### Test 12C: Cash Flow Interpretation
- [ ] Does forecast direction make business sense?
- [ ] Are there concerning weeks with negative CF?
- [ ] Do the trends align with your business cycle?
- [ ] Could results influence upcoming decisions?

**Expected Result:** Results make business sense, usable for planning.

---

## Test Results Summary

| Phase | Test | Status | Notes |
|-------|------|--------|-------|
| 1 | Environment Setup | ⬜ | |
| 2 | Application Startup | ⬜ | |
| 3 | File Format | ⬜ | |
| 4 | Data Extraction | ⬜ | |
| 5 | Forecast Calculation | ⬜ | |
| 6 | Visualization | ⬜ | |
| 7 | Detail Table | ⬜ | |
| 8 | Export Functionality | ⬜ | |
| 9 | Configuration | ⬜ | |
| 10 | Error Handling | ⬜ | |
| 11 | Performance | ⬜ | |
| 12 | Real Data | ⬜ | |

**Overall Status**: ⬜ (Mark as ✅ when all phases complete)

---

## Known Limitations & Workarounds

| Limitation | Impact | Workaround |
|-----------|--------|-----------|
| Excel only (no CSV) | Can't import from other formats | Export from accounting system as .xlsx |
| Fixed 26 columns | Different layouts won't parse | Contact support for custom mapping |
| 70-day hardcoded | Can't adjust filter easily | Edit `cf_predictor.py` line 131 |
| No data persistence | Results lost on page refresh | Export results immediately |
| Single forecast at a time | Can't compare versions | Download HTML before new upload |

---

## Deployment Readiness Checklist

- [ ] All 12 test phases completed successfully
- [ ] No crashes or unexpected errors
- [ ] Performance meets targets
- [ ] Results make business sense
- [ ] Team trained on how to use
- [ ] Excel export template approved
- [ ] HTML report format approved
- [ ] Weekly update process defined
- [ ] Backup/archival strategy planned
- [ ] Support contact identified

---

## Sign-Off

When all testing complete:

**Tested By**: ________________  
**Test Date**: ________________  
**Status**: ⬜ PASS / ⬜ FAIL / ⬜ PASS WITH ISSUES  
**Notes**: _______________________________________________________________

---

## Next Steps After Testing

✅ **If all tests PASS:**
1. Deploy to production environment
2. Set up weekly data refresh schedule
3. Train end users
4. Go live!

⚠️ **If issues found:**
1. Document all failures
2. Create bug reports with steps to reproduce
3. Fix issues
4. Re-test affected areas
5. Repeat until PASS

---

**Testing Complete?** Mark the date above and move to deployment! 🚀
