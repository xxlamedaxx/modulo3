import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv('medical_examination.csv')

# Ajusta nome da coluna para "sex"
df.rename(columns={'gender': 'sex'}, inplace=True)

# Cria coluna id
df['id'] = df.index

# Cria coluna overweight (IMC > 25 = 1)
bmi = df['weight'] / ((df['height'] / 100) ** 2)
df['overweight'] = (bmi > 25).astype(int)

# Normaliza colesterol e glicose
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)


def draw_cat_plot():
    features = ['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke']

    # Reorganiza no formato longo
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=features)

    # Conta cada categoria
    df_cat = (
        df_cat
        .groupby(['cardio', 'variable', 'value'])
        .size()
        .reset_index(name='total')
    )

    # Gráfico categórico
    g = sns.catplot(
        data=df_cat,
        x='variable',
        y='total',
        hue='value',
        col='cardio',
        kind='bar'
    )

    fig = g.fig
    fig.savefig('catplot.png')
    return fig


def draw_heat_map():
    # Filtra dados inválidos
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # Matriz de correlação
    corr = df_heat.corr()

    # Máscara para triângulo superior
    mask = np.triu(corr)

    # Figura
    fig, ax = plt.subplots(figsize=(12, 12))

    # Heatmap
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".1f",
        square=True,
        linewidths=1,
        cbar_kws={"shrink": 0.5},
        ax=ax
    )

    fig.savefig("heatmap.png")
    return fig
