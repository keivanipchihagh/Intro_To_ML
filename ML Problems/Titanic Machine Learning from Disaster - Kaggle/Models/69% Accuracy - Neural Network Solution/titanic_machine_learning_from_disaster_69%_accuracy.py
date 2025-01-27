# -*- coding: utf-8 -*-
"""Titanic Machine Learning from Disaster - 69% Accuracy.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WuUlOQmxx2m-1vIgEi4VR5IlcOhXBf5_

# Titanic: Machine Learning from Disaster

Problem overview from [Kaggle](https://www.kaggle.com/c/titanic/overview).

Problem datasets from [GitHub](https://github.com/keivanipchihagh/Intro_to_DataScience/tree/main/Titanic%20Machine%20Learning%20from%20Disaster/Datasets)

Problem notebook & solution from [Notebook](https://www.kaggle.com/startupsci/titanic-data-science-solutions)

## Import Tools
"""

# Data analysis library
import pandas as pd

# Data manipulation library
import numpy as np

# Data visualization libraries
from matplotlib import pyplot as plt
import seaborn as sns

# Save
from google.colab import files

# Deep learnig library
import keras

"""## Data Analysis & Data manipulation

### Load datasets
"""

# Training data
train_data = pd.read_csv('https://raw.githubusercontent.com/keivanipchihagh/Intro_to_DS_and_ML/master/Deep%20Learning%20Problems/Titanic%20Machine%20Learning%20from%20Disaster%20-%20Kaggle/Datasets/train.csv')

# Test data
test_data = pd.read_csv('https://raw.githubusercontent.com/keivanipchihagh/Intro_to_DS_and_ML/master/Deep%20Learning%20Problems/Titanic%20Machine%20Learning%20from%20Disaster%20-%20Kaggle/Datasets/test.csv')

"""### Getting to know the dataset"""

train_data.info()
# train_data.head()

"""### Age

Is column 'Age' a factor in how many souls survived? **Clearly**
"""

graph = sns.FacetGrid(data = train_data, col = 'Survived')
graph.map(plt.hist, 'Age')

"""Column 'Age' contains **891** values for the train data, from which **19.82%** are *NULL* values."""

print('Number of entries for "Age" in train data:', len(train_data['Age']))
print('Number of NULL entries for "Age" in train data:', len(train_data[train_data['Age'].isnull()]), end = '\n' * 2)

print('Number of entries for AGE in test data is:', len(test_data['Age']))
print('Number of NULL entries for "Age" in test data:', len(test_data[test_data['Age'].isnull()]))

"""Filling the *NULL* values with column's **mean** is likely to solve the problem"""

def fix_Age(dataset):
  mean = dataset['Age'].mean() # Get the mean
  dataset['Age'].fillna(value = mean, inplace = True) # Fill NAs inplace

  dataset['AgeBand'] = pd.cut(dataset['Age'], 5)

  # Covert to categorical
  dataset.loc[ dataset['Age'] <= 16, 'Age'] = 0
  dataset.loc[(dataset['Age'] > 16) & (dataset['Age'] <= 32), 'Age'] = 1
  dataset.loc[(dataset['Age'] > 32) & (dataset['Age'] <= 48), 'Age'] = 2
  dataset.loc[(dataset['Age'] > 48) & (dataset['Age'] <= 64), 'Age'] = 3
  dataset.loc[ dataset['Age'] > 64, 'Age']

  dataset['Age'] = dataset['Age'].astype(int)

  # Drop column
  dataset.drop(columns = ['AgeBand'], inplace = True)

fix_Age(train_data)  # Fix train data
fix_Age(test_data)   # Fix test data

"""Now let's convert the numerical 'Age' column into a categorical"""

train_data.head()

"""### Sex

Is column 'Sex' relavant to the number of souls survived? **Yes**, females are likely to have survived
"""

train_data[['Sex', 'Survived']].groupby('Sex', as_index = False).mean().sort_values(by = 'Survived', ascending = True)

# Visualization
# graph = sns.FacetGrid(data = train_data, col = 'Sex')
# graph.map(plt.hist, 'Survived')

"""Column 'Sex' does not contain any *NULLs*, however it must be feature engineered to satisfy the model."""

def fix_Sex(dataset):
  dataset['Sex'] = dataset['Sex'].map({'male': 0, 'female': 1}).astype(int) # Map

fix_Sex(train_data)
fix_Sex(test_data)

train_data.head()

"""### PassengerId

Is 'PassengerId' a factor indicating how many souls survived? **Nope**
"""

graph = sns.FacetGrid(data = train_data, col = 'Survived')
graph.map(plt.hist, 'PassengerId')

"""Simply enough, we can remove the column from our dataset"""

def fix_PassengerId(dataset):
  dataset.drop(columns = ['PassengerId'], inplace = True)

fix_PassengerId(train_data)

# Save PassengerIds for future reference
test_data_PassengerId = test_data['PassengerId']
fix_PassengerId(test_data)

train_data.head()

"""### Pclass

Does column 'Pclass' impact the rate of survived souls? **Statistics show positive**
"""

# train_data['Pclass'].unique()

train_data[['Pclass', 'Survived']].groupby('Pclass', as_index = False).mean().sort_values(by = 'Pclass', ascending = True)

# Visualization
# graph = sns.FacetGrid(data = train_data, col = 'Survived')
# graph.map(plt.hist, 'Pclass')

"""### Cabin

Does column 'Cabin' have any impact on survival rate? **Can't know**
"""

train_data_Cabin_all_entries = len(train_data['Cabin'])
train_data_Cabin_null_entries = len(train_data[train_data['Cabin'].isnull()])

print('Number of entries in train data for "Cabin":', train_data_Cabin_all_entries)
print('Number of NULL entries in train data for "Cabin":', train_data_Cabin_null_entries)
print('Ratio: ', str(train_data_Cabin_null_entries / train_data_Cabin_all_entries * 100)[:4], '% of the enties are NULL!', sep = '', end = '\n' * 2)

test_data_Cabin_all_entries = len(test_data['Cabin'])
test_data_Cabin_null_entries = len(test_data[test_data['Cabin'].isnull()])

print('Number of entries in test data for "Cabin":', test_data_Cabin_all_entries)
print('Number of NULL entries in test data for "Cabin":', test_data_Cabin_null_entries)
print('Ratio: ', str(test_data_Cabin_null_entries / test_data_Cabin_all_entries * 100)[:4], '% of the enties are NULL!', sep = '')

"""Solution: Drop the column"""

def fix_Cabin(dataset):
  dataset.drop(columns = ['Cabin'], inplace = True)

fix_Cabin(train_data)
fix_Cabin(test_data)

train_data.head()

"""### Ticket

Column 'Ticket' cannot be used due to its variaty of entries
"""

print('There are', len(train_data['Ticket'].unique()), 'unique entries for the column "Ticket"')

"""Solution: Column must be dropped"""

def fix_Ticket(dataset):
  dataset.drop(columns = ['Ticket'], inplace = True)

fix_Ticket(train_data)
fix_Ticket(test_data)

train_data.head()

"""### Embarked

Is column 'Embarked' effective on how many souls survive? **It is**
"""

print('Unique entries for "Embarked":', train_data['Embarked'].unique())
print('NULL entries for "Embarked":', len(train_data[train_data['Embarked'].isnull()]))

train_data[['Survived', 'Embarked']].groupby('Embarked', as_index = False).mean().sort_values(by = 'Survived', ascending = False)

"""We have 2 *NULL* entries for the column 'Embarked' which can be removed from the dataset. We aslo need to do a feature engieering for this column so it will satisfy the model"""

def fix_Embarked(dataset):
  dataset.dropna(axis = 0, subset = ['Embarked'], inplace = True)
  dataset['Embarked'] = dataset['Embarked'].map({'C': 0, 'Q': 1, 'S': 2})

fix_Embarked(train_data)
fix_Embarked(test_data)

print('Unique entries for "Embarked":', train_data['Embarked'].unique())
print('NULL entries for "Embarked":', len(train_data[train_data['Embarked'].isnull()]))

train_data.info()

"""### SibSp & Parch

Does the columns 'SibSp' & 'parch' have impact on the number of souls survived? **They do**
"""

train_data[['SibSp', 'Survived']].groupby('SibSp', as_index = False).mean().sort_values(by = 'Survived', ascending = False)

train_data[['Parch', 'Survived']].groupby('Parch', as_index = False).mean().sort_values(by = 'Survived', ascending = False)

"""Note that instead of having the two columns seperatly, we can combine them and create a new column instead and call it: 'FamilySize'

Although 'FamilySize' is not directly related to survival rate, we will use this column further down the road
"""

def fix_SibSp_Parch(dataset):
  # Create column
  dataset['FamilySize'] = dataset['Parch'] + dataset['SibSp'] + 1

  # Drop column
  dataset.drop(columns = ['SibSp', 'Parch'], inplace = True)

fix_SibSp_Parch(train_data)
fix_SibSp_Parch(test_data)

train_data.head()

"""Now we can analyse the impact of 'FamilySize' on the survival rate"""

train_data[['FamilySize', 'Survived']].groupby('FamilySize').mean().sort_values(by = 'Survived', ascending = False)

"""### Name

Column 'Name' is in-directly related to the survival rate when feature extraction is performed. We can do feature engineering and extract *Title* for each individual. After cleaning up the titles, we'll have to map them into numerical type. Finally dropping the 'Name' column
"""

def fix_Name(dataset):
  # Title Extraction
  dataset['Title'] = dataset['Name'].str.extract(' ([A-Za-z]+)\.', expand = False)

  # Cleanig up
  dataset['Title'] = dataset['Title'].replace(['Lady', 'Countess','Capt', 'Col', 'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')

  # Check mis-spellings
  dataset['Title'] = dataset['Title'].replace('Mlle', 'Miss').replace('Ms', 'Miss').replace('Mme', 'Mrs')

  # Mapping
  dataset['Title'] = dataset['Title'].map({"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Rare": 5})

  # Drop
  dataset.drop(columns = ['Name'], inplace = True)

fix_Name(train_data)
fix_Name(test_data)

pd.crosstab(train_data['Title'], train_data['Sex'])
train_data.head()

"""### IsAlone

Does the fact that an individual is alone or not have an impact on his/her survival? **We'll see**

We will drop the 'FamilySize' since it does not have direct impact on survival rate
"""

def fix_IsAlone(dataset):
  # Create column
  dataset['IsAlone'] = np.where(dataset['FamilySize'] == 1, 1, 0)

  # Drop 'FamilySize'
  dataset.drop(columns = ['FamilySize'], inplace = True)

fix_IsAlone(train_data)
fix_IsAlone(test_data)

train_data[['IsAlone', 'Survived']].groupby('IsAlone').mean().sort_values(by = 'Survived', ascending = False)
# train_data.head()

"""### Fare

First, we deal with the *NULL* values in the test data
"""

mean = test_data['Fare'].mean()
test_data['Fare'].fillna(value = mean, inplace = True)

"""Now let's convert 'Fare' column into categorical"""

def fix_Fare(dataset):
  dataset['FareBand'] = pd.qcut(dataset['Fare'], 4)

  # Convert into categorical
  dataset.loc[ dataset['Fare'] <= 7.91, 'Fare'] = 0
  dataset.loc[(dataset['Fare'] > 7.91) & (dataset['Fare'] <= 14.454), 'Fare'] = 1
  dataset.loc[(dataset['Fare'] > 14.454) & (dataset['Fare'] <= 31), 'Fare']   = 2
  dataset.loc[ dataset['Fare'] > 31, 'Fare'] = 3
  dataset['Fare'] = dataset['Fare'].astype(int)

  # Drop column
  dataset.drop(columns = ['FareBand'], inplace = True)

fix_Fare(train_data)
fix_Fare(test_data)

train_data.head()

"""## Neural Network

### Split & Shuffle Data
"""

train_labels = train_data['Survived']
train_data.drop(columns = ['Survived'], inplace = True, axis = 1)

# Shuffle data
train_data = train_data.iloc[np.random.permutation(len(train_data))]

"""### Build Model"""

def build_model(dataset):
  model = keras.models.Sequential()
  model.add(keras.layers.Dense(units = 32, activation = keras.activations.relu, input_shape = (dataset.shape[1], )))
  model.add(keras.layers.Dense(units = 32, activation = keras.activations.relu))
  model.add(keras.layers.Dense(units = 1))
  model.compile(optimizer = keras.optimizers.RMSprop(0.001), loss = keras.losses.mse, metrics = ['mse', 'accuracy'])

  return model

"""### Train Model"""

def train_model(model, batch_size, epochs):
  history = model.fit(x = train_data, y = train_labels, batch_size = batch_size, epochs = epochs, verbose = False)

  return history

"""### Visualize resutls"""

def visualize_model(history):

  # Calculate epochs
  epochs = range(0, len(history.history['loss']))

  plt.clf()
  plt.plot(epochs, history.history['loss'], 'b', label = 'Loss')
  plt.xlabel('Epochs')
  plt.ylabel('Loss')
  plt.legend()
  plt.show()

  plt.clf()
  plt.plot(epochs, history.history['accuracy'], 'r', label = 'Accuracy')
  plt.xlabel('Epochs')
  plt.ylabel('Accuracy')
  plt.legend()
  plt.show()

"""### All-In-One"""

# Build the model
model = build_model(train_data)
model.summary()

# Train the model
history = train_model(model, 32, 50)

# Visualize the model
visualize_model(history)

"""### Training results"""

# Print results
print('Max Accuracy:', max(history.history['accuracy']) * 100, '%')
print('Min Loss:', min(history.history['loss']) * 100, '%')

"""### Downloading predictions"""

def download_predictions(results):
  
  results.to_csv('results.csv')
  files.download('results.csv')

"""### Predicting"""

predictions = model.predict(test_data).astype(int)

results = pd.DataFrame()

# Convert to DataFrame
results['Survived'] = pd.DataFrame(predictions)

# Add PassengerId column
results['PassengerId'] = test_data_PassengerId

results = results.reindex(columns = ['PassengerId', 'Survived'])

print(results)

# Download predictions
download_predictions(results)