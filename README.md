# Dashboard de Finanzas Personales 📊

Dashboard interactivo de finanzas personales construido con Python, pandas y Plotly. Analiza 11 meses de transacciones reales (Ene–Nov 2025) divididas en fuentes de ingreso y categorías de gasto.

![Vista previa del dashboard](screenshots/dashboard.png)

## Funcionalidades

- **Resumen de KPIs** — Ingresos totales, gastos, balance neto y tasa de ahorro de un vistazo
- **Tendencia mensual** — Ingresos vs gastos a lo largo del tiempo con área sombreada
- **Balance mensual** — Gráfico de barras mostrando meses positivos y negativos
- **Desglose de gastos** — Gráfico de dona con 14 categorías de gasto
- **Ingresos por fuente** — Barras horizontales por tipo de ingreso
- **Top 5 gastos** — Categorías con mayor gasto ordenadas

## Tecnologías utilizadas

- Python 3
- pandas — carga y agregación de datos
- Plotly — gráficos interactivos
- HTML/CSS — diseño y estilo del dashboard

## Estructura del proyecto

```
financial-dashboard/
├── data/
│   ├── Income_clean.csv       # Transacciones de ingresos
│   └── Expenses_clean.csv     # Transacciones de gastos
├── generate_dashboard.py      # Script principal
├── dashboard.html             # Dashboard generado (abrir en el navegador)
└── README.md
```

## Cómo ejecutarlo

**1. Clonar el repositorio**
```bash
git clone https://github.com/TU_USUARIO/financial-dashboard.git
cd financial-dashboard
```

**2. Instalar dependencias**
```bash
pip install pandas plotly
```

**3. Ejecutar el script**
```bash
python generate_dashboard.py
```

**4. Abrir el dashboard**

Abrir `dashboard.html` en cualquier navegador. No requiere servidor.

## Dataset

Datos sintéticos de finanzas personales con la siguiente estructura:

| Columna | Descripción |
|---------|-------------|
| `date_time` | Fecha de la transacción |
| `category` | Categoría de ingreso o gasto |
| `account` | Identificador de cuenta |
| `amount` | Monto de la transacción (BYN) |
| `currency` | Código de moneda |
| `type` | `income` (ingreso) o `expense` (gasto) |

**Categorías de ingresos:** Trabajo principal, Trabajo secundario, Cashback, Regalo, Intereses, Devolución de deuda, Otros

**Categorías de gastos:** Comida, Salud, Café, Transporte, Taxi, Ocio, Ropa, Universidad, Regalos, Multas, Otros

## Insights principales

- **Ingresos totales:** 26.629 BYN en 11 meses
- **Gastos totales:** 14.860 BYN en 11 meses
- **Tasa de ahorro:** 44,2% — muy por encima del 20% recomendado
- **Mes de mayor gasto:** Marzo 2025 (3.291 BYN)
- **Mes de mayor ingreso:** Septiembre 2025 (5.730 BYN)
- **Categoría con más gasto:** Salud

## Autora

**[Johanna Baldi]**
Analista de Datos | Power BI · SQL · Python

[LinkedIn](https://linkedin.com/in/jbaldi) · [GitHub](https://github.com/JohannaB28)
