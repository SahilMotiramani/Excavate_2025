from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

dataset_path = "data/dataset_excavate.xlsx - Sheet 1.csv"
df = pd.read_csv(dataset_path)
df.columns = df.columns.str.strip()
functional_groups = df["functional group"].unique().tolist()

fake_classification_model = "data/best_xgboost_regressor"
fake_regression_model = "regression_model"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        selected_group = request.form.get("functional_group")
        band_gap_column = [col for col in df.columns if "band gap" in col.lower()]
        if band_gap_column:
            band_gap_column = band_gap_column[0]
            band_gap = df[df["functional group"] == selected_group][band_gap_column].values
            if len(band_gap) > 0:
                band_gap_value = band_gap[0]
                material_type = "Insulator" if band_gap_value >= 0.5 else "Non-Insulator"
            else:
                band_gap_value = "N/A"
                material_type = "Unknown"

            classification_prediction = "Insulator" if band_gap_value >= 0.5 else "Non-Insulator"
            regression_prediction = band_gap_value

            result = {
                "selected_group": selected_group,
                "band_gap": band_gap_value,
                "material_type": material_type,
                "classification_model_output": classification_prediction,
                "regression_model_output": regression_prediction
            }
    return render_template("index.html", functional_groups=functional_groups, result=result)

if __name__ == "__main__":
    app.run(debug=True)
