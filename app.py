from flask import Flask, request, jsonify 
from flask_cors import CORS 
import openai 
import os 
 
app = Flask(__name__) 
CORS(app) 
 
openai.api_key = os.getenv("OPENAI_API_KEY") 
 
@app.route("/") 
def index(): 
    return "API de correction HSE (via OpenAI) prˆte." 
 
@app.route("/api/corriger", methods=["POST"]) 
def corriger(): 
    data = request.get_json() 
    texte = data.get("texte", "") 
    if not texte.strip(): 
        return jsonify({"error": "Texte vide"}), 400 
    prompt = f"Corrige ce texte professionnellement sans changer le sens :\n\n{texte}" 
    try: 
        completion = openai.ChatCompletion.create( 
            model="gpt-3.5-turbo", 
            messages=[{"role": "user", "content": prompt}], 
            temperature=0.3, 
            max_tokens=500 
        ) 
        texte_corrige = completion.choices[0].message.content.strip() 
        return jsonify({"texte_corrige": texte_corrige}) 
    except Exception as e: 
        return jsonify({"error": str(e)}), 500 
