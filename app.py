from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        age = int(request.form['age'])
        gender = request.form['gender']
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        goal = request.form['goal']
        activity = request.form['activity']

        # BMI
        bmi = round(weight / ((height / 100) ** 2), 2)
        if bmi < 18.5:
            bmi_status = "Underweight"
        elif 18.5 <= bmi < 25:
            bmi_status = "Normal"
        elif 25 <= bmi < 30:
            bmi_status = "Overweight"
        else:
            bmi_status = "Obese"

        # Ideal weight range (based on BMI 18.5–24.9)
        min_ideal_weight = round(18.5 * ((height / 100) ** 2), 1)
        max_ideal_weight = round(24.9 * ((height / 100) ** 2), 1)

        # BMR (Mifflin-St Jeor)
        if gender == 'male':
            bmr = round(10 * weight + 6.25 * height - 5 * age + 5)
        else:
            bmr = round(10 * weight + 6.25 * height - 5 * age - 161)

        # Activity factors
        activity_factors = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }
        tdee = round(bmr * activity_factors.get(activity, 1.55))

        # Adjust calories based on goal
        if goal == 'maintenance':
            calories = tdee
            note = "Maintain your current weight and performance."
        elif goal == 'gain':
            calories = round(tdee * 1.12)
            note = "Eat a small calorie surplus with strength training for muscle gain."
        elif goal == 'cut':
            calories = round(tdee * 0.82)
            note = "Eat in a small deficit, keep protein high for fat loss."
        elif goal == 'strength':
            calories = round(tdee * 1.05)
            note = "Small surplus, focus on progressive overload for strength."

        # Estimate Body Fat % (using BMI-based formula)
        if gender == 'male':
            body_fat = round(1.20 * bmi + 0.23 * age - 16.2, 1)
        else:
            body_fat = round(1.20 * bmi + 0.23 * age - 5.4, 1)
        body_fat = max(2, min(body_fat, 50))  # reasonable limits

        # Lean Body Mass (LBM)
        lbm = round(weight * (1 - body_fat / 100), 1)

        # Macros
        protein = round(weight * (2.0 if goal == 'cut' else 1.6))
        fat = round((0.25 * calories) / 9)
        carbs = round((calories - (protein * 4) - (fat * 9)) / 4)

        # Health interpretation
        if bmi < 18.5:
            health_comment = "You're underweight. Try increasing calorie intake with balanced nutrition."
        elif 18.5 <= bmi < 25:
            health_comment = "You're in a healthy range. Focus on maintaining muscle and strength."
        elif 25 <= bmi < 30:
            health_comment = "You're slightly overweight. A calorie deficit and regular exercise can help."
        else:
            health_comment = "High BMI — consider a structured plan for fat loss and activity."

        result = {
            'bmi': bmi,
            'bmi_status': bmi_status,
            'bmr': bmr,
            'tdee': tdee,
            'calories': calories,
            'protein': protein,
            'fat': fat,
            'carbs': carbs,
            'body_fat': body_fat,
            'lbm': lbm,
            'note': note,
            'health_comment': health_comment,
            'min_ideal_weight': min_ideal_weight,
            'max_ideal_weight': max_ideal_weight
        }

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
