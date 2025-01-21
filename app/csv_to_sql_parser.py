import pandas as pd


def split_column_data(df, column_name):
    df[column_name] = df[column_name].dropna().str.split(", ")
    return df


if __name__ == "__main__":
    df = pd.read_csv("./data/netflix.csv")
    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
    df["release_year"] = pd.to_datetime(df["date_added"], errors="coerce")
    df = split_column_data(df, "cast")
    df = split_column_data(df, "country")
    df = split_column_data(df, "listed_in")
    df = split_column_data(df, "director")
