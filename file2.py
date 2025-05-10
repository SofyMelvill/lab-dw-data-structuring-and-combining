import pandas as pd
url = 'https://raw.githubusercontent.com/data-bootcamp-v4/data/main/file2.csv'
file2_df = pd.read_csv(url)

# format column names
def formating_column_names(file2_df):
    file2_df.columns = file2_df.columns.str.strip().str.lower().str.replace(' ', '_', regex=False)
    return file2_df

# renaming the columns , in this case st for state
def rename_columns(file2_df):
    file2_df = file2_df.rename(columns={'st': 'state'})
    return file2_df


# correct bad written values (states, education, vehicle class, etc.)
def correct_values(file2_df):
    file2_df["state"] = file2_df["state"].replace({"Cali" : "California","CALI" : "California", "WA": "Washington", "Washington": "Washington", "AZ" : "Arizona"})
    file2_df["education"] = file2_df["education"].replace({"Bachelors": "Bachelor"})
    file2_df["vehicle_class"] = file2_df["vehicle_class"].replace({"Luxury SUV" : "Luxury", "Luxury Car" : "Luxury","Sports Car" : "Luxury"})
    return file2_df


# clean gender column
def clean_category(file2_df, column, replacement_map):
    if column not in file2_df.columns:
        raise ValueError(f"Column '{column}' not found.")
    file2_df[column] = file2_df[column].astype(str).str.strip().str.title().replace(replacement_map)
    return file2_df


# clean percentages 
def clean_percentages (file2_df, column):
    file2_df[column] = file2_df[column].astype(str).str.rstrip("%").astype(float)
    return file2_df

# convert columns to numeric
def convert_to_numeric(file2_df, column):
    file2_df[column] = pd.to_numeric(file2_df[column], errors="coerce")
    return file2_df

# fillna with median
def fillna_median(file2_df, column):
    median_ = file2_df[column].median()
    file2_df[column] = file2_df[column].fillna(median_)
    return file2_df

# fillna with mode
def fillna_mode(file2_df, column):
    if not isinstance(file2_df, pd.DataFrame):
        raise TypeError ("This is a series and we expected a DataFrame")

    mode_ = file2_df[column].mode()[0]
    file2_df[column] = file2_df[column].fillna(mode_)
    return file2_df

# remove all null rows
def remove_empty_rows(file2_df):
    return file2_df.dropna(how="all")

# verify duplicates - reminding that I choose not to remove duplicates
def check_duplicates(file2_df, column):
    duplicates = file2_df[file2_df[column].duplicated(keep=False)]
    if duplicates.empty:
        print(f"No duplicates found in the column '{column}'.")
    else:
        print(f"Duplicates found in columns '{column}':\n", duplicates[[column]])
    return file2_df

# Main function

def clean_file2(file2_df):
    file2_df = formating_column_names(file2_df)
    
    print("Available columns:", file2_df.columns.tolist())

    file2_df = rename_columns(file2_df)
    file2_df = correct_values(file2_df)
    file2_df = remove_empty_rows(file2_df)

    file2_df = clean_percentages (file2_df, "customer_lifetime_value")
    file2_df = convert_to_numeric(file2_df, "number_of_open_complaints")

    file2_df = fillna_median(file2_df, "customer_lifetime_value")
    file2_df = fillna_mode(file2_df, "gender")

    file2_df = clean_category(file2_df, "gender", {"Male" : "M","Female" : "F"})
    file2_df = clean_category(file2_df, "education", {})

    file2_df = check_duplicates(file2_df, "customer") # doesn't remove, just checks

    return file2_df