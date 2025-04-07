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
        # Récupération des informations de l'étudiant correspondant à l'email
        etudiant = df[df["Email"] == email]
        nom = etudiant["Name"].values[0]
        groupe = etudiant["GROUP"].values[0]
        noteDS = etudiant["DS"].values[0]
        #noteTP = etudiant["TP"].values[0]
        # Création d'un dictionnaire contenant les informations de l'étudiant
        etudiant_info = {
                        "Nom": nom,
                        "Groupe": groupe,
                        "DS": noteDS,
                    }
        res = pd.DataFrame.from_dict(etudiant_info, orient='index', columns=['Résultats'])
        res['Résultats'] = res['Résultats'].astype(str)
        # Affichage des informations de l'étudiant dans un tableau
        st.subheader("Résultats de l'étudiant")
        a,b,c = st.columns(3)
        with b:
            st.write(res, unsafe_allow_html=True)
        if noteDS==0:
            st.warning("0 : abscent au DS si vous ne régler pas votre situation la note finale au ds sera définitivement 0")
        # Calculer les statistiques des notes pour le pie chart
    else:
        st.error("Email non trouvé")
# Bloc avec la possibilité de cacher/afficher les statistiques des groupes
with st.expander("Afficher/Masquer les statistiques des groupes"):
    # Champ de sélection pour choisir un groupe
    groupes = df["GROUP"].unique()
    groupes.sort()
    groupe_selectionne = st.selectbox("Choisissez un groupe", options=groupes)

    if groupe_selectionne:
        # Filtrer les données pour le groupe sélectionné
        df_groupe = df[df["GROUP"] == groupe_selectionne]
        # Statistiques du groupe
        moyenne = df_groupe["DS"].mean()
        variance = df_groupe["DS"].var()
        ecart_type = df_groupe["DS"].std()

        # Affichage des statistiques
        col1, col2 = st.columns(2)
        with col2:
            # Boxplot
            fig_box = px.box(df_groupe, y="DS", points="all", title="Boxplot des notes DS")
            st.plotly_chart(fig_box, use_container_width=True)
            st.write(f"- **Moyenne** : {moyenne:.2f}")
            st.write(f"- **Variance** : {variance:.2f}")
            st.write(f"- **Écart-type** : {ecart_type:.2f}")

        # Graphiques
        with col1:
            fig_pie = px.pie(df_groupe, names="Catégorie de notes DS", title="Répartition des catégories")
            st.plotly_chart(fig_pie, use_container_width=True)
            fig_hist = px.histogram(
            df_groupe,
            x="DS",
            nbins=10,  # Vous pouvez ajuster le nombre de bins
            title="Histogramme des notes DS",
            labels={"DS": "Notes DS"},
            color_discrete_sequence=["#636EFA"],
            )
            fig_hist.update_layout(bargap=0.2)  # Ajuste l'espace entre les barres
            st.plotly_chart(fig_hist, use_container_width=True)
