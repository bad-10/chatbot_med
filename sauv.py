import requests
from bs4 import BeautifulSoup

def extraire_informations_maladie(url, sections_ciblees=["Overview", "Symptoms", "When to see a doctor", "Causes", "Risk factors", "Complications"]):
    """
    Extrait les informations spécifiques d'une maladie à partir d'une page de Mayo Clinic.

    Args:
        url : L'URL de la page de la maladie.
        sections_ciblees : Une liste des sections à extraire.

    Returns:
        Un dictionnaire contenant les informations extraites,
        organisées par titre de section.
    """

    try:
        reponse = requests.get(url)
        reponse.raise_for_status()
        soup = BeautifulSoup(reponse.content, 'html.parser')

        sections = soup.find_all(['h2', 'h3'])
        informations_maladie = {}
        for section in sections:
            titre_section = section.text.strip()
            if titre_section in sections_ciblees:
                contenu_section = []
                element = section.find_next_sibling()
                while element and element.name not in ['h2', 'h3']:
                    if element.name in ['p', 'ul', 'ol']:
                        contenu_section.append(element.get_text(strip=True))
                    elif element.name == 'img':
                        legende = element.get('alt')
                        if legende:
                            contenu_section.append(f"Image : {legende}")
                    element = element.find_next_sibling()
                informations_maladie[titre_section] = '\n'.join(contenu_section)

        return informations_maladie

    except (requests.exceptions.RequestException, ConnectionError) as erreur:
        print(f"Erreur lors du scraping : {erreur}")
        return {}

# Remplacez par l'URL de la page de la maladie que vous voulez scraper
url = "https://www.mayoclinic.org/diseases-conditions/acanthosis-nigricans/symptoms-causes/syc-20368983"

# Liste des sections à extraire
sections_ciblees = ["Overview", "Symptoms", "When to see a doctor", "Causes", "Risk factors", "Complications"]

# Extrait les informations
informations_maladie = extraire_informations_maladie(url, sections_ciblees)

# Affiche les informations extraites
for titre, contenu in informations_maladie.items():
    print(f"**{titre}**\n{contenu}\n")