import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')
# Serve para quantidade de pessoas de cada raça
    race_count = df['race'].value_counts()

# Media de idade dos homens. Usa comando round para arredondar o valor
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    # Percentual de pessoas com bacharelado
    percentage_bachelors = round(
        (df['education'].value_counts(normalize=True) * 100).loc['Bachelors'], 1)

# cria uma mascara boolean para identificar pessoas com educação avançada (isin)
# df seleciiona na parte de educação e o isin ajuda pegar as pessoas com bacharelado, mestrado ou doutorado
    advanced_education = df['education'].isin(
        ['Bachelors', 'Masters', 'Doctorate'])
    higher_education = df[advanced_education]  # pega do advanced
    lower_education = df[~advanced_education]  # pega do contrario do advanced

    higher_education_rich = round(
        (higher_education[higher_education['salary'] == '>50K'].shape[0] / higher_education.shape[0]) * 100, 1)

    lower_education_rich = round(
        (lower_education[lower_education['salary'] == '>50K'].shape[0] / lower_education.shape[0]) * 100, 1)

    min_work_hours = df['hours-per-week'].min()

    num_min_workers = df[df['hours-per-week'] == min_work_hours]

    rich_percentage = round(
        (num_min_workers[num_min_workers['salary'] == '>50K'].shape[0] / num_min_workers.shape[0]) * 100, 1)

    country_earning = df[df['salary'] ==
                         '>50K']['native-country'].value_counts()

    country_total = df['native-country'].value_counts()
    highest_earning_country = (country_earning / country_total * 100).idxmax()
    highest_earning_country_percentage = round(
        (country_earning / country_total * 100).max(), 1)

# Verifica a ocupação mais comum entre os indianos que ganham mais de 50K
    top_IN_occupation = (df[(df['native-country'] == 'India') &
                         (df['salary'] == '>50K')]['occupation'].value_counts().idxmax())

    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(
            f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(
            f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(
            f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(
            f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
