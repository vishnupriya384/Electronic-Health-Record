from flask import Flask, render_template, request
import pickle
import numpy as np

# Load Model
model = pickle.load(open('model.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/aboutus')
def about():
    return render_template("aboutus.html")

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        try:
            # Collect user inputs
            age = float(request.form['age'])
            weight = float(request.form['weight'])
            height = float(request.form['height'])
            bmi = float(request.form['bmi'])
            cycle = 1 if request.form['cycle'] == "I" else 0  # Convert R/I to 0/1
            cycle_length = float(request.form['cycle_length'])
            hair_loss = int(request.form['hair_loss'])
            pimples = int(request.form['pimples'])
            fast_food = int(request.form['fast_food'])
            reg_exercise = int(request.form['reg_exercise'])

            # Prepare input for model
            features = np.array([[age, weight, height, bmi, cycle, cycle_length, hair_loss, pimples, fast_food, reg_exercise]])

            # Make prediction
            prediction = model.predict(features)
            result_text = "PCOS Detected" if prediction[0] == 1 else "No PCOS"
            result_message = "It is advised to consult a doctor for further examination." if prediction[0] == 1 else "Your results are normal, but maintaining a healthy lifestyle is important."

            return render_template('result.html', prediction=result_text, result_message=result_message)

        except Exception as e:
            return f"Error: {e}"

    return render_template("predict.html")

@app.route('/result')
def result():
    return render_template("result.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
 app.run(debug=True)