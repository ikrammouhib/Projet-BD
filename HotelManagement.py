import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date
import os

# Configuration de la page
st.set_page_config(
    page_title="Gestion Hôtelière Pro",
    page_icon="🌿",
    layout="wide"
)

# Style CSS personnalisé
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    /* Base Styles */
    .stApp {
        background-color: #E8F5E9 !important;
    }
    .stApp body {
        background-color: #E8F5E9 !important;
        font-family: 'Roboto', sans-serif;
        color: #2E7D32;
    }

    /* Title */
    .main-title {
        text-align: center;
        color: #2E7D32;
        font-size: 2.8rem;
        margin-bottom: 2rem;
        font-weight: 600;
    }

    /* Sidebar Styling */
    .css-1v3fvcr {
        background-color: #FFFFFF !important;
        padding-top: 2rem;
        width: 250px !important;
    }
    .css-1v3fvcr .stRadio > label {
        color: #FFFFFF !important;
        font-size: 1.2rem;
        font-weight: 500;
        padding: 0.8rem 1rem;
        margin: 0.2rem 0;
        background-color: #81C784;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    .css-1v3fvcr .stRadio > label:hover {
        background-color: #388E3C;
    }
    .css-1v3fvcr .stRadio > div[role="radiogroup"] > div > div {
        background-color: #FFFFFF !important;
        border: 2px solid #2E7D32 !important;
    }

    /* Main Content */
    .main-content {
        margin-left: 260px;
        padding: 1rem 2rem;
    }

    /* Panels */
    .panel {
        background: #FFFFFF;
        padding: 1.8rem;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        margin: 1.2rem 0;
        border-left: 5px solid #4CAF50;
    }

    /* Stat Cards */
    .stat-card {
        background: linear-gradient(135deg, #81C784 0%, #4CAF50 100%);
        color: #1C2541;
        padding: 1.2rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.7rem;
        font-weight: 500;
    }

    /* Notifications */
    .notification-success {
        background: #E8F5E9;
        border: 1px solid #81C784;
        color: #2E7D32;
        padding: 1rem;
        border-radius: 8px;
        margin: 1.2rem 0;
    }

    /* Buttons */
    button[kind="primary"] {
        background-color: #4CAF50 !important;
        color: #FFFFFF !important;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        cursor: pointer;
        transition: background-color 0.3s;
        border-radius: 5px;
    }
    button[kind="primary"]:hover {
        background-color: #388E3C !important;
    }

    /* DataFrame */
    div[data-testid="stDataFrame"] {
        border: 1px solid #4CAF50;
        border-radius: 5px;
    }

    /* Text Input */
    div[data-testid="stTextInput"] input {
        border: 1px solid #4CAF50;
        background-color: #FFFFFF;
        padding: 0.4rem;
        color: #2E7D32;
        border-radius: 5px;
    }

    /* Date Input */
    div[data-testid="stDateInput"] input {
        border: 1px solid #4CAF50;
        background-color: #FFFFFF;
        padding: 0.4rem;
        color: #2E7D32;
        border-radius: 5px;
    }

    /* Selectbox */
    div[data-testid="stSelectbox"] {
        border: 1px solid #4CAF50;
        border-radius: 5px;
    }
    div[data-testid="stSelectbox"] div {
        color: #2E7D32;
    }
</style>
""", unsafe_allow_html=True)

# Fonction d'initialisation de la base de données
def setup_database():
    """Configure la base de données SQLite avec les tables et données initiales"""
    db_conn = sqlite3.connect('HotelManagement.db')
    db_cursor = db_conn.cursor()
    
    # Création des tables
    db_cursor.executescript('''
    -- Table Hôtel
    CREATE TABLE IF NOT EXISTS Hotel (
        id_hotel INTEGER PRIMARY KEY,
        ville TEXT NOT NULL,
        pays TEXT NOT NULL,
        code_postal TEXT
    );

    -- Table Client
    CREATE TABLE IF NOT EXISTS Client (
        id_client INTEGER PRIMARY KEY,
        adresse TEXT,
        ville TEXT,
        code_postal TEXT,
        email TEXT,
        telephone TEXT,
        nom_complet TEXT NOT NULL
    );

    -- Table Prestation
    CREATE TABLE IF NOT EXISTS Prestation (
        id_prestation INTEGER PRIMARY KEY,
        prix REAL,
        nom_prestation TEXT NOT NULL
    );

    -- Table TypeChambre
    CREATE TABLE IF NOT EXISTS TypeChambre (
        id_type INTEGER PRIMARY KEY,
        type_nom TEXT NOT NULL,
        prix_nuit REAL NOT NULL
    );

    -- Table Chambre
    CREATE TABLE IF NOT EXISTS Chambre (
        id_chambre INTEGER PRIMARY KEY,
        numero_chambre INTEGER NOT NULL,
        etage INTEGER,
        balcon BOOLEAN DEFAULT 0,
        id_hotel INTEGER,
        id_type INTEGER,
        FOREIGN KEY (id_hotel) REFERENCES Hotel(id_hotel),
        FOREIGN KEY (id_type) REFERENCES TypeChambre(id_type)
    );

    -- Table Réservation
    CREATE TABLE IF NOT EXISTS Reservation (
        id_reservation INTEGER PRIMARY KEY,
        date_arrivee DATE NOT NULL,
        date_depart DATE NOT NULL,
        id_client INTEGER,
        FOREIGN KEY (id_client) REFERENCES Client(id_client)
    );

    -- Table Evaluation
    CREATE TABLE IF NOT EXISTS Evaluation (
        id_evaluation INTEGER PRIMARY KEY,
        date_evaluation DATE,
        note INTEGER CHECK (note >= 1 AND note <= 5),
        commentaire TEXT,
        id_reservation INTEGER,
        FOREIGN KEY (id_reservation) REFERENCES Reservation(id_reservation)
    );

    -- Table de liaison Réservation_Chambre
    CREATE TABLE IF NOT EXISTS ReservationChambre (
        id_reservation INTEGER,
        id_chambre INTEGER,
        PRIMARY KEY (id_reservation, id_chambre),
        FOREIGN KEY (id_reservation) REFERENCES Reservation(id_reservation),
        FOREIGN KEY (id_chambre) REFERENCES Chambre(id_chambre)
    );

    -- Table de liaison Client_Prestation
    CREATE TABLE IF NOT EXISTS ClientPrestation (
        id_client INTEGER,
        id_prestation INTEGER,
        PRIMARY KEY (id_client, id_prestation),
        FOREIGN KEY (id_client) REFERENCES Client(id_client),
        FOREIGN KEY (id_prestation) REFERENCES Prestation(id_prestation)
    );
    ''')
    
    # Vérifier si des données existent déjà
    db_cursor.execute("SELECT COUNT(*) FROM Hotel")
    if db_cursor.fetchone()[0] == 0:
        # Insertion des données initiales
        db_cursor.executescript('''
        -- Données Hôtel
        INSERT INTO Hotel VALUES 
        (1, 'Paris', 'France', '75001'),
        (2, 'Lyon', 'France', '69002');

        -- Données Client
        INSERT INTO Client VALUES 
        (1, '12 Rue de Paris', 'Paris', '75001', 'jean.dupont@email.fr', '0612345678', 'Jean Dupont'),
        (2, '5 Avenue Victor Hugo', 'Lyon', '69002', 'marie.leroy@email.fr', '0623456789', 'Marie Leroy'),
        (3, '8 Boulevard Saint-Michel', 'Marseille', '13005', 'paul.moreau@email.fr', '0634567890', 'Paul Moreau'),
        (4, '27 Rue Nationale', 'Lille', '59800', 'lucie.martin@email.fr', '0645678901', 'Lucie Martin'),
        (5, '3 Rue des Fleurs', 'Nice', '06000', 'emma.giraud@email.fr', '0656789012', 'Emma Giraud');

        -- Données Prestation
        INSERT INTO Prestation VALUES 
        (1, 15.00, 'Petit-déjeuner'),
        (2, 30.00, 'Navette aéroport'),
        (3, 0.00, 'Wi-Fi gratuit'),
        (4, 50.00, 'Spa et bien-être'),
        (5, 20.00, 'Parking sécurisé');

        -- Données TypeChambre
        INSERT INTO TypeChambre VALUES 
        (1, 'Chambre Simple', 80.00),
        (2, 'Chambre Double', 120.00);

        -- Données Chambre
        INSERT INTO Chambre VALUES 
        (1, 201, 2, 0, 1, 1),
        (2, 502, 5, 1, 1, 2),
        (3, 305, 3, 0, 2, 1),
        (4, 410, 4, 0, 2, 2),
        (5, 104, 1, 1, 2, 2),
        (6, 202, 2, 0, 1, 1),
        (7, 307, 3, 1, 1, 2),
        (8, 101, 1, 0, 1, 1);

        -- Données Réservation
        INSERT INTO Reservation VALUES 
        (1, '2025-06-15', '2025-06-18', 1),
        (2, '2025-07-01', '2025-07-05', 2),
        (3, '2025-08-10', '2025-08-14', 3),
        (4, '2025-09-05', '2025-09-07', 4),
        (5, '2025-09-20', '2025-09-25', 5),
        (7, '2025-11-12', '2025-11-14', 2),
        (9, '2026-01-15', '2026-01-18', 4),
        (10, '2026-02-01', '2026-02-05', 2);

        -- Données Réservation_Chambre
        INSERT INTO ReservationChambre VALUES 
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
        (7, 7), (9, 4), (10, 2);

        -- Données Evaluation
        INSERT INTO Evaluation VALUES 
        (1, '2025-06-15', 5, 'Excellent séjour, personnel très accueillant.', 1),
        (2, '2025-07-01', 4, 'Chambre propre, bon rapport qualité/prix.', 2),
        (3, '2025-08-10', 3, 'Séjour correct mais bruyant la nuit.', 3),
        (4, '2025-09-05', 5, 'Service impeccable, je recommande.', 4),
        (5, '2025-09-20', 4, 'Très bon petit-déjeuner, hôtel bien situé.', 5);
        ''')
    
    db_conn.commit()
    db_conn.close()

# Fonction de connexion à la base de données
def get_db_connection():
    return sqlite3.connect('HotelManagement.db')

# Opérations sur la base de données
def fetch_reservations():
    conn = get_db_connection()
    query = '''
    SELECT 
        r.id_reservation AS "ID",
        c.nom_complet AS "Client",
        h.ville AS "Lieu",
        r.date_arrivee AS "Arrivée",
        r.date_depart AS "Départ",
        ch.numero_chambre AS "Chambre",
        tc.type_nom AS "Catégorie"
    FROM Reservation r
    JOIN Client c ON r.id_client = c.id_client
    JOIN ReservationChambre rc ON r.id_reservation = rc.id_reservation
    JOIN Chambre ch ON rc.id_chambre = ch.id_chambre
    JOIN Hotel h ON ch.id_hotel = h.id_hotel
    JOIN TypeChambre tc ON ch.id_type = tc.id_type
    ORDER BY r.date_arrivee DESC
    '''
    result_df = pd.read_sql_query(query, conn)
    conn.close()
    return result_df

def fetch_clients():
    conn = get_db_connection()
    query = 'SELECT id_client AS "ID", nom_complet AS "Nom", email AS "Email", telephone AS "Téléphone", ville AS "Ville" FROM Client ORDER BY nom_complet'
    result_df = pd.read_sql_query(query, conn)
    conn.close()
    return result_df

def add_new_client(nom_complet, email, telephone, ville, adresse="", code_postal=""):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id_client) FROM Client")
    max_id = cursor.fetchone()[0] or 0
    new_id = max_id + 1
    
    cursor.execute('''
    INSERT INTO Client (id_client, nom_complet, adresse, ville, code_postal, email, telephone)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (new_id, nom_complet, adresse, ville, code_postal, email, telephone))
    
    conn.commit()
    conn.close()
    return new_id

def get_vacant_chambres(date_arrivee, date_depart):
    conn = get_db_connection()
    query = '''
    SELECT 
        ch.id_chambre,
        ch.numero_chambre AS "Chambre",
        h.ville AS "Hôtel",
        tc.type_nom AS "Catégorie",
        tc.prix_nuit AS "Tarif",
        CASE WHEN ch.balcon = 1 THEN 'Oui' ELSE 'Non' END AS "Balcon"
    FROM Chambre ch
    JOIN Hotel h ON ch.id_hotel = h.id_hotel
    JOIN TypeChambre tc ON ch.id_type = tc.id_type
    WHERE ch.id_chambre NOT IN (
        SELECT DISTINCT rc.id_chambre
        FROM ReservationChambre rc
        JOIN Reservation r ON rc.id_reservation = r.id_reservation
        WHERE (r.date_arrivee <= ? AND r.date_depart >= ?)
    )
    ORDER BY h.ville, ch.numero_chambre
    '''
    result_df = pd.read_sql_query(query, conn, params=(date_depart, date_arrivee))
    conn.close()
    return result_df

def create_reservation(date_arrivee, date_depart, id_client, id_chambre):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT MAX(id_reservation) FROM Reservation")
    max_id = cursor.fetchone()[0] or 0
    new_id = max_id + 1
    
    cursor.execute('''
    INSERT INTO Reservation (id_reservation, date_arrivee, date_depart, id_client)
    VALUES (?, ?, ?, ?)
    ''', (new_id, date_arrivee, date_depart, id_client))
    
    cursor.execute('''
    INSERT INTO ReservationChambre (id_reservation, id_chambre)
    VALUES (?, ?)
    ''', (new_id, id_chambre))
    
    conn.commit()
    conn.close()
    return new_id

# Initialisation de la base de données
setup_database()

# Interface principale
st.markdown('<h1 class="main-title">🌿 Gestion Hôtelière</h1>', unsafe_allow_html=True)

# Sidebar Menu
with st.sidebar:
    menu_options = ["Tableau de bord", "Réservations", "Clients", "Nouvelle Réservation"]
    selected_tab = st.radio("Menu", menu_options, format_func=lambda x: f"📊 {x}" if x == "Tableau de bord" else f"📅 {x}" if x == "Réservations" else f"👤 {x}" if x == "Clients" else f"➕ {x}")

# Conteneur principal pour le contenu
with st.container():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    if selected_tab == "Tableau de bord":
        st.header("Tableau de bord des performances")
        
        # Métriques
        col1, col2, col3 = st.columns(3)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        with col1:
            cursor.execute("SELECT COUNT(*) FROM Reservation")
            total_reservations = cursor.fetchone()[0]
            st.markdown(f'<div class="stat-card">Total Réservations: {total_reservations} (↑ 12%)</div>', unsafe_allow_html=True)
        
        with col2:
            cursor.execute("SELECT COUNT(*) FROM Client")
            total_clients = cursor.fetchone()[0]
            st.markdown(f'<div class="stat-card">Clients Enregistrés: {total_clients} 👤</div>', unsafe_allow_html=True)
        
        with col3:
            cursor.execute("SELECT COUNT(*) FROM Chambre")
            total_chambres = cursor.fetchone()[0]
            st.markdown(f'<div class="stat-card">Chambres Disponibles: {total_chambres} 🛏️</div>', unsafe_allow_html=True)
        
        conn.close()
        
        # Réservations récentes
        with st.expander("Réservations Récentes", expanded=True):
            recent_reservations = fetch_reservations().head(5)
            if not recent_reservations.empty:
                st.dataframe(recent_reservations, use_container_width=True, hide_index=True)
            else:
                st.info("Aucune réservation trouvée")

    elif selected_tab == "Réservations":
        st.header("Gestion des Réservations")
        
        # Filtres
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Rafraîchir les Données"):
                st.rerun()
        with col2:
            client_search = st.text_input("Rechercher un client", placeholder="Nom du client...")
        
        all_reservations = fetch_reservations()
        
        # Filtrer par nom du client
        if client_search:
            all_reservations = all_reservations[all_reservations['Client'].str.contains(client_search, case=False, na=False)]
        
        with st.expander("Liste des Réservations", expanded=True):
            if not all_reservations.empty:
                st.dataframe(all_reservations, use_container_width=True, hide_index=True)
                st.info(f"Total : {len(all_reservations)} réservation(s)")
            else:
                st.info("Aucune réservation correspondant aux critères")

    elif selected_tab == "Clients":
        st.header("Administration des Clients")
        
        # Sous-onglets pour les clients
        with st.expander("Répertoire des Clients", expanded=True):
            client_data = fetch_clients()
            if not client_data.empty:
                st.dataframe(client_data, use_container_width=True, hide_index=True)
                st.info(f"Total : {len(client_data)} client(s)")
            else:
                st.info("Aucun client enregistré")
        
        with st.expander("Enregistrer un Client", expanded=False):
            st.subheader("Enregistrement d'un Nouveau Client")
            
            col1, col2 = st.columns(2)
            with col1:
                nom_complet = st.text_input("Nom complet *", placeholder="Jean Dupont")
                email = st.text_input("Adresse email", placeholder="jean.dupont@example.com")
            with col2:
                telephone = st.text_input("Numéro de téléphone", placeholder="0123456789")
                ville = st.text_input("Ville", placeholder="Paris")
            
            if st.button("➕ Enregistrer le Client", type="primary"):
                if nom_complet:
                    try:
                        new_client_id = add_new_client(nom_complet, email, telephone, ville)
                        st.success(f"✅ Client enregistré avec succès ! ID : {new_client_id}")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Erreur : {str(e)}")
                else:
                    st.error("Le champ Nom complet est requis")

    elif selected_tab == "Nouvelle Réservation":
        st.header("Nouvelle Réservation")
        
        # Étape 1 : Sélection des dates
        with st.expander("Sélectionner les Dates", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                date_arrivee = st.date_input("Date d'arrivée", value=date.today())
            with col2:
                date_depart = st.date_input("Date de départ", value=date.today())
        
        if date_arrivee >= date_depart:
            st.error("La date de départ doit être postérieure à la date d'arrivée")
        else:
            # Vérification de la disponibilité des chambres
            if st.button("🔍 Vérifier la Disponibilité", type="primary"):
                available_chambres = get_vacant_chambres(date_arrivee.strftime('%Y-%m-%d'), date_depart.strftime('%Y-%m-%d'))
                
                if not available_chambres.empty:
                    st.session_state['available_chambres'] = available_chambres
                    st.session_state['selected_dates'] = (date_arrivee, date_depart)
                    st.success(f"✅ {len(available_chambres)} chambre(s) disponible(s)")
                else:
                    st.warning("Aucune chambre disponible pour les dates sélectionnées")
                    st.session_state['available_chambres'] = pd.DataFrame()
            
            # Étape 2 : Sélection de la chambre et du client
            if 'available_chambres' in st.session_state and not st.session_state['available_chambres'].empty:
                with st.expander("Choisir une Chambre", expanded=True):
                    chambres_df = st.session_state['available_chambres']
                    
                    # Afficher les chambres disponibles
                    st.dataframe(chambres_df.drop('id_chambre', axis=1), use_container_width=True, hide_index=True)
                    
                    # Sélection de la chambre
                    chambre_choices = {}
                    for _, row in chambres_df.iterrows():
                        label = f"Chambre {row['Chambre']} - {row['Catégorie']} - {row['Hôtel']} ({row['Tarif']}€/nuit)"
                        chambre_choices[label] = row['id_chambre']
                    
                    selected_chambre = st.selectbox("Sélectionner une chambre", list(chambre_choices.keys()))
                    chosen_chambre_id = chambre_choices[selected_chambre]
                
                with st.expander("Sélectionner un Client", expanded=True):
                    # Liste des clients
                    clients_df = fetch_clients()
                    if clients_df.empty:
                        st.warning("Aucun client trouvé. Veuillez d'abord enregistrer des clients.")
                    else:
                        client_options = {}
                        for _, row in clients_df.iterrows():
                            label = f"{row['Nom']} - {row['Email']}"
                            client_options[label] = row['ID']
                        
                        selected_client = st.selectbox("Choisir un client", list(client_options.keys()))
                        chosen_client_id = client_options[selected_client]
                
                # Résumé
                with st.expander("Résumé de la Réservation", expanded=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Client :** {selected_client.split(' - ')[0]}")
                        st.write(f"**Arrivée :** {date_arrivee}")
                        st.write(f"**Départ :** {date_depart}")
                    with col2:
                        st.write(f"**Chambre :** {selected_chambre}")
                        st.write(f"**Durée :** {(date_depart - date_arrivee).days} nuit(s)")
                    
                    # Confirmation
                    if st.button("🎯 Confirmer la Réservation", type="primary"):
                        try:
                            new_reservation_id = create_reservation(
                                date_arrivee.strftime('%Y-%m-%d'), 
                                date_depart.strftime('%Y-%m-%d'), 
                                chosen_client_id, 
                                chosen_chambre_id
                            )
                            st.success(f"🎉 Réservation confirmée ! ID : {new_reservation_id}")
                            st.balloons()
                            
                            # Nettoyer l'état de la session
                            if 'available_chambres' in st.session_state:
                                del st.session_state['available_chambres']
                            if 'selected_dates' in st.session_state:
                                del st.session_state['selected_dates']
                                
                        except Exception as e:
                            st.error(f"Erreur : {str(e)}")

    # Fermer le conteneur principal
    st.markdown('</div>', unsafe_allow_html=True)

# Pied de page
st.markdown("---")
st.markdown("🌿 **Système de Gestion Hôtelière**")
st.markdown("**Made by Soukaina Elhasoubi, Ikram Elmouhib**")