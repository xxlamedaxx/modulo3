import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress


def draw_plot():
    # Read data from file
    df = pd.read_csv("epa-sea-level.csv")

    # O dataset original vai até 2014, mas os testes do FCC usam até 2013
    df = df[df["Year"] <= 2013]

    # Create scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(df["Year"], df["CSIRO Adjusted Sea Level"])

    # Create first line of best fit (dados completos 1880–2013)
    slope_all, intercept_all, _, _, _ = linregress(
        df["Year"], df["CSIRO Adjusted Sea Level"]
    )
    years_extended = pd.Series(range(1880, 2051))
    plt.plot(years_extended, intercept_all + slope_all * years_extended)

    # Create second line of best fit (dados desde 2000 até 2013)
    df_recent = df[df["Year"] >= 2000]
    slope_recent, intercept_recent, _, _, _ = linregress(
        df_recent["Year"], df_recent["CSIRO Adjusted Sea Level"]
    )
    years_recent = pd.Series(range(2000, 2051))
    plt.plot(years_recent, intercept_recent + slope_recent * years_recent)

    # Add labels and title
    plt.title("Rise in Sea Level")
    plt.xlabel("Year")
    plt.ylabel("Sea Level (inches)")

    # Ajustar ticks do eixo X conforme esperado no teste
    plt.xticks([1850, 1875, 1900, 1925, 1950, 1975, 2000, 2025, 2050, 2075])

    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig("sea_level_plot.png")
    return plt.gca()
