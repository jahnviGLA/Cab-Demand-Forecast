from flask import Flask, render_template, request
import joblib
import numpy as np

#initialize flask app
app = Flask(__name__)

#load your trained 10-feature model
model = joblib.load('model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        #get values entered in the form
        data = [float(x) for x in request.form.values()]

        #if fewer than 10 inputs are provided, pad with zeros
        while len(data) < 10:
            data.append(0.0)

        #convert to numpy array and reshape for prediction
        final_input = np.array(data).reshape(1, -1)

        #predict ride demand
        prediction = model.predict(final_input)
        output = round(prediction[0], 2)

        return render_template('index.html', prediction_text=f'Predicted Ride Demand: {output}')

    except Exception as e:
        return render_template('index.html', prediction_text=f'Error: {e}')

if __name__ == "__main__":
    app.run(debug=True)
