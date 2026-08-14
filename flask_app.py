from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__, template_folder=".")

@app.route("/")
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.route("/api/digipin/<code_id>")
def get_digipin_data(code_id):
    clean = code_id.upper().replace("-", " ")
    if "M9F" in clean:
        return jsonify({
            "digipin": "M9F-4LLM-LFC",
            "lat": 11.1477, "lon": 77.1408,
            "name": "KPR Institute of Engineering & Technology, Coimbatore",
            "patta": "2045", "owner": "KPR Educational Trust",
            "survey": "162/3A", "district": "Coimbatore - 641407"
        })
    return jsonify({
        "digipin": "M8J-LJLC-5C2",
        "lat": 10.4326, "lon": 79.3184,
        "name": "Adambai South, Pattukkottai, Thanjavur",
        "patta": "1408", "owner": "Selvakumar Panneerselvam",
        "survey": "142/2A", "district": "Thanjavur - 614602"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
