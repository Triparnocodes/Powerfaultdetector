# from flask import Flask, render_template, request
# import joblib
# import numpy as np
# import os

# app = Flask(__name__)

# # --- Load Model ---
# model_path = os.path.join(os.path.dirname(__file__), "..", "model", "fault_detector.pkl")
# model = joblib.load(model_path)

# @app.route("/")
# def index():
#     return render_template("form.html")

# @app.route("/predict", methods=["POST"])
# def predict():
#     try:
#         # Read values from the form
#         current = float(request.form["current"])
#         phase_voltage = float(request.form["phase_voltage"])
#         line_voltage = float(request.form["line_voltage"])

#         # Format for model input
#         input_arr = np.array([[current, phase_voltage, line_voltage]])

#         # Predict
#         result = model.predict(input_arr)[0]

#         # Return result page
#         return render_template(
#             "result.html",
#             current=current,
#             phase_voltage=phase_voltage,
#             line_voltage=line_voltage,
#             result=result
#         )
#     except Exception as e:
#         return f"⚠ Error: {e}"

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request
import joblib
import numpy as np
import os

app = Flask(__name__)

# ----- Load Model Safely -----
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
model_path = os.path.join(base_dir, "model", "fault_detector.pkl")

print("Loading model from:", model_path)
model = joblib.load(model_path)

# ----- Safe float converter -----
def safe_float(value):
    try:
        return float(value)
    except:
        return None

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/predict", methods=["POST"])
def predict():
    # Retrieve raw input text
    raw_current = request.form["current"].strip()
    raw_phase_voltage = request.form["phase_voltage"].strip()
    raw_line_voltage = request.form["line_voltage"].strip()

    # Convert to float if possible
    current = safe_float(raw_current)
    phase_voltage = safe_float(raw_phase_voltage)
    line_voltage = safe_float(raw_line_voltage)

    # If any value couldn't be parsed → invalid
    if current is None or phase_voltage is None or line_voltage is None:
        return render_template(
            "result.html",
            current=raw_current,
            phase_voltage=raw_phase_voltage,
            line_voltage=raw_line_voltage,
            result="⚠ Invalid input format! Please enter only numbers."
        )

    # Make prediction
    prediction = model.predict(np.array([[current, phase_voltage, line_voltage]]))[0]

    return render_template(
        "result.html",
        current=current,
        phase_voltage=phase_voltage,
        line_voltage=line_voltage,
        result=prediction
    )

if __name__ == "__main__":
    app.run(debug=True)
