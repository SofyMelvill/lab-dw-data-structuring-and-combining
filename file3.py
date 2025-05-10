import pandas as pd
url_2 = 'https://raw.githubusercontent.com/data-bootcamp-v4/data/main/file3.csv'
file3_df = pd.read_csv(url_2)

# format column names
def formating_column_names(file3_df):
    file3_df.columns = file3_df.columns.str.strip().str.lower().str.replace(' ', '_', regex=False)
    return file3_df

# renaming the columns , in this case st for state
def rename_columns(file3_df):
    file3_df = file3_df.rename(columns={'st': 'state'})
    return file3_df


# correct bad written values (states, education, vehicle class, etc.)
def correct_values(file3_df):
    file3_df["state"] = file3_df["state"].replace({"Cali" : "California","CALI" : "California", "WA": "Washington", "Washington": "Washington", "AZ" : "Arizona"})
    file3_df["education"] = file3_df["education"].replace({"Bachelors": "Bachelor"})
    file3_df["vehicle_class"] = file3_df["vehicle_class"].replace({"Luxury SUV" : "Luxury", "Luxury Car" : "Luxury","Sports Car" : "Luxury"})
    return file3_df


# clean gender column
def clean_category(file3_df, column, replacement_map):
    if column not in file3_df.columns:
        raise ValueError(f"Column '{column}' not found.")
    file3_df[column] = file3_df[column].astype(str).str.strip().str.title().replace(replacement_map)
    return file3_df


# clean percentages 
def clean_percentages (file3_df, column):
    file3_df[column] = file3_df[column].astype(str).str.rstrip("%").astype(float)
    return file3_df

# convert columns to numeric
def convert_to_numeric(file3_df, column):
    file3_df[column] = pd.to_numeric(file3_df[column], errors="coerce")
    return file3_df

# fillna with median
def fillna_median(file3_df, column):
    median_ = file3_df[column].median()
    file3_df[column] = file3_df[column].fillna(median_)
    return file3_df

# fillna with mode
def fillna_mode(file3_df, column):
    if not isinstance(file3_df, pd.DataFrame):
        raise TypeError ("This is a series and we expected a DataFrame")

    mode_ = file3_df[column].mode()[0]
    file3_df[column] = file3_df[column].fillna(mode_)
    return file3_df

# remove all null rows
def remove_empty_rows(file3_df):
    return file3_df.dropna(how="all")

# verify duplicates - reminding that I choose not to remove duplicates
def check_duplicates(file3_df, column):
    duplicates = file3_df[file3_df[column].duplicated(keep=False)]
    if duplicates.empty:
        print(f"No duplicates found in the column '{column}'.")
    else:
        print(f"Duplicates found in columns '{column}':\n", duplicates[[column]])
    return file3_df

# Main function

def clean_file3(file3_df):
    file3_df = formating_column_names(file3_df)
    
    print("Available columns:", file3_df.columns.tolist())

    file3_df = rename_columns(file3_df)
    file3_df = correct_values(file3_df)
    file3_df = remove_empty_rows(file3_df)

    file3_df = clean_percentages (file3_df, "customer_lifetime_value")
    file3_df = convert_to_numeric(file3_df, "number_of_open_complaints")

    file3_df = fillna_median(file3_df, "customer_lifetime_value")
    file3_df = fillna_mode(file3_df, "gender")

    file3_df = clean_category(file3_df, "gender", {"Male" : "M","Female" : "F"})
    file3_df = clean_category(file3_df, "education", {})

    file3_df = check_duplicates(file3_df, "customer") # doesn't remove, just checks

    return file3_df