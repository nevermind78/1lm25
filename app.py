import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Notes DS Python 1LM", page_icon=":bar_chart:")

# 1. Fonction de catégorisation des notes
def categorize_notes(note):
    if note < 10: return "Insuffisant (<10)"
    elif note < 12: return "Passable (10-12)"
    elif note < 14: return "Assez Bien(12-14)"
    elif note < 16: return "Bien(14-16)"
    return "Très bien (>16)"

# 2. Fonction pour calculer les statistiques du groupe (avec cache)
@st.cache_data
def get_group_stats(df_groupe):
    return {
        "moyenne": df_groupe["DS"].mean(),
        "variance": df_groupe["DS"].var(),
        "ecart_type": df_groupe["DS"].std()
    }

# 3. Chargement optimisé des données avec cache
@st.cache_data  
def load_data():
    df = pd.read_csv(st.secrets['csv_file_path'], 
                    delimiter=",", 
                    converters={"Email": lambda x: x.strip()})
    df["DS"] = pd.to_numeric(df["DS"], errors='coerce').fillna(0)
    df["Catégorie de notes DS"] = df["DS"].apply(categorize_notes)
    return df

# Chargement des données
df = load_data()

# Interface utilisateur
st.title("NOTES DS et TP PYTHON")
st.header("1LM A.U 2024-2025")

# Recherche étudiante
email = st.text_input("Saisissez votre email")
if email:
    if email in df["Email"].values:
        etudiant = df.loc[df["Email"] == email].iloc[0]
        
        st.subheader("Résultats de l'étudiant")
        cols = st.columns(3)
        with cols[1]:
            st.metric("Nom", etudiant["Name"])
            st.metric("Groupe", etudiant["GROUP"])
            st.metric("Note DS", f"{etudiant['DS']:.2f}")

# Statistiques des groupes
with st.expander("Afficher/Masquer les statistiques des groupes"):
    groupe_selectionne = st.selectbox(
        "Choisissez un groupe",
        options=sorted(df["GROUP"].unique())
    )
    
    if groupe_selectionne:
        df_groupe = df[df["GROUP"] == groupe_selectionne]
        stats = get_group_stats(df_groupe)  # Appel de la fonction maintenant définie
        
        col1, col2 = st.columns(2)
        with col1:
            fig_pie = px.pie(df_groupe, names="Catégorie de notes DS", title="Répartition des notes")
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col2:
            fig_box = px.box(df_groupe, y="DS", title="Distribution des notes")
            st.plotly_chart(fig_box, use_container_width=True)
            
            st.metric("Moyenne du groupe", f"{stats['moyenne']:.2f}")
            st.metric("Écart-type", f"{stats['ecart_type']:.2f}")