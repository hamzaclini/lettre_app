import streamlit as st
import os
import pymongo
import hmac

# Fonction pour appliquer des styles CSS personnalisés à partir d'un fichier
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Application des styles CSS depuis le fichier 'style.css'
local_css("style.css")

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

@st.cache_resource
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])

client = init_connection()

def write_data(new_data):
    # Write new data to the database
    db = client.alphapv
    db.letters.insert_one(new_data)

# Chargement du logo de votre clinique
logo_path = os.path.join('images', 'logo.jpg')
st.image(logo_path, width=180)  # Ajustez la largeur selon vos besoins

# Titre de l'application
st.title("Lettre d'évaluation psychologique pour un enfant")

# Formulaire de soumission de la lettre
with st.form("letter_form"):
    # Entrée de texte pour le nom complet de la personne évaluatrice avec un espace réservé
    nom_eval = st.text_input("Nom de la personne évaluatrice:", placeholder="Écrivez votre nom")
    # Entrée pour le nom de l'enfant
    nom_enfant = st.text_input("Nom de l'enfant:", placeholder="Écrivez le nom de l'enfant")
    prenom_eval = st.text_input("Prénom de l'enfant:", placeholder="Écrivez le prénom de l'enfant")
    # Zone de texte pour écrire la lettre
    lettre = st.text_area("Écrivez votre lettre ici:", height=300)  # Hauteur de la zone de texte
    
    # Bouton pour soumettre le formulaire
    soumis = st.form_submit_button("Envoyer la lettre")
    
    if soumis:
        user_data = {"lastName": nom_eval,
                     'ch_lastName': nom_enfant,
                     'ch_firstName': prenom_eval,}
        letter = lettre

        document = {
        #"_id": ObjectId(),  # Generate a new ObjectId
        "user": user_data,
        "answers": letter
        #"__v": 0
        }
        write_data(document)
        # Message de confirmation après soumission
        st.success("Lettre envoyée avec succès ! Voici un aperçu de votre lettre :")
        # Affichage du contenu de la lettre
        #st.write("De:", f"{nom_eval} {prenom_eval}")  # Affichage du nom et prénom de l'évaluateur
        #st.write("Concernant:", nom_enfant)  # Affichage du nom de l'enfant
        #st.write("Lettre:")
        #st.write(lettre)  # Affichage de la lettre
