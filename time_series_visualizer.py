# Importar bibliotecas necessárias
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 1: Importar os dados
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col="date")

# 2: Limpeza dos dados (remover top 2.5% e bottom 2.5% das visualizações de página)
# Usar as funções do numpy np.quantile para evitar problemas com numpy
lower_quantile = df["value"].quantile(0.025)
upper_quantile = df["value"].quantile(0.975)
df_cleaned = df[(df["value"] >= lower_quantile) & (df["value"] <= upper_quantile)]

# 3: Criar o gráfico de linha
def draw_line_plot():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df_cleaned.index, df_cleaned["value"], color='red', linewidth=1)

    # Título e rótulos dos eixos
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Salvar e retornar o gráfico
    fig.savefig("line_plot.png")
    return fig

# 4: Criar o gráfico de barras
def draw_bar_plot():
    # Preparar os dados
    df_bar = df_cleaned.copy()
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month

    # Agrupar por ano e mês e calcular a média das visualizações diárias
    df_bar_grouped = df_bar.groupby(["year", "month"])["value"].mean().unstack()

    # Criar o gráfico de barras
    fig = df_bar_grouped.plot(kind="bar", figsize=(10, 6), legend=True).figure
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months", labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.xticks(rotation=45)

    # Salvar e retornar o gráfico
    fig.savefig("bar_plot.png")
    return fig

# 5: Criar os gráficos de box plot
def draw_box_plot():
    # Preparar os dados
    df_box = df_cleaned.copy()
    df_box.reset_index(inplace=True)
    df_box["year"] = df_box["date"].dt.year
    df_box["month"] = df_box["date"].dt.strftime("%b")

    # Ordenar os meses corretamente
    months_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    df_box["month"] = pd.Categorical(df_box["month"], categories=months_order, ordered=True)

    # Criar os gráficos de box plot
    fig, ax = plt.subplots(1, 2, figsize=(18, 6))

    # Box plot por ano
    sns.boxplot(x="year", y="value", data=df_box, ax=ax[0])
    ax[0].set_title("Year-wise Box Plot (Trend)")
    ax[0].set_xlabel("Year")
    ax[0].set_ylabel("Page Views")

    # Box plot por mês
    sns.boxplot(x="month", y="value", data=df_box, ax=ax[1])
    ax[1].set_title("Month-wise Box Plot (Seasonality)")
    ax[1].set_xlabel("Month")
    ax[1].set_ylabel("Page Views")

    # Salvar e retornar o gráfico
    fig
