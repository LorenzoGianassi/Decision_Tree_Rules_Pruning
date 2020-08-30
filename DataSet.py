import pandas as pd
import random

# METDODO CHE LEGGE IL FILE CSV E LO TSFAROMA IN DTATFRAME LEVANDO VALORE ASSENTI
def create_dataframe():
    df = pd.read_csv("adult.csv")
    df.head()
    df = df[df['workclass'] != '?']
    df = df[df['occupation'] != '?']
    df = df[df['native-country'] != '?']
    df = df.reset_index(drop=True)
    return df


# METODO CHE SPLITTA IL DATAFRAME USATO PER OTTENERE TRAIN-SET,VALIDATION-SET E TEST-SET
def df_split(df, test_size):
    if isinstance(test_size, float):
        test_size = round(test_size * len(df))

    indices = df.index.tolist()
    test_indices = random.sample(population=indices, k=test_size)

    test_df = df.loc[test_indices]
    train_df = df.drop(test_indices)

    return train_df, test_df

