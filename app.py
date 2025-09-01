from flask import Flask, render_template, request, jsonify
import mysql.connector
import openai

app = Flask(_name_)

# 🔑 Configure OpenAI (replace with your actual API key)
openai.api_key = "https://api.dreaded.site/api/chatgpt?text=$"

# 📦 Configure MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="recipe_db"
)
cursor = db.cursor(dictionary=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_recipes", methods=["POST"])
def get_recipes():
    data = request.json
    ingredients = data.get("ingredients", "")

    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    # 🔮 Query OpenAI for recipes
    prompt = f"Suggest 3 simple recipes using these ingredients: {ingredients}. Format as Title - Ingredients - Instructions."
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=300
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    recipes_text = response.choices[0].text.strip().split("\n\n")

    recipe_data = []
    for recipe in recipes_text:
        parts = recipe.split("-")
        if len(parts) >= 3:
            title, ing, instr = parts[0].strip(), parts[1].strip(), parts[2].strip()
            recipe_data.append({
                "title": title,
                "ingredients": ing,
                "instructions": instr
            })

            # Save to DB
            try:
                cursor.execute(
                    "INSERT INTO recipes (user_id, title, ingredients, instructions) VALUES (%s, %s, %s, %s)",
                    (1, title, ing, instr)
                )
                db.commit()
            except Exception as e:
                print("DB Insert Error:", e)

    return jsonify(recipe_data)

if _name_ == "_main_":
    app.run(debug=True)
