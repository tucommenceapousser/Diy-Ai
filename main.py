from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Configurez votre clé API OpenAI
openai.api_key = ""

@app.route("/")
def home():
    return render_template("diy.html")

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
            # Si c'est une demande d'idée, ajoutez plus de contexte pour guider la réponse
            if "orgonite" in prompt.lower():
                question = f"Donne-moi des idées de projets DIY pour fabriquer des objets en orgonite. L'objectif est d'explorer les propriétés énergétiques de l'orgonite, en utilisant des matériaux comme la résine, la poudre de métal, les cristaux, et d'autres éléments associés à l'orgonite. Les projets doivent être éducatifs et expérimentaux, permettant d'expérimenter avec la géométrie sacrée et le magnétisme."
            elif "moteur stirling" in prompt.lower():
                question = f"Propose-moi des idées de projets DIY pour construire un moteur Stirling. L'objectif est de comprendre le fonctionnement du moteur Stirling, en utilisant des matériaux simples et des techniques de mécanique de base."
            else:
                # Si le prompt ne concerne pas un projet spécifique, demandez des idées générales
                question = f"Donne-moi des idées de projets DIY basés sur ce thème ou matériel : {prompt}. Les projets doivent être intéressants, expérimentaux, et éducatifs."

        elif type_request == "method":
            # Si c'est une demande de méthode, ajoutez le contexte approprié
            if "orgonite" in prompt.lower():
                question = f"Donne-moi des étapes détaillées pour fabriquer de l'orgonite. Inclut les matériaux nécessaires, comme la résine, les cristaux et la poudre de métal. Précise les étapes pour assembler l'orgonite et explique comment explorer les effets énergétiques du produit final."
            elif "moteur stirling" in prompt.lower():
                question = f"Donne-moi des étapes détaillées pour construire un moteur Stirling. Inclut la liste des matériaux nécessaires, les étapes de fabrication, et les conseils pour comprendre son fonctionnement."
            else:
                # Demande une méthode générale
                question = f"Donne-moi des étapes détaillées pour réaliser ce projet DIY : {prompt}."

        else:
            return jsonify({"error": "Type de requête invalide."}), 400

        # Requête à l'API OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": question}],
            max_tokens=1500
        )

        # Retournez la réponse à l'utilisateur
        return jsonify({"response": response["choices"][0]["message"]["content"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
