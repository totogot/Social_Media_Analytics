import xgboost as xgb
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.svm import LinearSVC
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression



def test_classification(X_train, y_train, X_test, y_test, arg_dict):

    # dictionary of models supported by test function
    modelDict = {
        'LogisticRegression': train_LogisticRegression,
        'LinearSVC': train_LinearSVC,
        'XGBClassifier': train_XGBoost
    }

    model_selection = arg_dict['models']
    report_outputs = arg_dict['response_types']

    for k, v in model_selection.items():
        # output predictions
        if k not in modelDict.keys():
            raise ValueError(f'model of type {k} not available')
        else:
            print(f'Training {k} model \n\n')
            predictions = modelDict[k](X_train, y_train, X_test, v, return_model = False)
        
        # output accuacy report
        if 'classification_report' in report_outputs:
            print(classification_report(y_test, predictions))

        if 'confusion_matrix' in report_outputs:
            plot_confusion(k, y_test, predictions)

    return


def train_LogisticRegression(X_train, y_train, X_test, args, return_model):

    # add a fixed random state to ensure more repeatable results
    args['random_state'] = 1

    # train classifier
    logreg = LogisticRegression(**args)
    logreg.fit(X_train, y_train)

    # run predictions
    predictions = logreg.predict(X_test)

    if return_model == True:
        return logreg

    return predictions


def train_LinearSVC(X_train, y_train, X_test, args, return_model):

    # add a fixed random state to ensure more repeatable results
    args['random_state'] = 1

    # train classifier
    supvec = LinearSVC(**args)
    supvec.fit(X_train, y_train)

    # run predictions
    predictions = supvec.predict(X_test)

    if return_model == True:
        return supvec

    return predictions


def train_XGBoost(X_train, y_train, X_test, args, return_model):

    # add a fixed random state to ensure more repeatable results
    args['random_state'] = 1

    # encode the categorical variable strings as numeric
    encoder = LabelEncoder()
    encoder.fit(y_train)
    
    encoder_mapping = dict(zip(encoder.classes_, encoder.transform(encoder.classes_)))
    print('Categorical variables encoded: ', encoder_mapping)

    y_train_encoded = encoder.transform(y_train)

    # train classifier
    gradboost = xgb.XGBClassifier(random_state = 1)
    gradboost.fit(X_train, y_train_encoded)

    # run predictions
    predictions_encoded = gradboost.predict(X_test)
    predictions = encoder.inverse_transform(predictions_encoded)

    if return_model == True:
        return gradboost

    return predictions


def plot_confusion(k, y_test, predictions):

    labels = sorted(set(y_test))
    cf_matrix = confusion_matrix(y_test, predictions)

    plt.figure(figsize = (12,12))
    ax = sns.heatmap(cf_matrix, annot=True, cmap='Blues', fmt='d')

    ax.set_title(f'{k} Confusion Matrix\n\n');
    ax.set_xlabel('\nPredicted Values')
    ax.set_ylabel('Actual Values ');

    ## Ticket labels - List must be in alphabetical order
    ax.xaxis.set_ticklabels(labels, rotation=90)
    ax.yaxis.set_ticklabels(labels, rotation=0)

    ## Display the visualization of the Confusion Matrix.
    plt.show()

    return