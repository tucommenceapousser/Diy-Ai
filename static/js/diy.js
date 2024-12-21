document.getElementById("diyForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const prompt = document.getElementById("prompt").value.trim();
    const type_request = document.getElementById("type_request").value;
    const resultDiv = document.getElementById("result");

    // Validation côté client
    if (!prompt) {
        resultDiv.style.display = "block";
        resultDiv.innerHTML = "<pre>Veuillez entrer un thème ou un projet précis.</pre>";
        return;
    }

    // Envoyer la requête au serveur
    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ prompt, type_request }),
        });

        const data = await response.json();

        // Vérification des erreurs
        if (data.error) {
            resultDiv.style.display = "block";
            resultDiv.innerHTML = `<pre>Erreur : ${data.error}</pre>`;
            return;
        }

        // Traitement et formatage des réponses
        const formattedResponse = formatResponse(data.response);
        resultDiv.style.display = "block";
        resultDiv.innerHTML = formattedResponse;

    } catch (err) {
        resultDiv.style.display = "block";
        resultDiv.innerHTML = `<pre>Erreur de connexion : ${err.message}</pre>`;
    }
});

/**
 * Formater la réponse OpenAI pour une meilleure lisibilité
 * @param {string} response - La réponse brute d'OpenAI
 * @returns {string} - La réponse formatée avec du HTML
 */
function formatResponse(response) {
    // Échapper les caractères spéciaux pour éviter l'injection
    const escapedResponse = response
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");

    // Ajouter des retours à la ligne
    const formatted = escapedResponse
        .replace(/\n/g, "<br>") // Convertir les sauts de ligne en HTML
        .replace(/- (.+)/g, "<li>$1</li>") // Convertir les listes en puces
        .replace(/(\*\*(.+?)\*\*)/g, "<strong>$2</strong>") // Mettre en gras
        .replace(/__(.+?)__/g, "<em>$1</em>"); // Mettre en italique

    // Ajouter une structure HTML si nécessaire
    return `<div class="formatted-response">${formatted}</div>`;
}
