import streamlit as st
import pandas as pd
import numpy as np
import json
import joblib
import os
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import IncrementalPCA
from sklearn.svm import SVC
import sys
import traceback

# Set page configuration
st.set_page_config(
    page_title="Système de Détection d'Attaques Réseau",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for a cleaner look
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        margin-bottom: 1rem;
    }
    .subheader {
        font-size: 1.5rem;
        color: #1E3A8A;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid #E5E7EB;
        padding-bottom: 0.5rem;
    }
    .success-box {
        background-color: #ECFDF5;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 0.5rem solid #10B981;
    }
    .warning-box {
        background-color: #FEF2F2;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 0.5rem solid #EF4444;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">Système de Détection d\'Attaques Réseau</h1>', unsafe_allow_html=True)
st.write("Téléchargez un fichier de données de trafic réseau pour analyser les attaques potentielles.")

# Function to load the model files
@st.cache_resource
def load_models():
    try:
        # Paths to model files
        features_path = os.path.join('..', 'results', 'features_list.json')
        scaler_path = os.path.join('..', 'models', 'scaler.joblib')
        ipca_path = os.path.join('..', 'models', 'ipca_model.joblib')
        svm_path = os.path.join('..', 'models', 'svm_rbf_model.joblib')
        
        # Load feature list
        with open(features_path, 'r') as file:
            features_list = json.load(file)
        
        # Load models
        scaler = joblib.load(scaler_path)
        ipca_model = joblib.load(ipca_path)
        svm_model = joblib.load(svm_path)
        
        return {
            'features_list': features_list,
            'scaler': scaler,
            'ipca_model': ipca_model,
            'svm_model': svm_model
        }
    except Exception as e:
        st.error(f"Erreur lors du chargement des modèles: {str(e)}")
        st.error(traceback.format_exc())
        return None

# Function to read uploaded file
def read_file(uploaded_file):
    try:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_extension in ['xlsx', 'xls']:
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Format de fichier non supporté. Veuillez télécharger un fichier CSV ou Excel.")
            return None
        
        # Renommer les colonnes en supprimant les espaces avant et après le nom des colonnes
        col_names = {col: col.strip() for col in df.columns}
        df.rename(columns=col_names, inplace=True)
            
        return df
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier: {str(e)}")
        return None

# Function to process data through the ML pipeline
def process_data(df, models):
    try:
        # Extract relevant features
        features_list = models['features_list']
        
        # Check if all required features are in the dataframe
        missing_features = [feat for feat in features_list if feat not in df.columns]
        if missing_features:
            st.error(f"Colonnes manquantes dans le fichier téléchargé: {', '.join(missing_features)}")
            return None
            
        # Extract features from dataframe
        X = df[features_list].copy()
        
        # Handle missing values (fill with mean)
        X = X.fillna(X.mean())
        
        # Standardize features
        X_scaled = models['scaler'].transform(X)
        
        # Apply IPCA transformation
        X_ipca = models['ipca_model'].transform(X_scaled)
        
        # Get predictions
        y_pred = models['svm_model'].predict(X_ipca)
        
        # Get prediction probabilities
        y_prob = models['svm_model'].predict_proba(X_ipca)[:, 1]  # Probability for class 1
        
        # Create results dataframe
        results_df = pd.DataFrame({
            'Index_Original': df.index,
            'Prediction': y_pred,
            'Probabilite_Attaque': y_prob
        })
        
        # Map predictions to labels
        results_df['Statut'] = results_df['Prediction'].map({0: 'Normal', 1: 'Attaque'})
        
        return results_df
    except Exception as e:
        st.error(f"Erreur lors du traitement des données: {str(e)}")
        st.error(traceback.format_exc())
        return None

# Sidebar
with st.sidebar:
    st.markdown("## Télécharger des Données")
    st.write("Téléchargez votre fichier de données de trafic réseau (CSV ou Excel)")
    uploaded_file = st.file_uploader("Choisir un fichier", type=['csv', 'xlsx', 'xls'])
    
    if uploaded_file is not None:
        st.success(f"Fichier '{uploaded_file.name}' téléchargé avec succès!")
        
        # Display file metadata
        file_details = {
            "Nom du fichier": uploaded_file.name,
            "Taille du fichier": f"{uploaded_file.size / 1024:.2f} KB"
        }
        st.write(file_details)

# Main content area
if uploaded_file is not None:
    # Load models
    models = load_models()
    
    if models is not None:
        # Read the file
        df = read_file(uploaded_file)
        
        if df is not None:
            # Display data preview
            st.markdown('<h2 class="subheader">Aperçu des Données</h2>', unsafe_allow_html=True)
            st.write(f"Nombre total de lignes: {df.shape[0]}, Nombre total de colonnes: {df.shape[1]}")
            st.dataframe(df.head(5), use_container_width=True)
            
            # Process data
            st.markdown('<h2 class="subheader">Traitement des Données</h2>', unsafe_allow_html=True)
            with st.spinner("Traitement des données en cours..."):
                results_df = process_data(df, models)
            
            if results_df is not None:
                st.success("Données traitées avec succès!")
                
                # Display results
                st.markdown('<h2 class="subheader">Résultats de Détection</h2>', unsafe_allow_html=True)
                
                # Calculate statistics
                attack_count = results_df['Prediction'].sum()
                total_count = len(results_df)
                attack_percentage = (attack_count / total_count) * 100
                
                # Display statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total des Enregistrements", total_count)
                with col2:
                    st.metric("Attaques Détectées", int(attack_count))
                with col3:
                    st.metric("Pourcentage d'Attaques", f"{attack_percentage:.2f}%")
                
                # Add filter checkbox
                show_only_attacks = st.checkbox("Afficher uniquement les attaques")
                
                # Filter results if needed
                if show_only_attacks:
                    filtered_results = results_df[results_df['Prediction'] == 1]
                    display_df = filtered_results
                    st.write(f"Affichage de {len(filtered_results)} enregistrements d'attaques.")
                else:
                    display_df = results_df
                
                # Format the dataframe for display
                display_df = display_df.copy()
                display_df['Probabilite_Attaque'] = display_df['Probabilite_Attaque'].map("{:.2%}".format)
                
                # Create a styled dataframe
                st.dataframe(
                    display_df,
                    column_config={
                        "Index_Original": st.column_config.NumberColumn("Index de Ligne"),
                        "Prediction": st.column_config.NumberColumn("Code Prédiction"),
                        "Statut": st.column_config.TextColumn("Statut"),
                        "Probabilite_Attaque": st.column_config.TextColumn("Probabilité d'Attaque")
                    },
                    hide_index=True,
                    use_container_width=True
                )
                
                # Download button for results
                csv_results = display_df.to_csv(index=False)
                st.download_button(
                    label="Télécharger les Résultats en CSV",
                    data=csv_results,
                    file_name="resultats_detection_attaques.csv",
                    mime="text/csv"
                )
    else:
        st.error("Échec du chargement des fichiers modèles requis. Veuillez vérifier les chemins des fichiers et réessayer.")
else:
    # Show instructions when no file is uploaded
    st.info("Veuillez télécharger un fichier CSV ou Excel en utilisant la barre latérale pour commencer l'analyse.")
    
    st.markdown('<h2 class="subheader">Comment Utiliser Cette Application</h2>', unsafe_allow_html=True)
    st.markdown("""
    1. **Téléchargez votre fichier de données** (format .csv ou .xlsx) en utilisant l'outil de téléchargement dans la barre latérale
    2. L'application chargera automatiquement les modèles nécessaires
    3. Vos données seront analysées pour détecter les attaques réseau potentielles
    4. Consultez le tableau des résultats montrant les attaques prédites et les probabilités
    5. Utilisez l'option de filtre pour vous concentrer sur les enregistrements d'attaques détectées
    6. Téléchargez les résultats pour une analyse plus approfondie
    
    Cette application implémente un pipeline d'apprentissage automatique utilisant:
    - Standardisation des caractéristiques
    - PCA incrémental pour la réduction de dimensionnalité
    - Classifieur SVM (Support Vector Machine) avec noyau RBF
    """)
