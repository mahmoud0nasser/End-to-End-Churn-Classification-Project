import pandas as pd
from .request import CustomerData

def predict_new(data: CustomerData, pipeline, model):
    """
    Predicts customer churn using a trained model and preprocessing pipeline.

    Args:
        data (CustomerData): A Pydantic model containing customer features.
        pipeline (sklearn.Pipeline): A preprocessing pipeline used to transform the input data.
        model (sklearn.base.BaseEstimator): A trained machine learning model with `predict` and `predict_proba` methods.

    Returns:
        dict: A dictionary with the following keys:
            - "churn_prediction" (bool): True if the model predicts the customer will churn, False otherwise.
            - "churn_probability" (float): The probability that the customer will churn.
    """
    
    # to DF
    df = pd.DataFrame([data.model_dump()])
    
    # transform(Preprocessing)
    X_processed = pipeline.transform(df)
    
    # predict
    y_pred = model.predict(X_processed)
    y_prob = model.predict_proba(X_processed)

    return {
        "churn_prediction": bool(y_pred[0]),
        "churn_probability": float(y_prob[0][1])
    }