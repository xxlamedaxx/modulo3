import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Importa os dados e já define 'date' como índice datetime
df = pd.read_csv('fcc-forum-pageviews.csv',
                 parse_dates=['date'], index_col='date')

# Remove os 2,5% menores e 2,5% maiores valores para limpar outliers
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]


def draw_line_plot():
    df_line = df.copy()

    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df_line.index, df_line['value'], color='red', linewidth=1)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    # Agrupa por ano e mês e calcula a média
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Ordena os meses corretamente
    month_order = list(range(1, 13))
    df_bar = df_bar[month_order]

    # Gráfico de barras
    fig = df_bar.plot(kind='bar', figsize=(12, 6)).figure
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")

    # Usa abreviações de meses
    plt.legend(
        title="Months",
        labels=['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December']
    )

    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    df_box = df.copy().reset_index()
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')  # abreviações
    df_box['month_num'] = df_box['date'].dt.month

    # Ordena os meses para exibir corretamente no boxplot
    df_box = df_box.sort_values('month_num')

    fig, axes = plt.subplots(1, 2, figsize=(20, 8))

    # Boxplot por ano
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Boxplot por mês (ordem correta)
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='month', y='value', data=df_box,
                order=month_order, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    fig.savefig('box_plot.png')
    return fig
