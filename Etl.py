import requests
import pandas as pd
import json
import logging

# Configure the logging module
logging.basicConfig(level=logging.INFO)

def load_data(url):
    """
    Fetch data from the provided URL and create a DataFrame.

    Parameters:
    - url (str): The URL to fetch data from.

    Returns:
    - pd.DataFrame: A DataFrame containing the data.
    """
    response = requests.get(url)

    if response.status_code == 200:
        try:
            json_lines = [json.loads(line) for line in response.text.split("\n") if line.strip()]
            df = pd.DataFrame(json_lines)
            return df
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON: {e}")
    else:
        raise ValueError(f"Failed to fetch data. Status code: {response.status_code}")

def extract_chilies_recipes(df):
    """
    Extract recipes with "Chilies" as one of the ingredients.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing recipes.

    Returns:
    - pd.DataFrame: A DataFrame with recipes containing "Chilies."
    """
    chili_keywords = ['Chilies', 'Chiles', 'Chili']
    chilies_recipes = df[df['ingredients'].apply(lambda x: any(keyword in str(x) for keyword in chili_keywords))]
    return chilies_recipes

def parse_duration(value):
    """
    Parse the duration string and return a timedelta.

    Parameters:
    - value (str): The duration string.

    Returns:
    - pd.Timedelta: The parsed duration.
    """
    try:
        if value:
            hours_pos = value.find('H')
            minutes_pos = value.find('M')

            if hours_pos > -1 and minutes_pos > -1:
                hours = int(value[2:hours_pos])
                minutes = int(value[hours_pos + 1:minutes_pos])
            elif hours_pos > -1:
                hours = int(value[2:hours_pos])
                minutes = 0
            elif minutes_pos > -1:
                hours = 0
                minutes = int(value[2:minutes_pos])
            else:
                return pd.Timedelta(0)

            return pd.Timedelta(hours=hours, minutes=minutes)
        else:
            return pd.Timedelta(0)
    except ValueError:
        return pd.Timedelta(0)

def calculate_difficulty(row):
    """
    Calculate difficulty based on prepTime and cookTime.

    Parameters:
    - row (pd.Series): A row from the DataFrame.

    Returns:
    - str: The difficulty level.
    """
    total_time = parse_duration(row['prepTime']) + parse_duration(row['cookTime'])
    if total_time > pd.to_timedelta('1 hour'):
        return 'Hard'
    elif pd.to_timedelta('30 minutes') <= total_time <= pd.to_timedelta('1 hour'):
        return 'Medium'
    elif total_time < pd.to_timedelta('30 minutes'):
        return 'Easy'
    else:
        return 'Unknown'

def main():
    """
    Main function to demonstrate loading data, extracting recipes, and saving to CSV.

    Usage:
    - Ensure that you have internet access to fetch data from the specified URL.
    - The resulting DataFrame with recipes containing "Chilies" will be saved to 'recipes-etl/chilies_recipes_test.csv'.

    """
    url = "https://bnlf-tests.s3.eu-central-1.amazonaws.com/recipes.json"

    try:
        recipes_df = load_data(url)
        chilies_recipes = extract_chilies_recipes(recipes_df).copy()
        chilies_recipes['difficulty'] = chilies_recipes.apply(calculate_difficulty, axis=1)
        file_path = 'chilies_recipes.csv'
        chilies_recipes.to_csv(file_path, index=False)
        logging.info("Recipes with Chilies as an ingredient and difficulty added to a CSV file: %s", file_path)
    except ValueError as e:
        logging.error(e)

if __name__ == "__main__":
    main()


