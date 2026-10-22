"""
13-Week Rolling Cash Flow Forecast - Streamlit Web Application
A tool for forecasting cash flow by parsing unpaid receivables and payables.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from cf_predictor import CashFlowPredictor

# Page configuration
st.set_page_config(
    page_title="13-Week Cash Flow Forecast",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 10px 0;
    }

    .metric-card.positive {
        border-left-color: #2ca02c;
        background-color: #f0fdf4;
    }

    .metric-card.negative {
        border-left-color: #d62728;
        background-color: #fef2f2;
    }

    .metric-value {
        font-size: 24px;
        font-weight: bold;
        margin: 10px 0;
    }

    .metric-label {
        font-size: 14px;
        color: #666;
        text-transform: uppercase;
        font-weight: 600;
    }

    .metric-count {
        font-size: 12px;
        color: #999;
        margin-top: 8px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 4px 4px 0 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'forecast_data' not in st.session_state:
    st.session_state.forecast_data = None
if 'payables_df' not in st.session_state:
    st.session_state.payables_df = None
if 'receivables_df' not in st.session_state:
    st.session_state.receivables_df = None


def format_currency(value):
    """Format value as currency."""
    return f"€ {value:,.2f}".replace(',', ' ')


def load_excel_file(uploaded_file):
    """Load Excel file and return DataFrame."""
    try:
        df = pd.read_excel(uploaded_file, header=None)
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None


def create_summary_cards(summary):
    """Create summary metric cards."""
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
            <div class="metric-card positive">
                <div class="metric-label">Pohľadávky (Inflow)</div>
                <div class="metric-value">{format_currency(summary['total_receivables'])}</div>
                <div class="metric-count">{summary['num_receivables']} items</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card negative">
                <div class="metric-label">Záväzky (Outflow)</div>
                <div class="metric-value">{format_currency(summary['total_payables'])}</div>
                <div class="metric-count">{summary['num_payables']} items</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        net_value = summary['total_net']
        net_class = "positive" if net_value >= 0 else "negative"
        st.markdown(f"""
            <div class="metric-card {net_class}">
                <div class="metric-label">Net Cash Flow</div>
                <div class="metric-value">{format_currency(net_value)}</div>
                <div class="metric-count">13 weeks total</div>
            </div>
        """, unsafe_allow_html=True)


def create_stacked_bar_chart(forecast):
    """Create stacked bar chart: Receivables vs Payables."""
    weeks = []
    receivables = []
    payables = []

    for i in range(1, 14):
        week_data = forecast[f'week_{i}']
        weeks.append(f"W{i}")
        receivables.append(week_data['receivables'])
        payables.append(-week_data['payables'])  # Negative for visualization

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=weeks,
        y=receivables,
        name='Pohľadávky (Inflow)',
        marker=dict(color='#2ca02c'),
        hovertemplate='<b>%{x}</b><br>Pohľadávky: %{y:,.2f} €<extra></extra>'
    ))

    fig.add_trace(go.Bar(
        x=weeks,
        y=payables,
        name='Záväzky (Outflow)',
        marker=dict(color='#d62728'),
        hovertemplate='<b>%{x}</b><br>Záväzky: %{y:,.2f} €<extra></extra>'
    ))

    fig.update_layout(
        title='Receivables vs Payables by Week',
        xaxis_title='Week',
        yaxis_title='Amount (€)',
        barmode='relative',
        hovermode='x unified',
        template='plotly_white',
        height=400,
        margin=dict(b=50, l=50, r=20, t=50)
    )

    return fig


def create_net_cf_chart(forecast):
    """Create line chart: Net Cash Flow over 13 weeks."""
    weeks = []
    net_cf = []
    cumulative_cf = 0
    cumulative = []

    for i in range(1, 14):
        week_data = forecast[f'week_{i}']
        weeks.append(f"W{i}")
        net = week_data['net']
        net_cf.append(net)
        cumulative_cf += net
        cumulative.append(cumulative_cf)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Net CF Line
    fig.add_trace(
        go.Scatter(
            x=weeks,
            y=net_cf,
            name='Weekly Net CF',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=8),
            hovertemplate='<b>%{x}</b><br>Net CF: %{y:,.2f} €<extra></extra>'
        ),
        secondary_y=False
    )

    # Cumulative CF Line
    fig.add_trace(
        go.Scatter(
            x=weeks,
            y=cumulative,
            name='Cumulative CF',
            line=dict(color='#ff7f0e', width=2, dash='dash'),
            marker=dict(size=6),
            hovertemplate='<b>%{x}</b><br>Cumulative: %{y:,.2f} €<extra></extra>'
        ),
        secondary_y=True
    )

    fig.update_xaxes(title_text="Week")
    fig.update_yaxes(title_text="Weekly Net CF (€)", secondary_y=False)
    fig.update_yaxes(title_text="Cumulative CF (€)", secondary_y=True)

    fig.update_layout(
        title='Net Cash Flow Trend',
        hovermode='x unified',
        template='plotly_white',
        height=400,
        margin=dict(b=50, l=50, r=50, t=50)
    )

    return fig


def create_waterfall_chart(forecast):
    """Create waterfall chart showing cumulative impact."""
    weeks = []
    measures = []
    values = []

    cumulative = 0
    for i in range(1, 14):
        week_data = forecast[f'week_{i}']
        net = week_data['net']
        weeks.append(f"W{i}")
        measures.append('relative')
        values.append(net)
        cumulative += net

    # Add total
    weeks.append('Total')
    measures.append('total')
    values.append(0)  # Will be calculated automatically

    fig = go.Figure(go.Waterfall(
        x=weeks,
        y=values,
        measure=measures,
        text=[f"{v:,.0f}€" if v != 0 else "" for v in values],
        textposition="outside",
        connector={"line": {"color": "#888"}},
        increasing={"marker": {"color": "#2ca02c"}},
        decreasing={"marker": {"color": "#d62728"}},
        totals={"marker": {"color": "#1f77b4"}},
        hovertemplate='<b>%{x}</b><br>Value: %{y:,.2f} €<extra></extra>'
    ))

    fig.update_layout(
        title='Cumulative Cash Flow Impact (Waterfall)',
        template='plotly_white',
        height=400,
        margin=dict(b=50, l=50, r=20, t=50)
    )

    return fig


def create_detail_table(forecast):
    """Create detailed week-by-week table."""
    data = []
    for i in range(1, 14):
        week_data = forecast[f'week_{i}']
        data.append({
            'Week': f"W{i}",
            'Period': f"{week_data['week_start']} to {week_data['week_end']}",
            'Receivables': format_currency(week_data['receivables']),
            'Payables': format_currency(week_data['payables']),
            'Net CF': format_currency(week_data['net'])
        })

    df_detail = pd.DataFrame(data)
    return df_detail


def export_to_excel(forecast_data):
    """Export forecast to Excel."""
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Summary sheet
        summary = forecast_data['summary']
        summary_df = pd.DataFrame({
            'Metric': [
                'Total Receivables',
                'Total Payables',
                'Net Cash Flow',
                'Number of Receivables',
                'Number of Payables'
            ],
            'Value': [
                summary['total_receivables'],
                summary['total_payables'],
                summary['total_net'],
                summary['num_receivables'],
                summary['num_payables']
            ]
        })
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        # Forecast sheet
        forecast_data_list = []
        for i in range(1, 14):
            week_data = forecast_data['forecast'][f'week_{i}']
            forecast_data_list.append({
                'Week': i,
                'Start Date': week_data['week_start'],
                'End Date': week_data['week_end'],
                'Receivables': week_data['receivables'],
                'Payables': week_data['payables'],
                'Net CF': week_data['net']
            })
        forecast_df = pd.DataFrame(forecast_data_list)
        forecast_df.to_excel(writer, sheet_name='Forecast', index=False)

        # Receivables detail
        if forecast_data['receivables_detail']:
            receivables_df = pd.DataFrame(forecast_data['receivables_detail'])
            receivables_df.to_excel(writer, sheet_name='Receivables Detail', index=False)

        # Payables detail
        if forecast_data['payables_detail']:
            payables_df = pd.DataFrame(forecast_data['payables_detail'])
            payables_df.to_excel(writer, sheet_name='Payables Detail', index=False)

    return output.getvalue()


def export_to_html(forecast_data):
    """Export forecast to HTML using the predictor's report generator."""
    predictor = CashFlowPredictor()
    html = predictor.generate_html_report(forecast_data)
    return html.encode('utf-8')


# ==================== MAIN APP ====================

st.title("💰 13-Week Rolling Cash Flow Forecast")
st.write("Upload your Excel exports of unpaid receivables and payables to generate a rolling cash flow forecast.")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    # Date settings
    st.subheader("Forecast Period")
    today = datetime.now()
    forecast_start = st.date_input(
        "Forecast Start Date",
        value=today,
        help="Date to begin the 13-week forecast"
    )
    forecast_start_dt = datetime.combine(forecast_start, datetime.min.time())

    # Number of weeks
    num_weeks = st.slider(
        "Number of Weeks",
        min_value=4,
        max_value=26,
        value=13,
        help="Total weeks to forecast"
    )

    # Threshold amount
    min_amount = st.number_input(
        "Minimum Amount (EUR)",
        value=0.0,
        help="Exclude items below this amount"
    )

    st.divider()

    # File uploads
    st.subheader("📁 Data Upload")

    receivables_file = st.file_uploader(
        "Upload Receivables Excel",
        type=['xlsx', 'xls'],
        key='receivables_upload',
        help="Excel export of unpaid receivables"
    )

    payables_file = st.file_uploader(
        "Upload Payables Excel",
        type=['xlsx', 'xls'],
        key='payables_upload',
        help="Excel export of unpaid payables"
    )

    st.divider()

    if st.button("📊 Generate Forecast", key="generate_btn", use_container_width=True):
        if receivables_file and payables_file:
            with st.spinner("Processing files..."):
                # Load files
                receivables_raw = load_excel_file(receivables_file)
                payables_raw = load_excel_file(payables_file)

                if receivables_raw is not None and payables_raw is not None:
                    # Extract data
                    predictor = CashFlowPredictor(today=forecast_start_dt)

                    receivables_df = predictor.extract_receivables(receivables_raw)
                    payables_df = predictor.extract_payables(payables_raw)

                    # Apply minimum amount filter
                    if min_amount > 0:
                        receivables_df = receivables_df[receivables_df['amount'] >= min_amount]
                        payables_df = payables_df[payables_df['amount'] >= min_amount]

                    # Generate forecast
                    forecast_data = predictor.generate_forecast(
                        payables_df,
                        receivables_df,
                        num_weeks=num_weeks,
                        start_date=forecast_start_dt
                    )

                    # Cache in session state
                    st.session_state.forecast_data = forecast_data
                    st.session_state.payables_df = payables_df
                    st.session_state.receivables_df = receivables_df
                    st.session_state.num_weeks = num_weeks

                    st.success("✅ Forecast generated successfully!")
                else:
                    st.error("❌ Failed to load Excel files")
        else:
            st.error("❌ Please upload both receivables and payables files")

# Main content area
if st.session_state.forecast_data:
    forecast_data = st.session_state.forecast_data
    summary = forecast_data['summary']

    # Summary cards
    st.header("📈 Summary")
    create_summary_cards(summary)

    st.divider()

    # Visualizations
    st.header("📊 Visualizations")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Stacked Bar",
        "Net CF Trend",
        "Waterfall",
        "Details"
    ])

    with tab1:
        st.plotly_chart(
            create_stacked_bar_chart(forecast_data['forecast']),
            use_container_width=True
        )

    with tab2:
        st.plotly_chart(
            create_net_cf_chart(forecast_data['forecast']),
            use_container_width=True
        )

    with tab3:
        st.plotly_chart(
            create_waterfall_chart(forecast_data['forecast']),
            use_container_width=True
        )

    with tab4:
        st.dataframe(
            create_detail_table(forecast_data['forecast']),
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # Export options
    st.header("💾 Export")

    col1, col2, col3 = st.columns(3)

    with col1:
        excel_data = export_to_excel(forecast_data)
        st.download_button(
            label="📥 Download Excel",
            data=excel_data,
            file_name=f"CF_Forecast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    with col2:
        html_data = export_to_html(forecast_data)
        st.download_button(
            label="📄 Download HTML",
            data=html_data,
            file_name=f"CF_Forecast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
            mime="text/html",
            use_container_width=True
        )

    with col3:
        csv_data = create_detail_table(forecast_data['forecast']).to_csv(index=False)
        st.download_button(
            label="📊 Download CSV",
            data=csv_data,
            file_name=f"CF_Forecast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.divider()

    # Insights
    st.header("💡 Insights & Recommendations")

    net_total = summary['total_net']
    avg_weekly = net_total / st.session_state.num_weeks if st.session_state.num_weeks > 0 else 0

    insights = []

    if net_total > 0:
        insights.append(f"✅ **Positive Cash Flow**: Your 13-week forecast shows a net inflow of {format_currency(net_total)}")
    else:
        insights.append(f"⚠️ **Negative Cash Flow**: Your 13-week forecast shows a net outflow of {format_currency(abs(net_total))}")

    insights.append(f"📊 **Average Weekly**: {format_currency(avg_weekly)} per week")

    # Find weeks with negative cash flow
    negative_weeks = []
    for i in range(1, st.session_state.num_weeks + 1):
        if forecast_data['forecast'][f'week_{i}']['net'] < 0:
            negative_weeks.append(i)

    if negative_weeks:
        insights.append(f"⚠️ **Cash Flow Deficit Weeks**: Weeks {', '.join(map(str, negative_weeks))} show negative cash flow")

    for insight in insights:
        st.info(insight)

    st.divider()

    # Raw data preview
    with st.expander("📋 Show Raw Data"):
        st.subheader("Receivables Data")
        if not st.session_state.receivables_df.empty:
            st.dataframe(st.session_state.receivables_df, use_container_width=True)
        else:
            st.info("No receivables data")

        st.subheader("Payables Data")
        if not st.session_state.payables_df.empty:
            st.dataframe(st.session_state.payables_df, use_container_width=True)
        else:
            st.info("No payables data")

else:
    st.info("👋 Upload Excel files and click 'Generate Forecast' to begin!")
