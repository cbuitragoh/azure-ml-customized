# Import libraries
import mlflow
import argparse
import glob
import os

import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

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

    df["in_shazam_charts"] = df["in_shazam_charts"].apply(
                                    lambda x: float(str(x).replace(',', '')) 
                                    if (',' in str(x)) else float(x)
                                    )

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

    target_col = df["in_spotify_playlists"].values
    df.drop(columns="in_spotify_playlists", inplace=True)

    # tranform the released_year to age_of_song
    df.rename(columns={"released_year": "age_of_song"}, inplace=True)
    df["age_of_song"] = df["age_of_song"].apply(lambda x: 2023-x)

    num_cols = ['artist_count', 'age_of_song', 'released_month', 
                'released_day', 'in_spotify_charts', 'in_apple_playlists',
                'in_apple_charts', 'in_deezer_charts', 'in_shazam_charts',
                'bpm', 'danceability_%', 'valence_%', 'energy_%',
                'acousticness_%', 'instrumentalness_%', 'liveness_%',
                'speechiness_%']
    
    cat_cols = ['track_name', 'artist(s)_name', 'streams', 
                'in_deezer_playlists', 'key', 'mode']
    
    num_pipeline = Pipeline(steps=[
        ('impute', SimpleImputer(strategy='mean')),
        ('scale',StandardScaler())
        ])
    cat_pipeline = Pipeline(steps=[
        ('impute', SimpleImputer(strategy='most_frequent')),
        ('one-hot',OneHotEncoder(handle_unknown='ignore', sparse=False))
            ])
    
    col_trans = ColumnTransformer(transformers=[
        ('num_pipeline',num_pipeline,num_cols),
        ('cat_pipeline',cat_pipeline,cat_cols)
        ],
        remainder='drop',
        n_jobs=-1)
    
    clf = estimator
    clf_pipeline = Pipeline(steps=[
        ('col_trans', col_trans),
        ('model', clf)
        ])
    
    X = df[num_cols+cat_cols]
    y = target_col
    # train test split
    X_train, X_test, y_train, y_test = train_test_split(
                                                        X,
                                                        y,
                                                        test_size=0.2,
                                                        stratify=y
                                        )

    clf_pipeline.fit(X_train, y_train)


def parse_args():
    # setup arg parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--training_data", dest='training_data',
                        type=str)
    parser.add_argument("--n_estimators", dest="n_estimators",
                        type=int, default=100)
    parser.add_argument("--learning_rate", dest="learning_rate",
                        type=float, default=0.1)
    parser.add_argument("--random_state", dest="random_state",
                        type=int, default=42)

    # parse args
    args = parser.parse_args()

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