import streamlit as st
import base64
import os
from mistralai import Mistral
from dotenv import load_dotenv
import tempfile
from PIL import Image
import io

# Configuration de la page
st.set_page_config(
    page_title="🔥 Roast My Friends",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Chargement des variables d'environnement
load_dotenv()

def encode_image_from_bytes(image_bytes):
    """Encode l'image en base64 à partir de bytes."""
    try:
        return base64.b64encode(image_bytes).decode('utf-8')
    except Exception as e:
        st.error(f"Erreur lors de l'encodage de l'image: {e}")
        return None

def get_roast_from_mistral(base64_image, api_key, roast_type):
    """Génère un roast en utilisant l'API Mistral."""
    try:
        # Modèle utilisé
        model = "pixtral-12b-2409"
        
        # Initialisation du client Mistral
        client = Mistral(api_key=api_key)
        
        # Prompts selon le type de roast
        prompts = {
            "cheveux": "Ici tu as l'image d'un ami, fais une blague sur sa coupe de cheveux. Essaie d'être piquant et drôle.",
            "style": "Ici tu as l'image d'un ami, fais une blague sur son style vestimentaire. Sois créatif et humoristique.",
            "expression": "Ici tu as l'image d'un ami, fais une blague sur son expression faciale. Sois drôle mais pas méchant.",
            "général": "Ici tu as l'image d'un ami, fais un roast général mais amical. Sois drôle et créatif.",
            "compliment": "Ici tu as l'image d'un ami, fais-lui un compliment original et drôle. Sois positif mais avec de l'humour."
        }
        
        # Messages pour l'API
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompts[roast_type]
                    },
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{base64_image}" 
                    }
                ]
            }
        ]
        
        # Appel à l'API
        chat_response = client.chat.complete(
            model=model,
            messages=messages
        )
        
        return chat_response.choices[0].message.content
        
    except Exception as e:
        st.error(f"Erreur lors de l'appel à l'API Mistral: {e}")
        return None

def main():
    # Titre principal avec style
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1 style="color: #FF6B35; font-size: 3em;">🔥 Roast My Friends</h1>
        <p style="font-size: 1.2em; color: #666;">L'IA qui va chambrer tes amis avec style !</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Configuration de l'API key
    st.sidebar.title("⚙️ Configuration")
    
    # Vérification de l'API key
    api_key = os.environ.get("MISTRAL_KEY")
    if not api_key:
        api_key = st.sidebar.text_input(
            "Clé API Mistral", 
            type="password",
            help="Entrez votre clé API Mistral"
        )
        
    if not api_key:
        st.warning("⚠️ Veuillez configurer votre clé API Mistral dans les variables d'environnement ou dans la barre latérale.")
        st.info("💡 Pour obtenir une clé API, rendez-vous sur [console.mistral.ai](https://console.mistral.ai)")
        return
    
    # Sélection du type de roast
    st.sidebar.subheader("🎯 Type de roast")
    roast_type = st.sidebar.selectbox(
        "Choisissez votre style",
        ["cheveux", "style", "expression", "général", "compliment"],
        index=0,
        help="Sélectionnez le type de roast que vous voulez"
    )
    
    # Zone d'upload
    st.markdown("### 📸 Upload de l'image")
    uploaded_file = st.file_uploader(
        "Choisissez une photo de votre ami(e)",
        type=['png', 'jpg', 'jpeg'],
        help="Formats acceptés: PNG, JPG, JPEG"
    )
    
    if uploaded_file is not None:
        # Affichage de l'image
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Lecture et affichage de l'image
            image = Image.open(uploaded_file)
            st.image(image, caption="Image uploadée", use_container_width =True)
            
            # Bouton pour générer le roast
            if st.button("🔥 Générer le roast !", use_container_width=True, type="primary"):
                with st.spinner("🤖 L'IA analyse l'image et prépare son roast..."):
                    # Conversion de l'image en bytes
                    img_bytes = uploaded_file.getvalue()
                    
                    # Encodage en base64
                    base64_image = encode_image_from_bytes(img_bytes)
                    
                    if base64_image:
                        # Génération du roast
                        roast_result = get_roast_from_mistral(base64_image, api_key, roast_type)
                        
                        if roast_result:
                            # Affichage du résultat avec style
                            st.markdown("---")
                            st.markdown("### 🎭 Résultat du roast")
                            
                            # Style du résultat selon le type
                            if roast_type == "compliment":
                                st.success(f"💝 **Compliment:** {roast_result}")
                            else:
                                st.info(f"🔥 **Roast:** {roast_result}")
                            
                            # Boutons d'action
                            col_copy, col_new = st.columns(2)
                            
                            with col_copy:
                                if st.button("📋 Copier le texte", use_container_width=True):
                                    st.write("Texte copié dans le presse-papier !")
                                    # Note: Le vrai copy to clipboard nécessite du JavaScript
                            
                            with col_new:
                                if st.button("🔄 Nouveau roast", use_container_width=True):
                                    st.rerun()
                        else:
                            st.error("Impossible de générer le roast. Vérifiez votre connexion et votre clé API.")
                    else:
                        st.error("Erreur lors du traitement de l'image.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>🤖 Alimenté par Mistral AI • 🔥 Fait avec amour et humour</p>
        <p><small>⚠️ Utilisez avec modération et bienveillance !</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()