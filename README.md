# Recipe ETL Script

This Python script performs ETL (Extract, Transform, Load) operations on recipe data. It fetches data from a specified URL, extracts recipes containing "Chilies" as an ingredient, calculates difficulty levels, and saves the results to a CSV file.

## Getting Started

### Prerequisites

- Python 3.7.9
- Required Python packages: `requests`, `pandas`

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Amar-Mahdy/recipes-etl.git
    cd recipe-etl
    ```

2. Navigate to the project directory:

    ```bash
    cd recipe-etl
    ```

3. Create a virtual environment (optional but recommended):

    ```bash
        python -m venv venv
        ```

4. Activate the virtual environment for (Mac):

    ```bash
        source venv/bin/activate
    ```

5. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

6. Run the script:

    ```bash
    python3 etl.py

    ```

### Output

The resulting DataFrame with recipes containing chilies will be saved to 'chilies_recipes.csv'.
