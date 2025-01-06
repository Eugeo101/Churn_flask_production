from flask import Blueprint, render_template, request, jsonify
from .utils import extract_product_engagement
import pandas as pd
import joblib
import cloudpickle

from sklearn.base import TransformerMixin, BaseEstimator
import numpy as np

class LogTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.n_features_in = X.shape[1]
        return self

    def transform(self, X, y=None):
        assert self.n_features_in == X.shape[1]
        return np.log(X)

main = Blueprint('main', __name__)


# stacking_pipeline = joblib.load("./stacking_pipeline.pkl")

# import os
# print(os.getcwd() + '\\cloud_stacking_pipeline.pkl')
# with open(os.getcwd() + '\\stacking_pipeline.pkl', "rb") as f:
#     stacking_pipeline = joblib.load(f)

import dill
with open('model.dill', 'rb') as f:
    stacking_pipeline = dill.load(f)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/visualizations')
def visualizations():
    return render_template('visualizations.html')

@main.route('/predict', methods=['GET', 'POST'])
def predict():
    prediction = None
    if request.method == 'POST':
        try:
            # Extract data from the form and process it
            data = {
                'CreditScore': float(request.form.get('CreditScore')),
                'Geography': request.form.get('Geography'),
                'Gender': request.form.get('Gender'),
                'Age': int(request.form.get('Age')),
                'Tenure': int(request.form.get('Tenure')),
                'Balance': float(request.form.get('Balance')),
                'NumOfProducts': int(request.form.get('NumOfProducts')),
                'HasCrCard': int(request.form.get('HasCrCard')),
                'IsActiveMember': int(request.form.get('IsActiveMember')),
                'EstimatedSalary': float(request.form.get('EstimatedSalary'))
            }

            # Generate the `products_engagement` feature
            data['products_engagment'] = extract_product_engagement(data)

            # Convert the input into a DataFrame for model prediction
            input_df = pd.DataFrame(data, index=[0])

            # Make the prediction
            pred = stacking_pipeline.predict(input_df)
            # Map the prediction to a meaningful message
            if pred == 1:
                prediction = "Predicted churn likelihood: The customer is likely to churn."
            else:
                prediction = "Predicted churn likelihood: The customer is not likely to churn."

        except Exception as e:
            prediction = f"Error: {e}"
    
    return render_template('prediction.html', prediction=prediction)
