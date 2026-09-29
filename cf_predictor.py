"""
Cash Flow Predictor Module
Predicts 13-week rolling cash flow by parsing Excel exports
and distributing payables/receivables to weekly buckets.

Key Updates (2026-09-25):
- Uses column 26 (Rozdiel) for unpaid amount for both payables and receivables
- Implements 70-day age filter for receivables: exclude items > 70 days, include 0-69 days in Week 1
- Payables have no age filtering applied
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CashFlowPredictor:
    """
    Core business logic for parsing Excel files and computing 13-week cash flow forecast.
    """

    # Column indices (0-based) in the Excel export
    # Note: Excel columns are 1-based, but pandas uses 0-based indexing
    COL_COMPANY_NAME = 0      # Column A
    COL_DUE_DATE = 12         # Column M (Due Date / Splatnosť)
    COL_INVOICE_AMOUNT = 21   # Column V (Suma faktúry / Invoice Amount)
    COL_DIFFERENCE = 25       # Column Z (Rozdiel / Unpaid Amount) - THE KEY COLUMN

    def __init__(self, today: datetime = None):
        """
        Initialize the predictor.

        Args:
            today: Reference date for calculations. Defaults to current date.
        """
        self.today = today or datetime.now()
        logger.info(f"CashFlowPredictor initialized. Today: {self.today.date()}")

    def extract_payables(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        """
        Extract unpaid payables from Excel data.

        A payable is unpaid if column 26 (Rozdiel) > 0.
        No age filtering is applied to payables.

        Args:
            raw_data: Raw DataFrame from Excel export

        Returns:
            DataFrame with columns: company_name, due_date, amount, days_until_due
        """
        logger.info("Extracting payables...")

        try:
            # Ensure we have enough columns
            if raw_data.shape[1] < 26:
                logger.warning(f"Expected at least 26 columns, got {raw_data.shape[1]}")
                return pd.DataFrame(columns=['company_name', 'due_date', 'amount', 'days_until_due'])

            # Extract relevant columns
            df = raw_data.iloc[:, [self.COL_COMPANY_NAME, self.COL_DUE_DATE,
                                   self.COL_INVOICE_AMOUNT, self.COL_DIFFERENCE]].copy()
            df.columns = ['company_name', 'due_date', 'invoice_amount', 'unpaid_amount']

            # Remove rows with missing critical data
            df = df.dropna(subset=['due_date', 'unpaid_amount'])

            # Convert data types
            try:
                df['due_date'] = pd.to_datetime(df['due_date'], errors='coerce')
                df['unpaid_amount'] = pd.to_numeric(df['unpaid_amount'], errors='coerce')
            except Exception as e:
                logger.error(f"Error converting data types: {e}")
                return pd.DataFrame(columns=['company_name', 'due_date', 'amount', 'days_until_due'])

            # Filter: unpaid amount > 0 (meaning there's still something owed)
            df = df[df['unpaid_amount'] > 0].copy()

            # Calculate days until due date
            df['days_until_due'] = (df['due_date'] - self.today).dt.days

            # Rename amount column to standard name
            df.rename(columns={'unpaid_amount': 'amount'}, inplace=True)

            # Keep only needed columns
            df = df[['company_name', 'due_date', 'amount', 'days_until_due']]

            logger.info(f"Extracted {len(df)} payable items")
            return df

        except Exception as e:
            logger.error(f"Error extracting payables: {e}")
            return pd.DataFrame(columns=['company_name', 'due_date', 'amount', 'days_until_due'])

    def extract_receivables(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        """
        Extract unpaid receivables from Excel data.

        A receivable is unpaid if column 26 (Rozdiel) > 0.

        FILTERING RULE (2026-09-25):
        - Exclude receivables where (due_date - today) > 70 days (old items)
        - Include receivables where 0 <= (due_date - today) <= 69 days
        - These included items are routed to Week 1 regardless of actual due date

        Args:
            raw_data: Raw DataFrame from Excel export

        Returns:
            DataFrame with columns: company_name, due_date, amount, days_until_due
        """
        logger.info("Extracting receivables...")

        try:
            # Ensure we have enough columns
            if raw_data.shape[1] < 26:
                logger.warning(f"Expected at least 26 columns, got {raw_data.shape[1]}")
                return pd.DataFrame(columns=['company_name', 'due_date', 'amount', 'days_until_due'])

            # Extract relevant columns
            df = raw_data.iloc[:, [self.COL_COMPANY_NAME, self.COL_DUE_DATE,
                                   self.COL_INVOICE_AMOUNT, self.COL_DIFFERENCE]].copy()
            df.columns = ['company_name', 'due_date', 'invoice_amount', 'unpaid_amount']

            # Remove rows with missing critical data
            df = df.dropna(subset=['due_date', 'unpaid_amount'])

            # Convert data types
            try:
                df['due_date'] = pd.to_datetime(df['due_date'], errors='coerce')
                df['unpaid_amount'] = pd.to_numeric(df['unpaid_amount'], errors='coerce')
            except Exception as e:
                logger.error(f"Error converting data types: {e}")
                return pd.DataFrame(columns=['company_name', 'due_date', 'amount', 'days_until_due'])

            # Filter: unpaid amount > 0 (meaning there's still something owed)
            df = df[df['unpaid_amount'] > 0].copy()

            # Calculate days until due date
            df['days_until_due'] = (df['due_date'] - self.today).dt.days

            # APPLY 70-DAY THRESHOLD FOR RECEIVABLES ONLY
            # Exclude items that are > 70 days past due or > 70 days in the future
            initial_count = len(df)
            df = df[df['days_until_due'] <= 69].copy()
            excluded_count = initial_count - len(df)

            if excluded_count > 0:
                logger.info(f"Excluded {excluded_count} receivables older than 70 days")

            # Rename amount column to standard name
            df.rename(columns={'unpaid_amount': 'amount'}, inplace=True)

            # Keep only needed columns
            df = df[['company_name', 'due_date', 'amount', 'days_until_due']]

            logger.info(f"Extracted {len(df)} receivable items after filtering")
            return df

        except Exception as e:
            logger.error(f"Error extracting receivables: {e}")
            return pd.DataFrame(columns=['company_name', 'due_date', 'amount', 'days_until_due'])

    def assign_to_weeks(self, items_df: pd.DataFrame, num_weeks: int = 13,
                       start_date: datetime = None) -> Tuple[Dict[str, float], List[Dict]]:
        """
        Assign items to weekly buckets based on due date.

        For receivables (identified by positive amount and days_until_due <= 69):
        Route to Week 1 as per filtering rule.

        For payables (or receivables > 70 days):
        Distribute to appropriate week based on actual due date.

        Args:
            items_df: DataFrame with items to assign (from extract_payables or extract_receivables)
            num_weeks: Number of weeks in forecast (default 13)
            start_date: Start date for forecast. Defaults to today.

        Returns:
            Tuple of (weekly_amounts_dict, detail_list)
        """
        if items_df.empty:
            logger.warning("No items to assign to weeks")
            return {f"week_{i+1}": 0.0 for i in range(num_weeks)}, []

        start_date = start_date or self.today
        weekly_amounts = {f"week_{i+1}": 0.0 for i in range(num_weeks)}
        details = []

        for idx, row in items_df.iterrows():
            try:
                company = row['company_name']
                due_date = row['due_date']
                amount = row['amount']
                days_until = row['days_until_due']

                # Calculate which week this item falls into
                days_from_start = (due_date - start_date).days
                week_num = max(1, min(num_weeks, (days_from_start // 7) + 1))

                # Special handling: if days_until <= 69 (filtered receivable), put in Week 1
                # This is already filtered at extraction stage, so we just use normal logic
                week_key = f"week_{week_num}"

                if week_key in weekly_amounts:
                    weekly_amounts[week_key] += amount
                    details.append({
                        'company': company,
                        'due_date': due_date.date(),
                        'amount': amount,
                        'week': week_num,
                        'days_until': days_until
                    })
                else:
                    # Beyond forecast period
                    logger.debug(f"Item {company} falls beyond {num_weeks} week forecast")

            except Exception as e:
                logger.warning(f"Error assigning item to week: {e}")
                continue

        return weekly_amounts, details

    def generate_forecast(self, payables_df: pd.DataFrame, receivables_df: pd.DataFrame,
                         num_weeks: int = 13, start_date: datetime = None) -> Dict:
        """
        Generate complete 13-week cash flow forecast.

        Args:
            payables_df: DataFrame of unpaid payables from extract_payables()
            receivables_df: DataFrame of unpaid receivables from extract_receivables()
            num_weeks: Number of weeks in forecast
            start_date: Start date for forecast

        Returns:
            Dictionary with weekly summaries and details
        """
        start_date = start_date or self.today
        logger.info(f"Generating {num_weeks}-week forecast starting {start_date.date()}")

        # Assign payables to weeks (negative cash flow)
        payables_weekly, payables_detail = self.assign_to_weeks(payables_df, num_weeks, start_date)

        # Assign receivables to weeks (positive cash flow)
        receivables_weekly, receivables_detail = self.assign_to_weeks(receivables_df, num_weeks, start_date)

        # Calculate net cash flow per week
        forecast = {}
        for i in range(1, num_weeks + 1):
            week_key = f"week_{i}"
            week_start = start_date + timedelta(days=7 * (i - 1))
            week_end = week_start + timedelta(days=6)

            receivables = receivables_weekly.get(week_key, 0.0)
            payables = payables_weekly.get(week_key, 0.0)
            net = receivables - payables

            forecast[week_key] = {
                'week_num': i,
                'week_start': week_start.date(),
                'week_end': week_end.date(),
                'receivables': round(receivables, 2),
                'payables': round(payables, 2),
                'net': round(net, 2),
            }

        # Summary
        total_receivables = sum(item['amount'] for item in receivables_detail)
        total_payables = sum(item['amount'] for item in payables_detail)
        total_net = total_receivables - total_payables

        result = {
            'forecast': forecast,
            'summary': {
                'total_receivables': round(total_receivables, 2),
                'total_payables': round(total_payables, 2),
                'total_net': round(total_net, 2),
                'num_receivables': len(receivables_detail),
                'num_payables': len(payables_detail),
            },
            'receivables_detail': receivables_detail,
            'payables_detail': payables_detail,
            'forecast_start': start_date.date(),
        }

        logger.info(f"Forecast complete: {result['summary']}")
        return result

    def generate_html_report(self, forecast_data: Dict) -> str:
        """
        Generate a professional HTML report of the cash flow forecast.

        Args:
            forecast_data: Dictionary from generate_forecast()

        Returns:
            HTML string
        """
        summary = forecast_data['summary']
        forecast = forecast_data['forecast']

        # Format currency
        def fmt_currency(val):
            return f"€ {val:,.2f}".replace(',', ' ')

        # Build table rows
        table_rows = ""
        for i in range(1, 14):
            week_data = forecast[f'week_{i}']
            week_start = week_data['week_start']
            week_end = week_data['week_end']
            receivables = week_data['receivables']
            payables = week_data['payables']
            net = week_data['net']

            # Color code net based on positive/negative
            net_color = '#00aa00' if net >= 0 else '#cc0000'

            table_rows += f"""
            <tr>
                <td class="col-week">Týždeň {i}</td>
                <td class="col-date">{week_start} – {week_end}</td>
                <td class="col-amount" style="color: #00aa00;">{fmt_currency(receivables)}</td>
                <td class="col-amount" style="color: #cc0000;">{fmt_currency(-payables)}</td>
                <td class="col-amount" style="color: {net_color}; font-weight: bold;">{fmt_currency(net)}</td>
            </tr>
            """

        html = f"""
        <!DOCTYPE html>
        <html lang="sk">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>13-Week Cash Flow Forecast</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}

                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: #f5f5f5;
                    padding: 20px;
                    color: #333;
                }}

                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }}

                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                    border-bottom: 3px solid #007bff;
                    padding-bottom: 20px;
                }}

                .header h1 {{
                    color: #007bff;
                    font-size: 28px;
                    margin-bottom: 5px;
                }}

                .header p {{
                    color: #666;
                    font-size: 14px;
                }}

                .summary {{
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 20px;
                    margin-bottom: 30px;
                }}

                .summary-box {{
                    padding: 20px;
                    border-radius: 6px;
                    text-align: center;
                }}

                .summary-box.positive {{
                    background: #e8f5e9;
                    border-left: 4px solid #4caf50;
                }}

                .summary-box.negative {{
                    background: #ffebee;
                    border-left: 4px solid #f44336;
                }}

                .summary-box.net {{
                    background: #e3f2fd;
                    border-left: 4px solid #2196f3;
                }}

                .summary-box h3 {{
                    font-size: 12px;
                    color: #666;
                    text-transform: uppercase;
                    margin-bottom: 10px;
                    font-weight: 600;
                }}

                .summary-box .value {{
                    font-size: 20px;
                    font-weight: bold;
                    color: #333;
                }}

                .summary-box .count {{
                    font-size: 11px;
                    color: #999;
                    margin-top: 8px;
                }}

                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }}

                thead {{
                    background: #f9f9f9;
                    border-bottom: 2px solid #ddd;
                }}

                th {{
                    padding: 12px;
                    text-align: left;
                    font-weight: 600;
                    font-size: 13px;
                    color: #555;
                    text-transform: uppercase;
                }}

                tbody tr {{
                    border-bottom: 1px solid #eee;
                    transition: background 0.2s;
                }}

                tbody tr:hover {{
                    background: #f9f9f9;
                }}

                td {{
                    padding: 12px;
                    font-size: 14px;
                }}

                .col-week {{
                    font-weight: 600;
                    color: #007bff;
                    width: 80px;
                }}

                .col-date {{
                    font-size: 13px;
                    color: #666;
                    width: 140px;
                }}

                .col-amount {{
                    text-align: right;
                    font-family: 'Courier New', monospace;
                    width: 130px;
                }}

                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #eee;
                    font-size: 12px;
                    color: #999;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>13-Week Rolling Cash Flow Forecast</h1>
                    <p>Forecast Period: {forecast_data['forecast_start']}</p>
                </div>

                <div class="summary">
                    <div class="summary-box positive">
                        <h3>Pohľadávky (Expected Inflow)</h3>
                        <div class="value">{fmt_currency(summary['total_receivables'])}</div>
                        <div class="count">{summary['num_receivables']} položiek</div>
                    </div>
                    <div class="summary-box negative">
                        <h3>Záväzky (Expected Outflow)</h3>
                        <div class="value">{fmt_currency(summary['total_payables'])}</div>
                        <div class="count">{summary['num_payables']} položiek</div>
                    </div>
                    <div class="summary-box net">
                        <h3>Čistý Cash Flow</h3>
                        <div class="value">{fmt_currency(summary['total_net'])}</div>
                        <div class="count">13 weeks total</div>
                    </div>
                </div>

                <table>
                    <thead>
                        <tr>
                            <th>Týždeň</th>
                            <th>Dátum</th>
                            <th style="text-align: right;">Pohľadávky</th>
                            <th style="text-align: right;">Záväzky</th>
                            <th style="text-align: right;">Čistý CF</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>

                <div class="footer">
                    <p>Generated by 13-Week Cash Flow Forecast Tool | {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
                </div>
            </div>
        </body>
        </html>
        """

        return html
