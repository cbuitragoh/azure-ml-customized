import mlflow
import argparse
import glob
import os

import pandas as pd
from sklearn.preprocessing import StandardScaler 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier


# define functions
def main(args):
    #enable autologging
    mlflow.autolog()

    # read data
    data = get_csvs_df(args.training_data)

    # create estimator
    estimator = AdaBoostClassifier(n_estimators=args.n_estimators,
                                   learning_rate=args.learning_rate,
                                   random_state=args.random_state)

    # train model
    train_model(estimator=estimator, df=data)


def get_csvs_df(path):
    if not os.path.exists(path):
        raise RuntimeError(f"Cannot use non-existent path provided: {path}")
    csv_files = glob.glob(f"{path}/*.csv")
    if not csv_files:
        raise RuntimeError(f"No CSV files found in provided data path: {path}")
    return pd.concat((pd.read_csv(f) for f in csv_files), sort=False)


def train_model(estimator, df:pd.DataFrame):
    #replace , in_shazam_charts
    df["in_shazam_charts"] = df["in_shazam_charts"].apply(
                                lambda x: float(str(x).replace(',', '')) 
                                if (',' in str(x)) else float(x))
    
    #fillna in_shazam_charts
    df["in_shazam_charts"].fillna(df["in_shazam_charts"].mean(), inplace=True)

    #fillna key: mode = C#
    mode = df["key"].mode()
    df["key"].fillna(mode.values[0], inplace=True)

    #transform target column "in_spotify_playlists"
    in_spotify_playlists = df.in_spotify_playlists.values
    df.loc[df["in_spotify_playlists"] < int(in_spotify_playlists.mean()), 
           "in_spotify_playlists"] = 0
    df.loc[df["in_spotify_playlists"] >= int(in_spotify_playlists.mean()), 
           "in_spotify_playlists"] = 1

    # tranform the released_year to age_of_song
    df.rename(columns={"released_year": "age_of_song"}, inplace=True)
    df["age_of_song"] = df["age_of_song"].apply(lambda x: 2023-x)

    # Encoding data
    categorical_columns = df.select_dtypes(["object"])
    column_list = list(categorical_columns.columns)
    df2 = pd.get_dummies(
                        df,
                         prefix=column_list,
                         columns=column_list,
                         drop_first=True
        )

    #select target column for predictions
    y = df2["in_spotify_playlists"].values
    df2.drop(columns="in_spotify_playlists", inplace=True)
    scaler = StandardScaler()
    scaler.fit(df2)
    X = scaler.transform(df2)

    #split data
    X_train, X_test, y_train, y_test = train_test_split(
                                                        X,
                                                        y,
                                                        test_size=0.3,
                                                        random_state=42
                                        )

    #train estimator
    estimator.fit(X_train, y_train)


def parse_args():
    # setup arg parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--training_data", type=str)
    parser.add_argument("--n_estimators", type=int, default=100)
    parser.add_argument("--learning_rate", type=float, default=0.1)
    parser.add_argument("--random_state", type=int, default=42)

    # parse args
    args = parser.parse_args()
    print("args parsed")
    # return args
    return args


# run script here
if __name__ == "__main__":
    # add space in logs
    print("\n\n")
    print("*" * 60)

    # parse args
    args = parse_args()

    # run main function
    main(args)

    # add space in logs
    print("*" * 60)
    print("\n\n")