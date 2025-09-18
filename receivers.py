import pandas as pd
import numpy as np
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.model_selection import StratifiedKFold, GridSearchCV
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv("wrStats.csv") 

model = XGBClassifier(
    objective='binary:logistic',  # must be logistic for probabilities
    eval_metric='logloss',
    n_estimators=125,
    learning_rate=0.02,
    max_depth=3,
    scale_pos_weight=20,
    random_state=42
)

feature_cols = [                    #All the stat categories for training	
    "season",
    "receiving_yards",
    "yards_after_catch",
    "rush_attempts",
    "rush_touchdown",
    "pass_touchdown",
    "fumble",
    "receptions",
    "targets",
    "receiving_touchdown",
    "receptions_redzone",
    "targets_redzone",
    "receiving_touchdown_redzone",
    "fantasy_points_ppr",
    "offense_snaps",
    "total_tds",
    "touches",
    "total_yards",
    "games_missed",
    "age",
    "games_played_season"
    ]

for col in feature_cols:
    data[col] = pd.to_numeric(data[col], errors='coerce') #Goes Column by column to make sure data is numeric and fills it with 'NaN' if not

X = data[feature_cols]                  #Checks all Stat Groups
y = data["Top_10_Next_Season_or_Not"]   #Column of if they were top 10 the next season or not

train = data[data["season"] <= 2023]    #Train the model on all seasons before 2024
test  = data[data["season"] == 2024]    #Test the model on 2024 NFL season

X_train, Y_train = train[feature_cols], train["Top_10_Next_Season_or_Not"]  #Train model on the seasons before 2024 with the stat groups I picked to see if they were top 10 the next season or not
X_test, Y_test = test[feature_cols], test["Top_10_Next_Season_or_Not"]      #Test to see if the model can predict 2024 season

model.fit(X_train, Y_train)

probs = model.predict_proba(X_test) #gives probabilities for each player in format of array [Prob not top 10, Prob of top 10]

y_probs = probs[:, 1]  #Cuts off the prob of not being top 10, and just displays prob of top 10 in one array for each player in a row

players = data.loc[X_test.index, "player_name"] #Keep player names for 2024 and index them

data_probs = pd.DataFrame({"player_name": players, "prob_top10": y_probs})
data_probs = data_probs.sort_values(by="prob_top10", ascending=False)
pd.set_option('display.max_rows', None)  # show all rows
pd.options.display.float_format = '{:.4f}'.format
print(data_probs)

# xgb.plot_importance(model, importance_type='gain') #plots importance ranking of statistical features
# plt.show()

# param_grid = {                                #All hyperparameters I want to tune
#     "max_depth": [3, 4, 5],
#     "learning_rate": [0.01, 0.02, 0.03],
#     "n_estimators": [100, 125, 150],
#     }

# cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)   #Stratified K Fold to make sure the data isn't lopsided due to unevenness of correct/incorrect

# grid_search = GridSearchCV(estimator=model, param_grid=param_grid, scoring="roc_auc", cv=cv, n_jobs=-1)    #Grid search to make sure every possible combination is tested
# grid_search.fit(X_train, Y_train)

# results = pd.DataFrame(grid_search.cv_results_)

# pivot_table = results.pivot_table(
#     values='mean_test_score',
#     index='param_max_depth',
#     columns='param_learning_rate'
# )

# pivot_table2 = results.pivot_table(
#     values='mean_test_score',
#     index='param_max_depth',
#     columns='param_n_estimators'
# )


# pivot_table3 = results.pivot_table(
#     values='mean_test_score',
#     index='param_learning_rate',
#     columns='param_n_estimators'
# )

# plt.figure(figsize=(8,6))
# sns.heatmap(pivot_table, annot=True, cmap="viridis")
# plt.title("ROC-AUC for learning_rate vs max_depth")
# plt.show()

# plt.figure(figsize=(8,6))
# sns.heatmap(pivot_table2, annot=True, cmap="viridis")
# plt.title("ROC-AUC for max_depth vs n_estimators")
# plt.show()

# plt.figure(figsize=(8,6))
# sns.heatmap(pivot_table2, annot=True, cmap="viridis")
# plt.title("ROC-AUC for learning_rate vs n_estimators")
# plt.show()

