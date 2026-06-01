"""
Personal Finance Dashboard
Author: [Your Name]
Dataset: Financial Transactions (Income & Expenses) 2025
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# ── 1. Load & prepare data ──────────────────────────────────────────────────

income_df = pd.read_csv("data/Income_clean.csv")
expenses_df = pd.read_csv("data/Expenses_clean.csv")

income_df["type"] = "income"
expenses_df["type"] = "expense"

df = pd.concat([income_df, expenses_df], ignore_index=True)
df["date_time"] = pd.to_datetime(df["date_time"])
df["month"] = df["date_time"].dt.to_period("M").astype(str)
df["month_label"] = df["date_time"].dt.strftime("%b %Y")

# ── 2. Aggregations ─────────────────────────────────────────────────────────

total_income   = df[df["type"] == "income"]["amount"].sum()
total_expenses = df[df["type"] == "expense"]["amount"].sum()
balance        = total_income - total_expenses
savings_rate   = round((balance / total_income) * 100, 1)

monthly = (
    df.groupby(["month", "type"])["amount"]
    .sum()
    .unstack(fill_value=0)
    .reset_index()
)
monthly["balance"] = monthly.get("income", 0) - monthly.get("expense", 0)
monthly["month_label"] = pd.to_datetime(monthly["month"]).dt.strftime("%b %Y")

expense_by_cat = (
    df[df["type"] == "expense"]
    .groupby("category")["amount"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

income_by_cat = (
    df[df["type"] == "income"]
    .groupby("category")["amount"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

# ── 3. Color palette ────────────────────────────────────────────────────────

BG        = "#0f1117"
CARD_BG   = "#1a1d27"
BORDER    = "#2a2d3e"
GREEN     = "#00d4a4"
RED       = "#ff5c7c"
BLUE      = "#4d9fff"
YELLOW    = "#ffd166"
TEXT      = "#e8eaf0"
SUBTEXT   = "#8b90a8"

EXPENSE_COLORS = [
    "#ff5c7c", "#ff8fa3", "#ffb3c1", "#e63960",
    "#c41c42", "#ff7a5c", "#ffa07a", "#ffc4a8",
    "#ff6b35", "#ff9a6c", "#ffb894", "#ffd4bc",
    "#cc4400", "#ff6600"
]

INCOME_COLORS = [
    "#00d4a4", "#00b894", "#00a67e", "#4dffd9",
    "#80ffea", "#00e6b0", "#00c99a"
]

# ── 4. Build charts ─────────────────────────────────────────────────────────

# Chart 1 — Monthly Income vs Expenses (line)
fig_monthly = go.Figure()
fig_monthly.add_trace(go.Scatter(
    x=monthly["month_label"], y=monthly.get("income", [0]*len(monthly)),
    name="Income", line=dict(color=GREEN, width=2.5),
    fill="tozeroy", fillcolor="rgba(0,212,164,0.08)",
    mode="lines+markers", marker=dict(size=6, color=GREEN)
))
fig_monthly.add_trace(go.Scatter(
    x=monthly["month_label"], y=monthly.get("expense", [0]*len(monthly)),
    name="Expenses", line=dict(color=RED, width=2.5),
    fill="tozeroy", fillcolor="rgba(255,92,124,0.08)",
    mode="lines+markers", marker=dict(size=6, color=RED)
))
fig_monthly.update_layout(
    title=dict(text="Monthly Income vs Expenses", font=dict(color=TEXT, size=15)),
    paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
    font=dict(color=SUBTEXT, family="monospace"),
    legend=dict(bgcolor=CARD_BG, bordercolor=BORDER, font=dict(color=TEXT)),
    xaxis=dict(gridcolor=BORDER, tickfont=dict(color=SUBTEXT)),
    yaxis=dict(gridcolor=BORDER, tickfont=dict(color=SUBTEXT)),
    margin=dict(l=20, r=20, t=50, b=20), height=320
)

# Chart 2 — Monthly Balance (bar)
fig_balance = go.Figure()
fig_balance.add_trace(go.Bar(
    x=monthly["month_label"],
    y=monthly["balance"],
    marker_color=[GREEN if v >= 0 else RED for v in monthly["balance"]],
    name="Balance"
))
fig_balance.update_layout(
    title=dict(text="Monthly Balance", font=dict(color=TEXT, size=15)),
    paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
    font=dict(color=SUBTEXT, family="monospace"),
    xaxis=dict(gridcolor=BORDER, tickfont=dict(color=SUBTEXT)),
    yaxis=dict(gridcolor=BORDER, tickfont=dict(color=SUBTEXT)),
    margin=dict(l=20, r=20, t=50, b=20), height=300
)

# Chart 3 — Expense breakdown (donut)
fig_expenses_donut = go.Figure(go.Pie(
    labels=expense_by_cat["category"],
    values=expense_by_cat["amount"],
    hole=0.55,
    marker=dict(colors=EXPENSE_COLORS, line=dict(color=BG, width=2)),
    textfont=dict(color=TEXT),
    hovertemplate="<b>%{label}</b><br>%{value:.0f} BYN<br>%{percent}<extra></extra>"
))
fig_expenses_donut.update_layout(
    title=dict(text="Expense Breakdown", font=dict(color=TEXT, size=15)),
    paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
    font=dict(color=SUBTEXT, family="monospace"),
    legend=dict(bgcolor=CARD_BG, font=dict(color=TEXT, size=11)),
    margin=dict(l=20, r=20, t=50, b=20), height=360
)

# Chart 4 — Income by source (horizontal bar)
fig_income_bar = go.Figure(go.Bar(
    x=income_by_cat["amount"],
    y=income_by_cat["category"],
    orientation="h",
    marker=dict(
        color=income_by_cat["amount"],
        colorscale=[[0, "#005c47"], [1, GREEN]],
        line=dict(color=BG, width=1)
    ),
    text=income_by_cat["amount"].apply(lambda x: f"{x:,.0f}"),
    textposition="outside",
    textfont=dict(color=TEXT)
))
fig_income_bar.update_layout(
    title=dict(text="Income by Source", font=dict(color=TEXT, size=15)),
    paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
    font=dict(color=SUBTEXT, family="monospace"),
    xaxis=dict(gridcolor=BORDER, tickfont=dict(color=SUBTEXT)),
    yaxis=dict(gridcolor=BORDER, tickfont=dict(color=SUBTEXT)),
    margin=dict(l=20, r=20, t=50, b=20), height=300
)

# Chart 5 — Top 5 expenses (bar)
top5 = expense_by_cat.head(5)
fig_top5 = go.Figure(go.Bar(
    x=top5["category"],
    y=top5["amount"],
    marker=dict(
        color=top5["amount"],
        colorscale=[[0, "#5c001a"], [1, RED]],
        line=dict(color=BG, width=1)
    ),
    text=top5["amount"].apply(lambda x: f"{x:,.0f}"),
    textposition="outside",
    textfont=dict(color=TEXT)
))
fig_top5.update_layout(
    title=dict(text="Top 5 Expense Categories", font=dict(color=TEXT, size=15)),
    paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
    font=dict(color=SUBTEXT, family="monospace"),
    xaxis=dict(gridcolor=BORDER, tickfont=dict(color=SUBTEXT)),
    yaxis=dict(gridcolor=BORDER, tickfont=dict(color=SUBTEXT)),
    margin=dict(l=20, r=20, t=50, b=20), height=300
)

# ── 5. Convert charts to HTML ────────────────────────────────────────────────

def chart_html(fig):
    return fig.to_html(full_html=False, include_plotlyjs=False, config={"displayModeBar": False})

# ── 6. Assemble full HTML dashboard ─────────────────────────────────────────

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Personal Finance Dashboard 2025</title>
  <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet" />
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    :root {{
      --bg:       {BG};
      --card:     {CARD_BG};
      --border:   {BORDER};
      --green:    {GREEN};
      --red:      {RED};
      --blue:     {BLUE};
      --yellow:   {YELLOW};
      --text:     {TEXT};
      --subtext:  {SUBTEXT};
    }}

    body {{
      background: var(--bg);
      color: var(--text);
      font-family: 'DM Sans', sans-serif;
      min-height: 100vh;
      padding: 32px 24px;
    }}

    /* Header */
    .header {{
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      margin-bottom: 36px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--border);
    }}
    .header-left h1 {{
      font-family: 'Space Mono', monospace;
      font-size: 22px;
      font-weight: 700;
      letter-spacing: -0.5px;
      color: var(--text);
    }}
    .header-left p {{
      font-size: 13px;
      color: var(--subtext);
      margin-top: 4px;
      font-family: 'Space Mono', monospace;
    }}
    .badge {{
      background: rgba(0,212,164,0.1);
      border: 1px solid rgba(0,212,164,0.3);
      color: var(--green);
      font-family: 'Space Mono', monospace;
      font-size: 11px;
      padding: 6px 14px;
      border-radius: 20px;
      letter-spacing: 1px;
    }}

    /* KPI Cards */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-bottom: 28px;
    }}
    .kpi-card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px 22px;
      position: relative;
      overflow: hidden;
    }}
    .kpi-card::before {{
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 3px;
      border-radius: 12px 12px 0 0;
    }}
    .kpi-card.green::before  {{ background: var(--green); }}
    .kpi-card.red::before    {{ background: var(--red); }}
    .kpi-card.blue::before   {{ background: var(--blue); }}
    .kpi-card.yellow::before {{ background: var(--yellow); }}

    .kpi-label {{
      font-size: 11px;
      color: var(--subtext);
      text-transform: uppercase;
      letter-spacing: 1.5px;
      font-family: 'Space Mono', monospace;
      margin-bottom: 10px;
    }}
    .kpi-value {{
      font-family: 'Space Mono', monospace;
      font-size: 26px;
      font-weight: 700;
      line-height: 1;
    }}
    .kpi-card.green  .kpi-value {{ color: var(--green); }}
    .kpi-card.red    .kpi-value {{ color: var(--red); }}
    .kpi-card.blue   .kpi-value {{ color: var(--blue); }}
    .kpi-card.yellow .kpi-value {{ color: var(--yellow); }}
    .kpi-sub {{
      font-size: 12px;
      color: var(--subtext);
      margin-top: 6px;
    }}

    /* Chart grid */
    .chart-card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 8px 12px 4px;
      margin-bottom: 20px;
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-bottom: 20px;
    }}
    .grid-2 .chart-card {{ margin-bottom: 0; }}

    /* Footer */
    footer {{
      text-align: center;
      margin-top: 40px;
      padding-top: 20px;
      border-top: 1px solid var(--border);
      font-family: 'Space Mono', monospace;
      font-size: 11px;
      color: var(--subtext);
      letter-spacing: 1px;
    }}

    @media (max-width: 900px) {{
      .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }}
      .grid-2   {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>

  <div class="header">
    <div class="header-left">
      <h1>Personal Finance Dashboard</h1>
      <p>Jan 2025 — Nov 2025 &nbsp;·&nbsp; 1,287 transactions</p>
    </div>
    <span class="badge">BYN · 2025</span>
  </div>

  <!-- KPI Cards -->
  <div class="kpi-grid">
    <div class="kpi-card green">
      <div class="kpi-label">Total Income</div>
      <div class="kpi-value">{total_income:,.0f}</div>
      <div class="kpi-sub">BYN · Jan–Nov 2025</div>
    </div>
    <div class="kpi-card red">
      <div class="kpi-label">Total Expenses</div>
      <div class="kpi-value">{total_expenses:,.0f}</div>
      <div class="kpi-sub">BYN · Jan–Nov 2025</div>
    </div>
    <div class="kpi-card blue">
      <div class="kpi-label">Net Balance</div>
      <div class="kpi-value">{balance:,.0f}</div>
      <div class="kpi-sub">Income minus expenses</div>
    </div>
    <div class="kpi-card yellow">
      <div class="kpi-label">Savings Rate</div>
      <div class="kpi-value">{savings_rate}%</div>
      <div class="kpi-sub">Of total income saved</div>
    </div>
  </div>

  <!-- Monthly trend — full width -->
  <div class="chart-card">
    {chart_html(fig_monthly)}
  </div>

  <!-- Balance + Income source -->
  <div class="grid-2">
    <div class="chart-card">{chart_html(fig_balance)}</div>
    <div class="chart-card">{chart_html(fig_income_bar)}</div>
  </div>

  <!-- Donut + Top 5 -->
  <div class="grid-2">
    <div class="chart-card">{chart_html(fig_expenses_donut)}</div>
    <div class="chart-card">{chart_html(fig_top5)}</div>
  </div>

  <footer>BUILT WITH PYTHON · PANDAS · PLOTLY &nbsp;·&nbsp; PERSONAL FINANCE DASHBOARD 2025</footer>

</body>
</html>"""

with open("dashboard.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ dashboard.html generated successfully")
