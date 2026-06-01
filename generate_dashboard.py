"""
Dashboard de Finanzas Personales — Generador
Lee los CSV de ingresos y gastos y genera un dashboard HTML interactivo
(diseño glassmorphism, filtros, valores en USD, tabla de transacciones).

Requisitos: pandas. Plotly se carga desde el archivo local plotly.min.js.

Uso:
    python generate_dashboard.py

Salida:
    dashboard.html  (abrir en el navegador)
"""

import json
import pandas as pd

# Tasa de conversión BYN -> USD (aproximada)
BYN_TO_USD = 0.30


def load_data():
    income = pd.read_csv("data/Income_clean.csv")
    expenses = pd.read_csv("data/Expenses_clean.csv")

    income["type"] = "income"
    expenses["type"] = "expense"

    df = pd.concat([income, expenses], ignore_index=True)
    df["date_time"] = pd.to_datetime(df["date_time"])
    df["month"] = df["date_time"].dt.to_period("M").astype(str)
    df["amount_usd"] = (df["amount"] * BYN_TO_USD).round(2)
    df["day"] = df["date_time"].dt.strftime("%Y-%m-%d")
    df["amount"] = df["amount"].round(2)
    return df


def main():
    df = load_data()
    records = df[["day", "month", "category", "account",
                  "amount", "amount_usd", "type"]]
    payload = json.dumps({"records": json.loads(records.to_json(orient="records"))})

    with open("template.html", "r", encoding="utf-8") as f:
        template = f.read()

    html = template.replace("/*__DATA__*/", payload)

    with open("dashboard.html", "w", encoding="utf-8") as f:
        f.write(html)

    inc = df[df.type == "income"]["amount_usd"].sum()
    exp = df[df.type == "expense"]["amount_usd"].sum()
    print("dashboard.html generado")
    print(f"   Ingresos: ${inc:,.0f} | Gastos: ${exp:,.0f} | Balance: ${inc-exp:,.0f} (USD)")


if __name__ == "__main__":
    main()
