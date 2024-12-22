from flask import Flask, render_template, request, jsonify, send_from_directory
import openai
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Chargez les variables d'environnement
load_dotenv()

# Configurez votre clé API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        # Récupérez les données envoyées par le client
        prompt = request.json.get("prompt")
        type_request = request.json.get("type_request")

        # Validez les entrées
        if not prompt or not type_request:
            return jsonify({"error": "Les champs 'prompt' et 'type_request' sont requis."}), 400

        # Créez la question selon le type de demande
        if type_request == "idea":
            if "orgonite" in prompt.lower():
                question = f"Donne-moi des idées de projets DIY pour fabriquer des objets en orgonite..."
            elif "moteur stirling" in prompt.lower():
                question = f"Propose-moi des idées de projets DIY pour construire un moteur Stirling..."
            else:
                question = f"Donne-moi des idées de projets DIY basés sur ce thème ou matériel : {prompt}."

        elif type_request == "method":
            if "orgonite" in prompt.lower():
                question = f"Donne-moi des étapes détaillées pour fabriquer de l'orgonite..."
            elif "moteur stirling" in prompt.lower():
                question = f"Donne-moi des étapes détaillées pour construire un moteur Stirling..."
            else:
                question = f"Donne-moi des étapes détaillées pour réaliser ce projet DIY : {prompt}."

        else:
            return jsonify({"error": "Type de requête invalide."}), 400

        # Requête à l'API OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": question}],
            max_tokens=1500
        )

        # Récupérer la réponse d'OpenAI
        tutorial_response = response["choices"][0]["message"]["content"]

        # Générer un fichier texte avec les résultats
        file_name = f"tutorial_{type_request}_{prompt.replace(' ', '_')}.txt"
        file_path = os.path.join(app.root_path, 'static', 'downloads', file_name)
        
        # Sauvegarder la réponse d'OpenAI dans un fichier
        with open(file_path, 'w') as f:
            f.write(tutorial_response)

        # Retourner la réponse à l'utilisateur avec le lien pour télécharger le fichier
        return jsonify({
            "response": tutorial_response,
            "download_link": f"/download/{file_name}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour télécharger les fichiers générés
@app.route("/download/<filename>")
def download_file(filename):
    # Répertoire de stockage des fichiers à télécharger
    download_dir = os.path.join(app.root_path, 'static', 'downloads')
    return send_from_directory(download_dir, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
