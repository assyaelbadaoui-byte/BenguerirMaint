# ============================================================
#   BenguerirMaint — Application FINALE COMPLÈTE
#   OCP Benguerir | Épierrage · Criblage · Chargement
#   Pannes + Vibrations i-SENSE + IA Prédictive
#   PFE 2025-2026
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier

# ─── Configuration ──────────────────────────────────────────
st.set_page_config(
    page_title="BenguerirMaint — OCP",
    page_icon="⚙️",
    layout="wide"
)

VERT   = "#00843D"
ORANGE = "#F47920"
ROUGE  = "#dc2626"
GRIS   = "#6b7280"

# ════════════════════════════════════════════════════════════
#  SYSTÈME DE LOGIN — MOT DE PASSE
# ════════════════════════════════════════════════════════════

# ─── Comptes utilisateurs ───────────────────────────────────
# Vous pouvez modifier ces comptes selon vos besoins
USERS = {
    "admin":      {"password": "ocp2025",    "role": "Administrateur", "nom": "Admin OCP"},
    "ingenieur":  {"password": "benguerir",  "role": "Ingénieur",      "nom": "Ingénieur Maintenance"},
    "technicien": {"password": "convoyeur",  "role": "Technicien",     "nom": "Technicien Terrain"},
}

# ─── CSS page de login ──────────────────────────────────────
st.markdown(f"""
<style>
/* ── Reset général ── */
* {{ box-sizing: border-box; }}

/* ── Page login ── */
.login-wrap {{
    max-width: 420px;
    margin: 60px auto 0;
    padding: 0 16px;
}}
.login-logo {{
    text-align: center;
    margin-bottom: 28px;
}}
.login-logo-icon {{
    font-size: 3.5rem;
    display: block;
    margin-bottom: 8px;
}}
.login-logo-title {{
    font-size: 2rem;
    font-weight: 700;
    color: {VERT};
    margin: 0;
}}
.login-logo-sub {{
    font-size: 0.85rem;
    color: {GRIS};
    margin-top: 4px;
}}
.login-card {{
    background: white;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.10);
    border: 1px solid #e5e7eb;
}}
.login-title {{
    font-size: 1.1rem;
    font-weight: 600;
    color: #111827;
    margin-bottom: 1.5rem;
    text-align: center;
}}
.login-footer {{
    text-align: center;
    font-size: 11px;
    color: {GRIS};
    margin-top: 20px;
}}

/* ── App principale ── */
.header {{
    background: linear-gradient(135deg, {VERT}, #005a2b);
    padding: 1.2rem 2rem;
    border-radius: 14px;
    margin-bottom: 1.5rem;
    color: white;
    display: flex;
    align-items: center;
    justify-content: space-between;
}}
.h-left {{ flex: 1; }}
.h-title {{ font-size: 1.8rem; font-weight: 700; margin: 0; }}
.h-sub   {{ font-size: 0.85rem; opacity: 0.85; margin-top: 3px; }}
.h-badge {{
    background: rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 12px;
    color: white;
    text-align: right;
}}
.kpi {{
    background: white; border-radius: 10px;
    padding: 1rem 1.2rem;
    border-left: 4px solid {VERT};
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    margin-bottom: 8px;
}}
.kpi-warn   {{ border-left-color: {ORANGE} !important; }}
.kpi-danger {{ border-left-color: {ROUGE}  !important; }}
.kpi-lbl  {{ font-size:.75rem; color:{GRIS}; font-weight:600;
             text-transform:uppercase; letter-spacing:.05em; }}
.kpi-val  {{ font-size:1.9rem; font-weight:700;
             color:{VERT}; line-height:1.2; }}
.kpi-val-warn   {{ color:{ORANGE} !important; }}
.kpi-val-danger {{ color:{ROUGE}  !important; }}
.kpi-unit {{ font-size:.8rem; color:{GRIS}; }}
.alert-r {{ background:#fee2e2; border-left:4px solid {ROUGE};
            padding:12px 14px; border-radius:0 10px 10px 0; margin:6px 0; }}
.alert-o {{ background:#fff7ed; border-left:4px solid {ORANGE};
            padding:12px 14px; border-radius:0 10px 10px 0; margin:6px 0; }}
.alert-g {{ background:#f0fdf4; border-left:4px solid {VERT};
            padding:12px 14px; border-radius:0 10px 10px 0; margin:6px 0; }}
footer   {{ text-align:center; font-size:11px; color:{GRIS};
            margin-top:2rem; padding:1rem; }}
</style>
""", unsafe_allow_html=True)

# ─── Initialisation session ─────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user      = ""
    st.session_state.role      = ""
    st.session_state.nom       = ""

# ─── Page de Login ──────────────────────────────────────────
def page_login():

    # ── Logos en haut ────────────────────────────────────────
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        # Logo OCP (image officielle depuis internet)
        st.markdown(f"""
        <div style="text-align:center; margin-bottom: 10px;">
          <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/OCP_Group_logo.svg/320px-OCP_Group_logo.svg.png"
               width="140"
               style="margin-bottom:6px;"
               onerror="this.style.display='none'">
        </div>
        """, unsafe_allow_html=True)

        # Logo BenguerirMaint (texte stylisé)
        st.markdown(f"""
        <div style="
            text-align:center;
            background: linear-gradient(135deg, {VERT}, #005a2b);
            border-radius: 16px;
            padding: 22px 20px 16px;
            margin-bottom: 24px;
            box-shadow: 0 4px 20px rgba(0,132,61,0.25);
        ">
          <div style="font-size:3rem; margin-bottom:6px;">⚙️</div>
          <div style="
              font-size: 1.9rem;
              font-weight: 800;
              color: white;
              letter-spacing: -0.5px;
              margin-bottom: 4px;
          ">BenguerirMaint</div>
          <div style="
              font-size: 0.82rem;
              color: rgba(255,255,255,0.85);
              line-height: 1.6;
          ">
            Plateforme de maintenance prédictive<br>
            OCP Benguerir · Installations fixes<br>
            <span style="opacity:0.7;">Épierrage · Criblage · Chargement</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Formulaire de connexion ───────────────────────────
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 14px;
            padding: 24px;
            box-shadow: 0 2px 16px rgba(0,0,0,0.08);
            border: 1px solid #e5e7eb;
        ">
          <div style="
              font-size: 1rem;
              font-weight: 600;
              color: #111827;
              text-align: center;
              margin-bottom: 16px;
          ">🔐 Connexion</div>
        """, unsafe_allow_html=True)

        username = st.text_input(
            "👤 Identifiant",
            placeholder="Entrez votre identifiant"
        )
        password = st.text_input(
            "🔑 Mot de passe",
            type="password",
            placeholder="Entrez votre mot de passe"
        )

        if st.button("▶  Se connecter",
                     use_container_width=True,
                     type="primary"):
            if username in USERS and \
               USERS[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.user      = username
                st.session_state.role      = USERS[username]["role"]
                st.session_state.nom       = USERS[username]["nom"]
                st.rerun()
            else:
                st.error("❌ Identifiant ou mot de passe incorrect")

        st.markdown("</div>", unsafe_allow_html=True)

        # ── Pied de page login ────────────────────────────────
        st.markdown(f"""
        <div style="
            text-align:center;
            font-size: 11px;
            color: {GRIS};
            margin-top: 18px;
            line-height: 1.8;
        ">
          ⚙️ <b>BenguerirMaint</b> — PFE 2025-2026<br>
          OCP Benguerir · Mines de Benguerir<br><br>
          <b>Comptes de démonstration :</b><br>
          <code>admin</code> / <code>ocp2025</code> &nbsp;·&nbsp;
          <code>ingenieur</code> / <code>benguerir</code> &nbsp;·&nbsp;
          <code>technicien</code> / <code>convoyeur</code>
        </div>
        """, unsafe_allow_html=True)

# ─── Si pas connecté → afficher login ───────────────────────
if not st.session_state.logged_in:
    page_login()
    st.stop()

# ─── Si connecté → afficher l'application ───────────────────

# ─── En-tête avec nom utilisateur ───────────────────────────
st.markdown(f"""
<div class="header">
  <div class="h-left">
    <div class="h-title">⚙️ BenguerirMaint</div>
    <div class="h-sub">
      Plateforme complète de maintenance prédictive — OCP Benguerir<br>
      Pannes · Vibrations i-SENSE · Intelligence Artificielle ·
      Épierrage · Criblage · Chargement
    </div>
  </div>
  <div class="h-badge">
    👤 {st.session_state.nom}<br>
    <small>{st.session_state.role}</small>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Bouton déconnexion dans sidebar ────────────────────────
st.sidebar.markdown(f"""
### 👤 {st.session_state.nom}
**Rôle :** {st.session_state.role}
""")
if st.sidebar.button("🚪 Se déconnecter", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.user      = ""
    st.session_state.role      = ""
    st.session_state.nom       = ""
    st.rerun()
st.sidebar.markdown("---")

# ════════════════════════════════════════════════════════════
#  SIDEBAR — Chargement fichiers
# ════════════════════════════════════════════════════════════
st.sidebar.title("⚙️ BenguerirMaint")
st.sidebar.markdown("---")
st.sidebar.markdown("### 📂 Vos fichiers")

f_pannes = st.sidebar.file_uploader(
    "1️⃣ Fichier pannes (Excel)",
    type=["xlsx","xls"], key="pannes"
)
f_isense = st.sidebar.file_uploader(
    "2️⃣ Rapport i-SENSE (Excel/CSV)",
    type=["xlsx","xls","csv"], key="isense"
)
st.sidebar.markdown("---")

# ════════════════════════════════════════════════════════════
#  DONNÉES D'EXEMPLE
# ════════════════════════════════════════════════════════════
@st.cache_data
def ex_pannes():
    np.random.seed(42)
    sous = ["EPIERRAGE","CRIBLAGE","CHARGEMENT"]
    equip = {
        "EPIERRAGE":  ["CVB2","CVB4","CVB5","CVB6","CVB7","CVB9","CVB10"],
        "CRIBLAGE":   ["T1","T14B","T2","T3"],
        "CHARGEMENT": ["HAF","HCF","HBC01"],
    }
    desc  = ["Patinage","Rupture","Déclenchement","Nettoyage",
             "Déplacement","Retour produit","Liberation",
             "Réparation bande","Défaut"]
    natur = ["Mécanique","Electrique","Exploitation"]
    rows  = []
    for _ in range(280):
        su = np.random.choice(sous)
        eq = np.random.choice(equip[su])
        dur= round(abs(np.random.exponential(3.5)), 2)
        dt = pd.Timestamp("2024-01-01") + pd.Timedelta(
               days=int(np.random.randint(0,365)))
        rows.append({"Sous_Unite":su,"Equipement":eq,
                     "Description":np.random.choice(desc),
                     "Duree_h":dur,
                     "Nature":np.random.choice(natur),
                     "Date":dt})
    return pd.DataFrame(rows)

@st.cache_data
def ex_isense():
    np.random.seed(42)
    convs = ["CVB2","CVB4","CVB5","CVB6","CVB7","CVB9","CVB10",
             "T1","T14B","T2","T3","HAF","HCF","HBC01"]
    comps = ["Moteur d'entrainement","Réducteur",
             "Tambour de commande","Palier Bande"]
    dates = pd.date_range("2024-01-01","2025-01-05", freq="7D")
    rows  = []
    for cv in convs:
        base = np.random.uniform(0.01, 0.12)
        for dt in dates:
            for cp in comps:
                nga  = round(abs(np.random.normal(base,    0.02)), 3)
                ngv  = round(abs(np.random.normal(base*2,  0.05)), 3)
                temp = round(np.random.uniform(8,45),1) \
                       if np.random.random()>0.2 else None
                rows.append({"Convoyeur":cv,"Composant":cp,
                             "Nga":nga,"Ngv":ngv,
                             "Temperature":temp,"Date":dt})
    return pd.DataFrame(rows)

# ─── Chargement ─────────────────────────────────────────────
if f_pannes:
    df_p = pd.read_excel(f_pannes)
    for col in df_p.columns:
        c = col.lower().strip()
        if "sous"   in c: df_p.rename(columns={col:"Sous_Unite"},   inplace=True)
        elif "equip" in c: df_p.rename(columns={col:"Equipement"},  inplace=True)
        elif "dur"   in c: df_p.rename(columns={col:"Duree_h"},     inplace=True)
        elif "natur" in c: df_p.rename(columns={col:"Nature"},      inplace=True)
        elif "discri" in c or "descri" in c:
            df_p.rename(columns={col:"Description"}, inplace=True)
        elif "date"  in c: df_p.rename(columns={col:"Date"},        inplace=True)
    df_p["Duree_h"] = pd.to_numeric(df_p.get("Duree_h",0),
                                    errors="coerce").fillna(0)
    df_p["Date"]    = pd.to_datetime(df_p.get("Date",""),
                                     errors="coerce", dayfirst=True)
    st.sidebar.success(f"✅ {len(df_p)} lignes pannes")
else:
    df_p = ex_pannes()
    st.sidebar.info("💡 Données pannes exemple")

if f_isense:
    df_i = pd.read_csv(f_isense) if f_isense.name.endswith(".csv") \
           else pd.read_excel(f_isense)
    # Renommer les colonnes selon votre fichier réel
    df_i = df_i.rename(columns={
        "Nga (Acc.)":    "Nga",
        "Ngv (Vit.)":   "Ngv",
        "Temp (°C)":    "Temperature",
        "Point de Mesure": "Composant",
        "Organe":        "Composant",
    })
    st.sidebar.success(f"✅ {len(df_i)} mesures i-SENSE")
else:
    df_i = ex_isense()
    st.sidebar.info("💡 Données i-SENSE exemple")

# ════════════════════════════════════════════════════════════
#  CALCULS FIABILITÉ (depuis pannes)
# ════════════════════════════════════════════════════════════
df_p = df_p.sort_values(["Equipement","Date"]).reset_index(drop=True)
df_p["Debut_Suiv"] = df_p.groupby("Equipement")["Date"].shift(-1)
df_p["MTBF_inst"]  = (
    df_p["Debut_Suiv"] - df_p["Date"]
).dt.total_seconds() / 3600

stats_p = df_p.groupby(["Sous_Unite","Equipement"]).agg(
    Nb_Pannes   = ("Duree_h","count"),
    MTTR        = ("Duree_h","mean"),
    MTBF        = ("MTBF_inst","mean"),
    Duree_tot   = ("Duree_h","sum"),
).reset_index()
stats_p["MTTR"] = stats_p["MTTR"].round(2)
stats_p["MTBF"] = stats_p["MTBF"].fillna(8760).round(0)
stats_p["Dispo_%"] = (
    stats_p["MTBF"] / (stats_p["MTBF"] + stats_p["MTTR"]) * 100
).clip(0,100).round(1)

# ════════════════════════════════════════════════════════════
#  CALCULS VIBRATOIRES + IA (depuis i-SENSE)
# ════════════════════════════════════════════════════════════
# ─── Renommage flexible colonnes i-SENSE ───────────────────
rename_isense = {}
for col in df_i.columns:
    cl = col.lower().strip()
    if "nga" in cl:         rename_isense[col] = "Nga"
    elif "ngv" in cl:       rename_isense[col] = "Ngv"
    elif "temp" in cl:      rename_isense[col] = "Temperature"
    elif "convoyeur" in cl: rename_isense[col] = "Convoyeur"
    elif "organe" in cl or "point" in cl or "composant" in cl:
        rename_isense[col] = "Composant"
df_i = df_i.rename(columns=rename_isense)

# Ajouter colonnes manquantes si absentes
for col in ["Nga","Ngv","Temperature","Convoyeur"]:
    if col not in df_i.columns:
        df_i[col] = 0 if col != "Convoyeur" else "Inconnu"

feats = df_i.groupby("Convoyeur").agg(
    Nga_max  = ("Nga","max"),
    Nga_mean = ("Nga","mean"),
    Ngv_max  = ("Ngv","max"),
    Ngv_mean = ("Ngv","mean"),
    Temp_max = ("Temperature","max"),
).reset_index()
feats["Temp_max"] = feats["Temp_max"].fillna(20)

nb_p = df_p.groupby("Equipement").size().reset_index()
nb_p.columns = ["Convoyeur","Nb_Pannes"]
feats = feats.merge(nb_p, on="Convoyeur", how="left")
feats["Nb_Pannes"] = feats["Nb_Pannes"].fillna(0)

# Health Score combiné (vibrations + pannes)
feats["Health_Score"] = (100 - (
    feats["Nga_max"]  / 0.15 * 20 +
    feats["Ngv_max"]  / 0.35 * 30 +
    (feats["Temp_max"] - 20).clip(0) / 60 * 25 +
    feats["Nb_Pannes"].clip(0,10)   / 10  * 25
)).clip(0,100).round(0)

feats["Niveau"] = feats["Health_Score"].apply(
    lambda s: "CRITIQUE" if s<40 else "DÉGRADÉ" if s<65 else "BON"
)


# Modèle Random Forest
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

cols_rf = ["Nga_max","Nga_mean","Ngv_max","Ngv_mean","Temp_max","Nb_Pannes"]

X = feats[cols_rf]
y = feats["Niveau"]

validation_ok = False

if len(y.unique()) > 1 and len(feats) >= 10:

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.30,
        random_state=42,
        stratify=y if y.value_counts().min() >= 2 else None
    )

    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="weighted", zero_division=0)
    recall = recall_score(y_test, y_pred, average="weighted", zero_division=0)
    f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)
    cm = confusion_matrix(y_test, y_pred, labels=["BON", "DÉGRADÉ", "CRITIQUE"])

    feats["Niveau_RF"] = rf.predict(X)
    validation_ok = True

else:
    feats["Niveau_RF"] = feats["Niveau"]

# Probabilité de panne basée sur le Health Score
feats["Proba_Panne_%"] = (100 - feats["Health_Score"]).round(1)

# ════════════════════════════════════════════════════════════
#  SIDEBAR — FILTRES
# ════════════════════════════════════════════════════════════
st.sidebar.markdown("### 🔽 Filtres")
unites = ["Toutes"] + sorted(df_p["Sous_Unite"].dropna().unique().tolist())
f_unite = st.sidebar.selectbox("Unité", unites)
f_natur = st.sidebar.multiselect(
    "Nature d'arrêt",
    sorted(df_p["Nature"].dropna().unique().tolist()),
    default=sorted(df_p["Nature"].dropna().unique().tolist())
)
st.sidebar.markdown("---")
st.sidebar.caption("BenguerirMaint · PFE 2025-2026 · OCP Benguerir")

# Filtrage
df_pf = df_p.copy()
sf    = stats_p.copy()
if f_unite != "Toutes":
    df_pf = df_pf[df_pf["Sous_Unite"] == f_unite]
    sf    = sf[sf["Sous_Unite"] == f_unite]
if f_natur:
    df_pf = df_pf[df_pf["Nature"].isin(f_natur)]

# ════════════════════════════════════════════════════════════
#  ONGLETS PRINCIPAUX
# ════════════════════════════════════════════════════════════
t1,t2,t3,t4,t5,t6,t7,t8 = st.tabs([
    "🏠 Accueil",
    "📊 Tableau de bord",
    "🔍 Convoyeurs",
    "📈 Pareto & Analyses",
    "📡 Vibrations i-SENSE",
    "🤖 IA Prédictive",
    "🚨 Alertes",
    "🔧 Interventions",
])

# ─── Stockage interventions (session) ───────────────────────
if "interventions" not in st.session_state:
    st.session_state.interventions = []

# ────────────────────────────────────────────────────────────
# ONGLET 1 — Tableau de bord KPI
# ────────────────────────────────────────────────────────────
with t2:
    st.subheader("Indicateurs globaux du parc")

    mtbf_g  = round(sf["MTBF"].mean())
    mttr_g  = round(sf["MTTR"].mean(), 1)
    dispo_g = round(sf["Dispo_%"].mean(), 1)
    nb_cv   = sf["Equipement"].nunique()
    critiq  = (feats["Niveau"]=="CRITIQUE").sum()
    tot_arr = round(df_pf["Duree_h"].sum(), 1)

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.markdown(f'<div class="kpi"><div class="kpi-lbl">MTBF moyen</div>'
                f'<div class="kpi-val">{mtbf_g}</div>'
                f'<div class="kpi-unit">heures</div></div>',
                unsafe_allow_html=True)
    c2.markdown(f'<div class="kpi kpi-warn"><div class="kpi-lbl">MTTR moyen</div>'
                f'<div class="kpi-val kpi-val-warn">{mttr_g}</div>'
                f'<div class="kpi-unit">heures</div></div>',
                unsafe_allow_html=True)
    c3.markdown(f'<div class="kpi"><div class="kpi-lbl">Disponibilité</div>'
                f'<div class="kpi-val">{dispo_g}</div>'
                f'<div class="kpi-unit">%</div></div>',
                unsafe_allow_html=True)
    c4.markdown(f'<div class="kpi"><div class="kpi-lbl">Convoyeurs</div>'
                f'<div class="kpi-val">{nb_cv}</div>'
                f'<div class="kpi-unit">équipements</div></div>',
                unsafe_allow_html=True)
    c5.markdown(f'<div class="kpi kpi-danger"><div class="kpi-lbl">Critiques IA</div>'
                f'<div class="kpi-val kpi-val-danger">{critiq}</div>'
                f'<div class="kpi-unit">convoyeurs</div></div>',
                unsafe_allow_html=True)
    c6.markdown(f'<div class="kpi kpi-warn"><div class="kpi-lbl">Total arrêts</div>'
                f'<div class="kpi-val kpi-val-warn">{tot_arr}</div>'
                f'<div class="kpi-unit">heures</div></div>',
                unsafe_allow_html=True)

    st.markdown("---")
    g1,g2 = st.columns(2)

    with g1:
        st.markdown("**Disponibilité par sous-unité**")
        du = sf.groupby("Sous_Unite")["Dispo_%"].mean().reset_index()
        fig = px.bar(du, x="Sous_Unite", y="Dispo_%",
                     color="Dispo_%",
                     color_continuous_scale=[ROUGE, ORANGE, VERT],
                     range_color=[85,100], text="Dispo_%")
        fig.update_traces(texttemplate='%{text:.1f}%',
                          textposition='outside')
        fig.update_layout(height=300, yaxis_range=[80,102],
                          coloraxis_showscale=False,
                          xaxis_title="", yaxis_title="Disponibilité (%)")
        st.plotly_chart(fig, use_container_width=True, key='chart_1')

    with g2:
        st.markdown("**Répartition par nature d'arrêt**")
        nc = df_pf["Nature"].value_counts().reset_index()
        nc.columns = ["Nature","Nb"]
        fig2 = px.pie(nc, names="Nature", values="Nb",
                      color="Nature",
                      color_discrete_map={
                          "Mécanique":   VERT,
                          "Electrique":  ORANGE,
                          "Exploitation":"#3b82f6"
                      }, hole=0.42)
        fig2.update_layout(height=300)
        st.plotly_chart(fig2, use_container_width=True, key='chart_2')

    if "Date" in df_pf.columns and df_pf["Date"].notna().any():
        st.markdown("**Évolution des pannes par mois**")
        ev = df_pf.groupby(df_pf["Date"].dt.to_period("M")).agg(
            Nb=("Duree_h","count"),
            Dur=("Duree_h","sum")
        ).reset_index()
        ev["Date"] = ev["Date"].astype(str)
        fig3 = px.line(ev, x="Date", y="Nb",
                       markers=True,
                       color_discrete_sequence=[VERT],
                       title="Nombre de pannes par mois")
        fig3.update_layout(height=260,
                           xaxis_title="Mois",
                           yaxis_title="Nb pannes")
        st.plotly_chart(fig3, use_container_width=True, key='chart_3')

    # ════════════════════════════════════════════════════════
    #  SECTION COÛTS — Données réelles OCP Benguerir
    # ════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("### 💰 Analyse des coûts — Installations fixes OCP Benguerir")

    # ── Paramètres coûts (modifiables) ──────────────────────
    with st.expander("⚙️ Paramètres de calcul des coûts", expanded=False):
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            cout_heure_meca = st.number_input(
                "Coût maintenance mécanique (MAD/heure)",
                min_value=100, max_value=10000,
                value=800, step=100,
                help="Coût horaire moyen d'une intervention mécanique"
            )
            cout_heure_elec = st.number_input(
                "Coût maintenance électrique (MAD/heure)",
                min_value=100, max_value=10000,
                value=600, step=100,
                help="Coût horaire moyen d'une intervention électrique"
            )
        with col_p2:
            cout_heure_prod = st.number_input(
                "Coût perte production (MAD/heure)",
                min_value=1000, max_value=100000,
                value=15000, step=1000,
                help="Perte de production par heure d'arrêt non planifié"
            )
            reduction_ia = st.slider(
                "Réduction des arrêts avec l'IA (%)",
                min_value=10, max_value=50,
                value=30,
                help="Réduction attendue grâce à BenguerirMaint (benchmark industrie)"
            )

    # ── Calculs des coûts ────────────────────────────────────
    # Coût par nature depuis les données réelles
    cout_par_nature = df_pf.groupby("Nature").agg(
        Nb_pannes   = ("Duree_h", "count"),
        Duree_totale= ("Duree_h", "sum")
    ).reset_index()

    def cout_intervention(row):
        if "mécanique" in row["Nature"].lower() or "mecanique" in row["Nature"].lower():
            return round(row["Duree_totale"] * cout_heure_meca)
        elif "electrique" in row["Nature"].lower() or "électrique" in row["Nature"].lower():
            return round(row["Duree_totale"] * cout_heure_elec)
        else:
            return round(row["Duree_totale"] * 400)

    cout_par_nature["Cout_Maintenance_MAD"] = cout_par_nature.apply(
        cout_intervention, axis=1
    )
    cout_par_nature["Cout_Production_MAD"] = (
        cout_par_nature["Duree_totale"] * cout_heure_prod
    ).round(0).astype(int)
    cout_par_nature["Cout_Total_MAD"] = (
        cout_par_nature["Cout_Maintenance_MAD"] +
        cout_par_nature["Cout_Production_MAD"]
    )

    # Totaux
    cout_maint_total = int(cout_par_nature["Cout_Maintenance_MAD"].sum())
    cout_prod_total  = int(cout_par_nature["Cout_Production_MAD"].sum())
    cout_total       = int(cout_par_nature["Cout_Total_MAD"].sum())
    economie_ia      = int(cout_total * reduction_ia / 100)

    # Données réelles OCP du PPT
    COUT_OCP_2025    = 4_000_000   # 4 MDH réel 2025
    COUT_OCP_2026    = 6_730_000   # 6.73 MDH prévu 2026 sans action
    GAIN_INITIATIVE4 = 300_000     # 0.30 MDH gain Initiative 4 i-SENSE

    # ── KPI Coûts ────────────────────────────────────────────
    st.markdown("#### Indicateurs financiers calculés")
    kc1, kc2, kc3, kc4 = st.columns(4)

    kc1.markdown(f"""
    <div class="kpi kpi-danger">
      <div class="kpi-lbl">Coût maintenance estimé</div>
      <div class="kpi-val kpi-val-danger">{cout_maint_total/1000:.0f}k</div>
      <div class="kpi-unit">MAD / an</div>
    </div>""", unsafe_allow_html=True)

    kc2.markdown(f"""
    <div class="kpi kpi-danger">
      <div class="kpi-lbl">Coût perte production</div>
      <div class="kpi-val kpi-val-danger">{cout_prod_total/1000:.0f}k</div>
      <div class="kpi-unit">MAD / an</div>
    </div>""", unsafe_allow_html=True)

    kc3.markdown(f"""
    <div class="kpi kpi-warn">
      <div class="kpi-lbl">Coût total arrêts</div>
      <div class="kpi-val kpi-val-warn">{cout_total/1_000_000:.2f}M</div>
      <div class="kpi-unit">MAD / an</div>
    </div>""", unsafe_allow_html=True)

    kc4.markdown(f"""
    <div class="kpi" style="border-left-color:{VERT};">
      <div class="kpi-lbl">Économie avec BenguerirMaint</div>
      <div class="kpi-val" style="color:{VERT};">{economie_ia/1000:.0f}k</div>
      <div class="kpi-unit">MAD / an ({reduction_ia}% réduction)</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(" ")

    # ── Données officielles OCP ──────────────────────────────
    st.markdown("#### Référence OCP Benguerir — Plan P&L 2025-2026")
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0a1628,#0d2137);
                border-radius:14px;padding:1.4rem;margin:8px 0;">
      <div style="display:flex;flex-wrap:wrap;gap:16px;">

        <div style="flex:1;min-width:140px;text-align:center;
                    background:rgba(220,38,38,0.2);border-radius:10px;padding:14px;">
          <div style="font-size:11px;color:rgba(255,255,255,0.6);
                      text-transform:uppercase;letter-spacing:.05em;">
            Consommation bandes 2025
          </div>
          <div style="font-size:1.8rem;font-weight:800;color:#f87171;">
            4,0 MDH
          </div>
          <div style="font-size:11px;color:rgba(255,255,255,0.5);">Réel — Source OCP</div>
        </div>

        <div style="flex:1;min-width:140px;text-align:center;
                    background:rgba(245,158,11,0.2);border-radius:10px;padding:14px;">
          <div style="font-size:11px;color:rgba(255,255,255,0.6);
                      text-transform:uppercase;letter-spacing:.05em;">
            Prévision 2026 sans action
          </div>
          <div style="font-size:1.8rem;font-weight:800;color:{ORANGE};">
            6,73 MDH
          </div>
          <div style="font-size:11px;color:rgba(255,255,255,0.5);">+68% vs 2025</div>
        </div>

        <div style="flex:1;min-width:140px;text-align:center;
                    background:rgba(0,132,61,0.2);border-radius:10px;padding:14px;">
          <div style="font-size:11px;color:rgba(255,255,255,0.6);
                      text-transform:uppercase;letter-spacing:.05em;">
            Gain Initiative 4 (i-SENSE)
          </div>
          <div style="font-size:1.8rem;font-weight:800;color:#4ade80;">
            0,30 MDH
          </div>
          <div style="font-size:11px;color:rgba(255,255,255,0.5);">Investissement : 0 MAD</div>
        </div>

        <div style="flex:1;min-width:140px;text-align:center;
                    background:rgba(0,132,61,0.3);border-radius:10px;padding:14px;">
          <div style="font-size:11px;color:rgba(255,255,255,0.6);
                      text-transform:uppercase;letter-spacing:.05em;">
            Gain total 4 initiatives
          </div>
          <div style="font-size:1.8rem;font-weight:800;color:#4ade80;">
            1,47 MDH
          </div>
          <div style="font-size:11px;color:rgba(255,255,255,0.5);">Plan P&L 2026 OCP</div>
        </div>

      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(" ")

    # ── Graphiques coûts ────────────────────────────────────
    gc1, gc2 = st.columns(2)

    with gc1:
        st.markdown("**Coût total par nature d'arrêt (MAD)**")
        fig_cout = go.Figure()
        fig_cout.add_trace(go.Bar(
            name="Coût maintenance",
            x=cout_par_nature["Nature"],
            y=cout_par_nature["Cout_Maintenance_MAD"],
            marker_color=ORANGE
        ))
        fig_cout.add_trace(go.Bar(
            name="Coût perte production",
            x=cout_par_nature["Nature"],
            y=cout_par_nature["Cout_Production_MAD"],
            marker_color=ROUGE
        ))
        fig_cout.update_layout(
            barmode="stack", height=320,
            xaxis_title="Nature d'arrêt",
            yaxis_title="Coût (MAD)",
            legend=dict(orientation="h", y=-0.25),
            title="Décomposition des coûts par nature"
        )
        st.plotly_chart(fig_cout, use_container_width=True, key="chart_cout1")

    with gc2:
        st.markdown("**Évolution des coûts OCP 2025-2026 (MDH)**")
        annees = ["2025 (réel)", "2026 (sans action)", "2026 (avec BenguerirMaint)"]
        valeurs = [4.0, 6.73, round((6.73 - GAIN_INITIATIVE4/1_000_000), 2)]
        couleurs = [ORANGE, ROUGE, VERT]
        fig_evol = go.Figure(go.Bar(
            x=annees, y=valeurs,
            marker_color=couleurs,
            text=[f"{v} MDH" for v in valeurs],
            textposition="outside"
        ))
        fig_evol.add_hline(
            y=4.0, line_dash="dash", line_color=ORANGE,
            annotation_text="Référence 2025"
        )
        fig_evol.update_layout(
            height=320, yaxis_range=[0, 8],
            yaxis_title="Coût (MDH)",
            title="Impact de BenguerirMaint sur les coûts OCP"
        )
        st.plotly_chart(fig_evol, use_container_width=True, key="chart_cout2")

    # ── Coût par convoyeur ───────────────────────────────────
    st.markdown("**Coût estimé par convoyeur (MAD)**")
    cout_cv = df_pf.groupby("Equipement").agg(
        Duree_tot = ("Duree_h", "sum"),
        Nb_pannes = ("Duree_h", "count")
    ).reset_index()
    cout_cv["Cout_Maint_MAD"]  = (cout_cv["Duree_tot"] * cout_heure_meca).round(0).astype(int)
    cout_cv["Cout_Prod_MAD"]   = (cout_cv["Duree_tot"] * cout_heure_prod).round(0).astype(int)
    cout_cv["Cout_Total_MAD"]  = cout_cv["Cout_Maint_MAD"] + cout_cv["Cout_Prod_MAD"]
    cout_cv = cout_cv.sort_values("Cout_Total_MAD", ascending=False)

    fig_cv = px.bar(
        cout_cv, x="Equipement", y="Cout_Total_MAD",
        color="Cout_Total_MAD",
        color_continuous_scale=[VERT, ORANGE, ROUGE],
        title="Coût total estimé par convoyeur (MAD)",
        labels={"Cout_Total_MAD": "Coût total (MAD)", "Equipement": "Convoyeur"},
        text="Cout_Total_MAD"
    )
    fig_cv.update_traces(texttemplate='%{text:,.0f}', textposition="outside")
    fig_cv.update_layout(height=320, coloraxis_showscale=False)
    st.plotly_chart(fig_cv, use_container_width=True, key="chart_cout3")

    # ── ROI BenguerirMaint ───────────────────────────────────
    st.markdown("#### 📈 Retour sur investissement de BenguerirMaint")
    r1, r2, r3 = st.columns(3)
    r1.metric("Coût de développement",     "0 MAD",
              delta="Moyens internes OCP", delta_color="off")
    r2.metric("Économies annuelles",
              f"{economie_ia:,.0f} MAD",
              delta=f"{reduction_ia}% de réduction")
    r3.metric("Retour sur investissement",
              "Immédiat",
              delta="ROI = ∞ (investissement = 0)")

    st.success(
        f"✅ En appliquant BenguerirMaint sur les installations fixes OCP Benguerir, "
        f"l'économie estimée est de **{economie_ia:,.0f} MAD/an** "
        f"({reduction_ia}% de réduction des coûts d'arrêt), "
        f"conformément à l'**Initiative 4** du Plan P&L 2026 OCP "
        f"qui prévoit un gain de **0,30 MDH/an** grâce à la maintenance prédictive i-SENSE."
    )

# ────────────────────────────────────────────────────────────
# ONGLET 2 — Convoyeurs
# ────────────────────────────────────────────────────────────
with t3:
    st.subheader(f"Parc convoyeurs — {len(sf)} équipements")

    def badge(n):
        if n=="CRITIQUE": return "🔴 CRITIQUE"
        if n=="DÉGRADÉ":  return "🟡 DÉGRADÉ"
        return "🟢 BON"

    # Fusionner stats pannes + IA
    sf2 = sf.merge(
        feats[["Convoyeur","Health_Score","Niveau","Proba_Panne_%"]],
        left_on="Equipement", right_on="Convoyeur", how="left"
    )
    sf2["Health_Score"] = sf2["Health_Score"].fillna(75)
    sf2["Niveau"]       = sf2["Niveau"].fillna("BON")
    sf2["Proba_Panne_%"]= sf2["Proba_Panne_%"].fillna(25)

    aff = sf2[[
        "Sous_Unite","Equipement","Nb_Pannes",
        "MTBF","MTTR","Dispo_%",
        "Health_Score","Proba_Panne_%","Niveau"
    ]].copy()
    aff["Niveau"] = aff["Niveau"].apply(badge)
    aff = aff.rename(columns={
        "Sous_Unite":    "Sous-unité",
        "Nb_Pannes":     "Nb Pannes",
        "Dispo_%":       "Dispo %",
        "Health_Score":  "Score Santé /100",
        "Proba_Panne_%": "Proba Panne %"
    })
    st.dataframe(aff.sort_values("Score Santé /100"),
                 use_container_width=True, height=400)

    st.markdown("**MTBF vs MTTR par convoyeur**")
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(x=sf["Equipement"], y=sf["MTBF"],
                          name="MTBF", marker_color=VERT))
    fig4.add_trace(go.Bar(x=sf["Equipement"], y=sf["MTTR"],
                          name="MTTR", marker_color=ORANGE))
    fig4.update_layout(barmode="group", height=300,
                       xaxis_title="Equipement",
                       yaxis_title="Heures")
    st.plotly_chart(fig4, use_container_width=True, key='chart_4')

# ────────────────────────────────────────────────────────────
# ONGLET 3 — Pareto
# ────────────────────────────────────────────────────────────
with t4:
    st.markdown("### Pareto des descriptions d'arrêt")
    par = df_pf["Description"].value_counts().reset_index()
    par.columns = ["Description","Nb"]
    par["Cum_%"] = (par["Nb"].cumsum()/par["Nb"].sum()*100).round(1)

    fig5 = go.Figure()
    fig5.add_trace(go.Bar(x=par["Description"], y=par["Nb"],
                          name="Nb pannes", marker_color=VERT))
    fig5.add_trace(go.Scatter(x=par["Description"], y=par["Cum_%"],
                              name="% cumulé", yaxis="y2",
                              line=dict(color=ORANGE, width=2.5),
                              mode="lines+markers"))
    fig5.add_hline(y=80, line_dash="dash", line_color=ROUGE,
                   yref="y2", annotation_text="Seuil 80%")
    fig5.update_layout(
        yaxis =dict(title="Nombre de pannes"),
        yaxis2=dict(title="% cumulé", overlaying="y",
                    side="right", range=[0,105]),
        height=380, legend=dict(orientation="h", y=-0.25),
        title="Pareto des arrêts — BenguerirMaint"
    )
    st.plotly_chart(fig5, use_container_width=True, key='chart_5')

    c1,c2 = st.columns(2)
    with c1:
        st.markdown("**Durée totale par équipement**")
        fig6 = px.bar(
            sf.sort_values("Duree_tot", ascending=False),
            x="Equipement", y="Duree_tot",
            color="Sous_Unite",
            color_discrete_sequence=[VERT, ORANGE, "#3b82f6"],
            title="Heures d'arrêt cumulées"
        )
        fig6.update_layout(height=300)
        st.plotly_chart(fig6, use_container_width=True, key='chart_6')

    with c2:
        st.markdown("**Pareto par nature d'arrêt**")
        nat = df_pf.groupby("Nature")["Duree_h"].sum().reset_index()
        nat = nat.sort_values("Duree_h", ascending=False)
        fig7 = px.bar(nat, x="Nature", y="Duree_h",
                      color="Nature",
                      color_discrete_map={
                          "Mécanique":   VERT,
                          "Electrique":  ORANGE,
                          "Exploitation":"#3b82f6"
                      },
                      title="Durée totale par nature (h)")
        fig7.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig7, use_container_width=True, key='chart_7')

# ────────────────────────────────────────────────────────────
# ONGLET 4 — Vibrations i-SENSE
# ────────────────────────────────────────────────────────────
with t5:
    st.subheader("Analyse vibratoire — i-SENSE")

    with st.expander("📖 Légende i-SENSE", expanded=False):
        col1,col2,col3 = st.columns(3)
        col1.info("**Nga** — Niveau Global Accélération\nChocs & défauts roulements\nSeuil critique : > 0.1")
        col2.warning("**Ngv** — Niveau Global Vibration\nUsure générale\nSeuil critique : > 0.3")
        col3.error("**Temp** — Température °C\nEchauffement\nSeuil critique : > 80°C")

    nga_max = df_i["Nga"].max()
    ngv_max = df_i["Ngv"].max()
    nb_crit = (feats["Niveau"]=="CRITIQUE").sum()

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Nga max", f"{nga_max:.3f}",
              delta="⚠️ Critique" if nga_max>0.1 else "✅ Normal")
    c2.metric("Ngv max", f"{ngv_max:.3f}",
              delta="⚠️ Critique" if ngv_max>0.3 else "✅ Normal")
    c3.metric("Temp max",
              f"{df_i['Temperature'].max():.1f}°C")
    c4.metric("Capteurs critiques", nb_crit)

    st.markdown("---")
    g1,g2 = st.columns(2)

    with g1:
        st.markdown("**Ngv max par convoyeur**")
        ngv_c = df_i.groupby("Convoyeur")["Ngv"].max().reset_index()
        ngv_c = ngv_c.sort_values("Ngv", ascending=False)
        cols_c = [ROUGE if v>0.3 else ORANGE if v>0.15 else VERT
                  for v in ngv_c["Ngv"]]
        fig8 = go.Figure(go.Bar(
            x=ngv_c["Convoyeur"], y=ngv_c["Ngv"],
            marker_color=cols_c,
            text=ngv_c["Ngv"].round(3), textposition="outside"
        ))
        fig8.add_hline(y=0.3, line_dash="dash", line_color=ROUGE,
                       annotation_text="Seuil critique")
        fig8.add_hline(y=0.15, line_dash="dash", line_color=ORANGE,
                       annotation_text="Seuil dégradé")
        fig8.update_layout(height=320, xaxis_title="Convoyeur",
                           yaxis_title="Ngv (mm/s)")
        st.plotly_chart(fig8, use_container_width=True, key='chart_8')

    with g2:
        st.markdown("**Température max par convoyeur**")
        tmp = df_i.dropna(subset=["Temperature"])
        tmp = tmp.groupby("Convoyeur")["Temperature"].max().reset_index()
        tmp = tmp.sort_values("Temperature", ascending=False)
        cols_t = [ROUGE if t>80 else ORANGE if t>60 else VERT
                  for t in tmp["Temperature"]]
        fig9 = go.Figure(go.Bar(
            x=tmp["Convoyeur"], y=tmp["Temperature"],
            marker_color=cols_t,
            text=tmp["Temperature"].round(1), textposition="outside"
        ))
        fig9.add_hline(y=80, line_dash="dash", line_color=ROUGE,
                       annotation_text="Seuil critique 80°C")
        fig9.update_layout(height=320, xaxis_title="Convoyeur",
                           yaxis_title="Température (°C)")
        st.plotly_chart(fig9, use_container_width=True, key='chart_9')

    st.markdown("**Évolution vibratoire dans le temps**")
    cv_sel = st.selectbox("Choisir un convoyeur",
                          df_i["Convoyeur"].unique(), key="cv_vib")
    df_sel = df_i[df_i["Convoyeur"]==cv_sel]
    ngv_t  = df_sel.groupby("Date")["Ngv"].max().reset_index()

    fig10 = go.Figure()
    fig10.add_trace(go.Scatter(
        x=ngv_t["Date"], y=ngv_t["Ngv"],
        mode="lines+markers",
        line=dict(color=VERT, width=2), name="Ngv"
    ))
    fig10.add_hrect(y0=0.15, y1=ngv_t["Ngv"].max()*1.1,
                    fillcolor=ROUGE, opacity=0.07, line_width=0)
    fig10.add_hline(y=0.3, line_dash="dash", line_color=ROUGE,
                    annotation_text="Seuil critique")
    fig10.add_hline(y=0.15, line_dash="dash", line_color=ORANGE,
                    annotation_text="Seuil dégradé")
    fig10.update_layout(height=280,
                        title=f"Évolution Ngv — {cv_sel}",
                        yaxis_title="Ngv", xaxis_title="Date")
    st.plotly_chart(fig10, use_container_width=True, key='chart_10')

# ────────────────────────────────────────────────────────────
# ONGLET 5 — IA Prédictive
# ────────────────────────────────────────────────────────────
with t6:
    st.subheader("🤖 Maintenance Prédictive — Random Forest")

    st.info("""
    **Comment fonctionne l'IA ?**
    Le modèle Random Forest analyse 6 indicateurs pour chaque convoyeur :
    Nga max, Ngv max, Température max, Nga moyen, Ngv moyen, Nb pannes historiques.
    Il calcule ensuite un **Health Score** (0-100) et une **probabilité de panne**.
    """)

    c1,c2,c3 = st.columns(3)
    c1.metric("Convoyeurs analysés", len(feats))
    c2.metric("Score santé moyen",
              f"{feats['Health_Score'].mean():.0f}/100")
    c3.metric("En état critique",
              (feats["Niveau"]=="CRITIQUE").sum())

    st.markdown("---")
    st.markdown("**Health Score et probabilité de panne**")

    ft_tri = feats.sort_values("Health_Score")
    cols_h = [ROUGE if s<40 else ORANGE if s<65 else VERT
              for s in ft_tri["Health_Score"]]
    fig11 = go.Figure()
    fig11.add_trace(go.Bar(
        x=ft_tri["Convoyeur"],
        y=ft_tri["Health_Score"],
        marker_color=cols_h,
        text=ft_tri["Health_Score"].astype(int),
        textposition="outside", name="Health Score"
    ))
    fig11.add_hline(y=40, line_dash="dash", line_color=ROUGE,
                    annotation_text="Seuil critique")
    fig11.add_hline(y=65, line_dash="dash", line_color=ORANGE,
                    annotation_text="Seuil dégradé")
    fig11.update_layout(height=320, yaxis_range=[0,115],
                        yaxis_title="Health Score /100",
                        xaxis_title="Convoyeur",
                        title="Health Score — BenguerirMaint IA")
    st.plotly_chart(fig11, use_container_width=True, key='chart_11')

    st.markdown("**Tableau complet des prédictions**")
    aff_ia = feats[[
        "Convoyeur","Nga_max","Ngv_max","Temp_max",
        "Nb_Pannes","Health_Score","Proba_Panne_%","Niveau"
    ]].copy()
    aff_ia["Niveau"] = aff_ia["Niveau"].apply(
        lambda n: "🔴 CRITIQUE" if n=="CRITIQUE"
                  else "🟡 DÉGRADÉ" if n=="DÉGRADÉ" else "🟢 BON"
    )
    aff_ia = aff_ia.rename(columns={
        "Nga_max":"Nga Max",
        "Ngv_max":"Ngv Max",
        "Temp_max":"Temp Max °C",
        "Nb_Pannes":"Nb Pannes",
        "Health_Score":"Score /100",
        "Proba_Panne_%":"Proba Panne %"
    })
    st.dataframe(aff_ia.sort_values("Score /100"),
                 use_container_width=True, height=350)

    # Importance des variables
    st.markdown("**Importance des variables pour l'IA**")
    if len(y.unique()) > 1:
        importances = rf.feature_importances_
        imp_df = pd.DataFrame({
            "Variable": ["Nga max","Nga moyen","Ngv max",
                         "Ngv moyen","Temp max","Nb pannes"],
            "Importance": importances
        }).sort_values("Importance", ascending=True)
        fig12 = px.bar(imp_df, x="Importance", y="Variable",
                       orientation="h",
                       color="Importance",
                       color_continuous_scale=[ORANGE, VERT],
                       title="Quels capteurs influencent le plus la prédiction ?")
        fig12.update_layout(height=280,
                            coloraxis_showscale=False)
        st.plotly_chart(fig12, use_container_width=True, key='chart_12')

    st.markdown("---")
    st.subheader("Validation du modèle Random Forest")

    if validation_ok:
        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Accuracy", f"{accuracy*100:.1f}%")
        c2.metric("Précision", f"{precision*100:.1f}%")
        c3.metric("Rappel", f"{recall*100:.1f}%")
        c4.metric("F1-score", f"{f1*100:.1f}%")

        st.write("Matrice de confusion")
        st.dataframe(
            pd.DataFrame(
                cm,
                index=["Réel BON", "Réel DÉGRADÉ", "Réel CRITIQUE"],
                columns=["Prédit BON", "Prédit DÉGRADÉ", "Prédit CRITIQUE"]
            )
        )
    else:
        st.warning("Validation non disponible : données insuffisantes.")

# ────────────────────────────────────────────────────────────
# ONGLET 6 — Alertes
# ────────────────────────────────────────────────────────────
with t7:
    st.subheader("🚨 Centre d'alertes — BenguerirMaint")

    critiques = feats[feats["Niveau"]=="CRITIQUE"]
    degrades  = feats[feats["Niveau"]=="DÉGRADÉ"]
    bons      = feats[feats["Niveau"]=="BON"]

    st.markdown(f"### 🔴 {len(critiques)} convoyeur(s) CRITIQUE(S)")
    if len(critiques)==0:
        st.success("✅ Aucun convoyeur en état critique")
    for _, r in critiques.iterrows():
        st.markdown(f"""
<div class="alert-r">
  <b>🔴 {r['Convoyeur']}</b>
  — Score santé : <b>{int(r['Health_Score'])}/100</b>
  — Probabilité panne : <b>{r['Proba_Panne_%']:.0f}%</b><br>
  Nga={r['Nga_max']:.3f} | Ngv={r['Ngv_max']:.3f}
  | Temp={r['Temp_max']:.1f}°C
  | Nb pannes : {int(r['Nb_Pannes'])}<br>
  <b>→ Intervention immédiate recommandée</b>
</div>""", unsafe_allow_html=True)

    st.markdown(f"### 🟡 {len(degrades)} convoyeur(s) DÉGRADÉ(S)")
    for _, r in degrades.iterrows():
        st.markdown(f"""
<div class="alert-o">
  <b>🟡 {r['Convoyeur']}</b>
  — Score santé : <b>{int(r['Health_Score'])}/100</b>
  — Probabilité panne : <b>{r['Proba_Panne_%']:.0f}%</b><br>
  Nga={r['Nga_max']:.3f} | Ngv={r['Ngv_max']:.3f}
  | Temp={r['Temp_max']:.1f}°C<br>
  <b>→ Planifier maintenance préventive sous 30 jours</b>
</div>""", unsafe_allow_html=True)

    st.markdown(f"### 🟢 {len(bons)} convoyeur(s) en BON état")
    st.success(f"✅ {len(bons)} convoyeurs fonctionnent normalement.")

# ════════════════════════════════════════════════════════════
# ONGLET 1 — ACCUEIL (Landing Page)
# ════════════════════════════════════════════════════════════
with t1:

    # ── CSS Landing Page ─────────────────────────────────────
    st.markdown("""
    <style>
    .landing-hero {
        background: linear-gradient(135deg, #0a1628 0%, #0d2137 50%, #0a1f35 100%);
        border-radius: 20px;
        padding: 3rem 2.5rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    .landing-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 30px;
        padding: 6px 16px;
        font-size: 12px;
        color: #7dd3fc;
        margin-bottom: 1.5rem;
        font-weight: 500;
    }
    .landing-badge::before {
        content: "";
        width: 8px; height: 8px;
        border-radius: 50%;
        background: #22c55e;
        display: inline-block;
    }
    .landing-title {
        font-size: 3rem;
        font-weight: 800;
        color: white;
        line-height: 1.15;
        margin-bottom: 1rem;
        letter-spacing: -1px;
    }
    .landing-title span {
        color: #4ade80;
    }
    .landing-desc {
        font-size: 1rem;
        color: rgba(255,255,255,0.75);
        line-height: 1.75;
        max-width: 520px;
        margin-bottom: 2rem;
    }
    .btn-primary {
        display: inline-block;
        background: #00843D;
        color: white !important;
        padding: 12px 28px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 14px;
        text-decoration: none;
        margin-right: 12px;
        margin-bottom: 12px;
        border: none;
        cursor: pointer;
    }
    .btn-secondary {
        display: inline-block;
        background: transparent;
        color: white !important;
        padding: 12px 28px;
        border-radius: 30px;
        font-weight: 600;
        font-size: 14px;
        border: 1.5px solid rgba(255,255,255,0.4);
        cursor: pointer;
        margin-bottom: 12px;
    }
    .problem-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 14px;
        padding: 1.4rem;
        height: 100%;
    }
    .solution-card {
        background: rgba(0,132,61,0.15);
        border: 1px solid rgba(0,132,61,0.35);
        border-radius: 14px;
        padding: 1.4rem;
        height: 100%;
    }
    .prob-title {
        font-size: 14px;
        font-weight: 700;
        color: #f87171;
        margin-bottom: 10px;
    }
    .sol-title {
        font-size: 14px;
        font-weight: 700;
        color: #4ade80;
        margin-bottom: 10px;
    }
    .prob-item {
        font-size: 13px;
        color: rgba(255,255,255,0.75);
        padding: 5px 0;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        line-height: 1.5;
    }
    .prob-item:last-child { border: none; }
    .module-card {
        background: white;
        border-radius: 14px;
        padding: 1.2rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border-top: 3px solid #00843D;
        height: 100%;
        transition: transform 0.2s;
    }
    .module-icon {
        font-size: 1.8rem;
        margin-bottom: 8px;
        display: block;
    }
    .module-title {
        font-size: 14px;
        font-weight: 700;
        color: #1F3864;
        margin-bottom: 6px;
    }
    .module-desc {
        font-size: 12px;
        color: #6b7280;
        line-height: 1.6;
    }
    .stat-box {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
    .stat-val {
        font-size: 1.8rem;
        font-weight: 800;
        color: #4ade80;
        line-height: 1.1;
    }
    .stat-lbl {
        font-size: 11px;
        color: rgba(255,255,255,0.6);
        margin-top: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Hero Section ─────────────────────────────────────────
    nb_cv_total  = stats_p["Equipement"].nunique()
    nb_pannes_t  = len(df_p)
    nb_critiq_t  = (feats["Niveau"]=="CRITIQUE").sum()
    eco_mois     = round(df_p["Duree_h"].sum() * 0.3, 0)

    st.markdown(f"""
    <div class="landing-hero">
      <div class="landing-badge">
        Plateforme prédictive · IoT-ready · i-SENSE
      </div>
      <div class="landing-title">
        BenguerirMaint<br>
        <span>Smart Maintenance</span>
      </div>
      <div class="landing-desc">
        Anticipez les pannes, optimisez la disponibilité de vos
        convoyeurs à bande et priorisez vos interventions grâce
        à l'analyse prédictive, la surveillance vibratoire i-SENSE
        et l'Intelligence Artificielle.
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:16px;margin-bottom:2rem;">
        <div class="stat-box" style="flex:1;min-width:120px;">
          <div class="stat-val">{nb_cv_total}</div>
          <div class="stat-lbl">Convoyeurs suivis</div>
        </div>
        <div class="stat-box" style="flex:1;min-width:120px;">
          <div class="stat-val">{nb_pannes_t}</div>
          <div class="stat-lbl">Pannes analysées</div>
        </div>
        <div class="stat-box" style="flex:1;min-width:120px;">
          <div class="stat-val" style="color:#f87171;">{nb_critiq_t}</div>
          <div class="stat-lbl">En état critique</div>
        </div>
        <div class="stat-box" style="flex:1;min-width:120px;">
          <div class="stat-val">3</div>
          <div class="stat-lbl">Unités supervisées</div>
        </div>
      </div>
      <div style="font-size:12px;color:rgba(255,255,255,0.5);margin-top:1rem;">
        OCP Benguerir &nbsp;·&nbsp; Épierrage &nbsp;·&nbsp;
        Criblage &nbsp;·&nbsp; Chargement &nbsp;·&nbsp; PFE 2025-2026
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Problème vs Solution ──────────────────────────────────
    st.markdown("### Le problème & notre solution")
    col_p, col_s = st.columns(2)

    with col_p:
        st.markdown(f"""
        <div class="problem-card">
          <div class="prob-title">⚠️ Le problème industriel</div>
          <div class="prob-item">
            • Des <b>pannes imprévues</b> qui interrompent la production
            de phosphate sans avertissement
          </div>
          <div class="prob-item">
            • Une <b>priorisation aveugle</b> sans indicateur de santé
            en temps réel sur les convoyeurs
          </div>
          <div class="prob-item">
            • Des données <b>en silos</b> : GMAO et i-SENSE exploités
            séparément sans croisement intelligent
          </div>
          <div class="prob-item">
            • Un coût élevé de la <b>maintenance corrective</b> post-panne
            (urgence, délais, pièces express)
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_s:
        st.markdown(f"""
        <div class="solution-card">
          <div class="sol-title">✅ Notre solution BenguerirMaint</div>
          <div class="prob-item" style="color:rgba(255,255,255,0.8);">
            • Calcule un <b>Health Score</b> en temps réel pour
            chaque convoyeur (0 = critique, 100 = parfait)
          </div>
          <div class="prob-item" style="color:rgba(255,255,255,0.8);">
            • Prédit les pannes grâce au <b>Random Forest</b>
            combinant vibrations i-SENSE et historique
          </div>
          <div class="prob-item" style="color:rgba(255,255,255,0.8);">
            • <b>Fusionne</b> les données Excel et i-SENSE dans
            une plateforme unique et sécurisée
          </div>
          <div class="prob-item" style="color:rgba(255,255,255,0.8);">
            • Génère des <b>alertes automatiques</b> et des
            recommandations d'intervention priorisées
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Modules de l'application ─────────────────────────────
    st.markdown("---")
    st.markdown("### Les modules de BenguerirMaint")

    m1,m2,m3,m4 = st.columns(4)
    modules = [
        ("📊","Tableau de bord",
         "KPI globaux : MTBF, MTTR, Disponibilité, TRG et évolution mensuelle"),
        ("📡","Vibrations i-SENSE",
         "Analyse Nga, Ngv et Température par convoyeur avec seuils d'alerte"),
        ("🤖","IA Prédictive",
         "Random Forest : Health Score et probabilité de panne par convoyeur"),
        ("🚨","Centre d'alertes",
         "Convoyeurs critiques avec recommandations d'intervention automatiques"),
    ]
    for col, (icon, titre, desc) in zip([m1,m2,m3,m4], modules):
        col.markdown(f"""
        <div class="module-card">
          <span class="module-icon">{icon}</span>
          <div class="module-title">{titre}</div>
          <div class="module-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(" ")
    m5,m6,m7,m8 = st.columns(4)
    modules2 = [
        ("🔍","Convoyeurs",
         "Liste complète avec MTBF, MTTR, disponibilité et niveau de risque"),
        ("📈","Pareto & Analyses",
         "Analyse Pareto des causes d'arrêt — règle des 80/20"),
        ("🔧","Interventions",
         "Enregistrement et suivi des interventions terrain avec export CSV"),
        ("🔐","Sécurisé",
         "Authentification par rôle : Administrateur, Ingénieur, Technicien"),
    ]
    for col, (icon, titre, desc) in zip([m5,m6,m7,m8], modules2):
        col.markdown(f"""
        <div class="module-card">
          <span class="module-icon">{icon}</span>
          <div class="module-title">{titre}</div>
          <div class="module-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Stack technique ───────────────────────────────────────
    st.markdown("---")
    st.markdown("### Stack technique")
    t1c,t2c,t3c,t4c,t5c = st.columns(5)
    stack = [
        ("🐍","Python","Langage principal","Pandas · NumPy · Scikit-learn"),
        ("🌐","Streamlit","Interface web","Application interactive"),
        ("📊","Plotly","Graphiques","Visualisations dynamiques"),
        ("🤖","Random Forest","IA / ML","Prédiction des pannes"),
        ("📡","i-SENSE","Capteurs","Nga · Ngv · Température"),
    ]
    for col, (ico, nom, role, detail) in zip([t1c,t2c,t3c,t4c,t5c], stack):
        col.markdown(f"""
        <div style="background:#f8fafc;border-radius:10px;padding:14px;
                    text-align:center;border:1px solid #e5e7eb;">
          <div style="font-size:1.6rem;">{ico}</div>
          <div style="font-weight:700;color:#1F3864;font-size:13px;
                      margin:4px 0;">{nom}</div>
          <div style="font-size:11px;color:#00843D;font-weight:600;">{role}</div>
          <div style="font-size:11px;color:#6b7280;margin-top:2px;">{detail}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Pied de landing ───────────────────────────────────────
    st.markdown("---")
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0a1628,#0d2137);
                border-radius:14px;padding:1.5rem 2rem;
                display:flex;align-items:center;
                justify-content:space-between;flex-wrap:wrap;gap:12px;">
      <div>
        <div style="font-size:1.2rem;font-weight:800;color:white;">
          ⚙️ BenguerirMaint
        </div>
        <div style="font-size:12px;color:rgba(255,255,255,0.6);margin-top:4px;">
          PFE 2025-2026 · OCP Benguerir ·
          Épierrage · Criblage · Chargement
        </div>
      </div>
      <div style="font-size:12px;color:rgba(255,255,255,0.5);text-align:right;">
        Connecté en tant que :<br>
        <b style="color:#4ade80;">{st.session_state.nom}</b>
        — {st.session_state.role}
      </div>
    </div>
    """, unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────
# ONGLET 1 — Tableau de bord KPI
# ────────────────────────────────────────────────────────────
with t2:
    st.subheader("Indicateurs globaux du parc")

    mtbf_g  = round(sf["MTBF"].mean())
    mttr_g  = round(sf["MTTR"].mean(), 1)
    dispo_g = round(sf["Dispo_%"].mean(), 1)
    nb_cv   = sf["Equipement"].nunique()
    critiq  = (feats["Niveau"]=="CRITIQUE").sum()
    tot_arr = round(df_pf["Duree_h"].sum(), 1)

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.markdown(f'<div class="kpi"><div class="kpi-lbl">MTBF moyen</div>'
                f'<div class="kpi-val">{mtbf_g}</div>'
                f'<div class="kpi-unit">heures</div></div>',
                unsafe_allow_html=True)
    c2.markdown(f'<div class="kpi kpi-warn"><div class="kpi-lbl">MTTR moyen</div>'
                f'<div class="kpi-val kpi-val-warn">{mttr_g}</div>'
                f'<div class="kpi-unit">heures</div></div>',
                unsafe_allow_html=True)
    c3.markdown(f'<div class="kpi"><div class="kpi-lbl">Disponibilité</div>'
                f'<div class="kpi-val">{dispo_g}</div>'
                f'<div class="kpi-unit">%</div></div>',
                unsafe_allow_html=True)
    c4.markdown(f'<div class="kpi"><div class="kpi-lbl">Convoyeurs</div>'
                f'<div class="kpi-val">{nb_cv}</div>'
                f'<div class="kpi-unit">équipements</div></div>',
                unsafe_allow_html=True)
    c5.markdown(f'<div class="kpi kpi-danger"><div class="kpi-lbl">Critiques IA</div>'
                f'<div class="kpi-val kpi-val-danger">{critiq}</div>'
                f'<div class="kpi-unit">convoyeurs</div></div>',
                unsafe_allow_html=True)
    c6.markdown(f'<div class="kpi kpi-warn"><div class="kpi-lbl">Total arrêts</div>'
                f'<div class="kpi-val kpi-val-warn">{tot_arr}</div>'
                f'<div class="kpi-unit">heures</div></div>',
                unsafe_allow_html=True)

    st.markdown("---")
    g1,g2 = st.columns(2)

    with g1:
        st.markdown("**Disponibilité par sous-unité**")
        du = sf.groupby("Sous_Unite")["Dispo_%"].mean().reset_index()
        fig = px.bar(du, x="Sous_Unite", y="Dispo_%",
                     color="Dispo_%",
                     color_continuous_scale=[ROUGE, ORANGE, VERT],
                     range_color=[85,100], text="Dispo_%")
        fig.update_traces(texttemplate='%{text:.1f}%',
                          textposition='outside')
        fig.update_layout(height=300, yaxis_range=[80,102],
                          coloraxis_showscale=False,
                          xaxis_title="", yaxis_title="Disponibilité (%)")
        st.plotly_chart(fig, use_container_width=True, key='chart_13')

    with g2:
        st.markdown("**Répartition par nature d'arrêt**")
        nc = df_pf["Nature"].value_counts().reset_index()
        nc.columns = ["Nature","Nb"]
        fig2 = px.pie(nc, names="Nature", values="Nb",
                      color="Nature",
                      color_discrete_map={
                          "Mécanique":   VERT,
                          "Electrique":  ORANGE,
                          "Exploitation":"#3b82f6"
                      }, hole=0.42)
        fig2.update_layout(height=300)
        st.plotly_chart(fig2, use_container_width=True, key='chart_14')

    if "Date" in df_pf.columns and df_pf["Date"].notna().any():
        st.markdown("**Évolution des pannes par mois**")
        ev = df_pf.groupby(df_pf["Date"].dt.to_period("M")).agg(
            Nb=("Duree_h","count"),
            Dur=("Duree_h","sum")
        ).reset_index()
        ev["Date"] = ev["Date"].astype(str)
        fig3 = px.line(ev, x="Date", y="Nb",
                       markers=True,
                       color_discrete_sequence=[VERT],
                       title="Nombre de pannes par mois")
        fig3.update_layout(height=260,
                           xaxis_title="Mois",
                           yaxis_title="Nb pannes")
        st.plotly_chart(fig3, use_container_width=True, key='chart_15')

# ────────────────────────────────────────────────────────────
# ONGLET 2 — Convoyeurs
# ────────────────────────────────────────────────────────────
with t3:
    st.subheader(f"Parc convoyeurs — {len(sf)} équipements")

    def badge(n):
        if n=="CRITIQUE": return "🔴 CRITIQUE"
        if n=="DÉGRADÉ":  return "🟡 DÉGRADÉ"
        return "🟢 BON"

    # Fusionner stats pannes + IA
    sf2 = sf.merge(
        feats[["Convoyeur","Health_Score","Niveau","Proba_Panne_%"]],
        left_on="Equipement", right_on="Convoyeur", how="left"
    )
    sf2["Health_Score"] = sf2["Health_Score"].fillna(75)
    sf2["Niveau"]       = sf2["Niveau"].fillna("BON")
    sf2["Proba_Panne_%"]= sf2["Proba_Panne_%"].fillna(25)

    aff = sf2[[
        "Sous_Unite","Equipement","Nb_Pannes",
        "MTBF","MTTR","Dispo_%",
        "Health_Score","Proba_Panne_%","Niveau"
    ]].copy()
    aff["Niveau"] = aff["Niveau"].apply(badge)
    aff = aff.rename(columns={
        "Sous_Unite":    "Sous-unité",
        "Nb_Pannes":     "Nb Pannes",
        "Dispo_%":       "Dispo %",
        "Health_Score":  "Score Santé /100",
        "Proba_Panne_%": "Proba Panne %"
    })
    st.dataframe(aff.sort_values("Score Santé /100"),
                 use_container_width=True, height=400)

    st.markdown("**MTBF vs MTTR par convoyeur**")
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(x=sf["Equipement"], y=sf["MTBF"],
                          name="MTBF", marker_color=VERT))
    fig4.add_trace(go.Bar(x=sf["Equipement"], y=sf["MTTR"],
                          name="MTTR", marker_color=ORANGE))
    fig4.update_layout(barmode="group", height=300,
                       xaxis_title="Equipement",
                       yaxis_title="Heures")
    st.plotly_chart(fig4, use_container_width=True, key='chart_16')

# ────────────────────────────────────────────────────────────
# ONGLET 3 — Pareto
# ────────────────────────────────────────────────────────────
with t4:
    st.markdown("### Pareto des descriptions d'arrêt")
    par = df_pf["Description"].value_counts().reset_index()
    par.columns = ["Description","Nb"]
    par["Cum_%"] = (par["Nb"].cumsum()/par["Nb"].sum()*100).round(1)

    fig5 = go.Figure()
    fig5.add_trace(go.Bar(x=par["Description"], y=par["Nb"],
                          name="Nb pannes", marker_color=VERT))
    fig5.add_trace(go.Scatter(x=par["Description"], y=par["Cum_%"],
                              name="% cumulé", yaxis="y2",
                              line=dict(color=ORANGE, width=2.5),
                              mode="lines+markers"))
    fig5.add_hline(y=80, line_dash="dash", line_color=ROUGE,
                   yref="y2", annotation_text="Seuil 80%")
    fig5.update_layout(
        yaxis =dict(title="Nombre de pannes"),
        yaxis2=dict(title="% cumulé", overlaying="y",
                    side="right", range=[0,105]),
        height=380, legend=dict(orientation="h", y=-0.25),
        title="Pareto des arrêts — BenguerirMaint"
    )
    st.plotly_chart(fig5, use_container_width=True, key='chart_17')

    c1,c2 = st.columns(2)
    with c1:
        st.markdown("**Durée totale par équipement**")
        fig6 = px.bar(
            sf.sort_values("Duree_tot", ascending=False),
            x="Equipement", y="Duree_tot",
            color="Sous_Unite",
            color_discrete_sequence=[VERT, ORANGE, "#3b82f6"],
            title="Heures d'arrêt cumulées"
        )
        fig6.update_layout(height=300)
        st.plotly_chart(fig6, use_container_width=True, key='chart_18')

    with c2:
        st.markdown("**Pareto par nature d'arrêt**")
        nat = df_pf.groupby("Nature")["Duree_h"].sum().reset_index()
        nat = nat.sort_values("Duree_h", ascending=False)
        fig7 = px.bar(nat, x="Nature", y="Duree_h",
                      color="Nature",
                      color_discrete_map={
                          "Mécanique":   VERT,
                          "Electrique":  ORANGE,
                          "Exploitation":"#3b82f6"
                      },
                      title="Durée totale par nature (h)")
        fig7.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig7, use_container_width=True, key='chart_19')

# ────────────────────────────────────────────────────────────
# ONGLET 4 — Vibrations i-SENSE
# ────────────────────────────────────────────────────────────
with t5:
    st.subheader("Analyse vibratoire — i-SENSE")

    with st.expander("📖 Légende i-SENSE", expanded=False):
        col1,col2,col3 = st.columns(3)
        col1.info("**Nga** — Niveau Global Accélération\nChocs & défauts roulements\nSeuil critique : > 0.1")
        col2.warning("**Ngv** — Niveau Global Vibration\nUsure générale\nSeuil critique : > 0.3")
        col3.error("**Temp** — Température °C\nEchauffement\nSeuil critique : > 80°C")

    nga_max = df_i["Nga"].max()
    ngv_max = df_i["Ngv"].max()
    nb_crit = (feats["Niveau"]=="CRITIQUE").sum()

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Nga max", f"{nga_max:.3f}",
              delta="⚠️ Critique" if nga_max>0.1 else "✅ Normal")
    c2.metric("Ngv max", f"{ngv_max:.3f}",
              delta="⚠️ Critique" if ngv_max>0.3 else "✅ Normal")
    c3.metric("Temp max",
              f"{df_i['Temperature'].max():.1f}°C")
    c4.metric("Capteurs critiques", nb_crit)

    st.markdown("---")
    g1,g2 = st.columns(2)

    with g1:
        st.markdown("**Ngv max par convoyeur**")
        ngv_c = df_i.groupby("Convoyeur")["Ngv"].max().reset_index()
        ngv_c = ngv_c.sort_values("Ngv", ascending=False)
        cols_c = [ROUGE if v>0.3 else ORANGE if v>0.15 else VERT
                  for v in ngv_c["Ngv"]]
        fig8 = go.Figure(go.Bar(
            x=ngv_c["Convoyeur"], y=ngv_c["Ngv"],
            marker_color=cols_c,
            text=ngv_c["Ngv"].round(3), textposition="outside"
        ))
        fig8.add_hline(y=0.3, line_dash="dash", line_color=ROUGE,
                       annotation_text="Seuil critique")
        fig8.add_hline(y=0.15, line_dash="dash", line_color=ORANGE,
                       annotation_text="Seuil dégradé")
        fig8.update_layout(height=320, xaxis_title="Convoyeur",
                           yaxis_title="Ngv (mm/s)")
        st.plotly_chart(fig8, use_container_width=True, key='chart_20')

    with g2:
        st.markdown("**Température max par convoyeur**")
        tmp = df_i.dropna(subset=["Temperature"])
        tmp = tmp.groupby("Convoyeur")["Temperature"].max().reset_index()
        tmp = tmp.sort_values("Temperature", ascending=False)
        cols_t = [ROUGE if t>80 else ORANGE if t>60 else VERT
                  for t in tmp["Temperature"]]
        fig9 = go.Figure(go.Bar(
            x=tmp["Convoyeur"], y=tmp["Temperature"],
            marker_color=cols_t,
            text=tmp["Temperature"].round(1), textposition="outside"
        ))
        fig9.add_hline(y=80, line_dash="dash", line_color=ROUGE,
                       annotation_text="Seuil critique 80°C")
        fig9.update_layout(height=320, xaxis_title="Convoyeur",
                           yaxis_title="Température (°C)")
        st.plotly_chart(fig9, use_container_width=True, key='chart_21')

    st.markdown("**Évolution vibratoire dans le temps**")
    cv_sel = st.selectbox("Choisir un convoyeur",
                          df_i["Convoyeur"].unique(), key="cv_vib2")
    df_sel = df_i[df_i["Convoyeur"]==cv_sel]
    ngv_t  = df_sel.groupby("Date")["Ngv"].max().reset_index()

    fig10 = go.Figure()
    fig10.add_trace(go.Scatter(
        x=ngv_t["Date"], y=ngv_t["Ngv"],
        mode="lines+markers",
        line=dict(color=VERT, width=2), name="Ngv"
    ))
    fig10.add_hrect(y0=0.15, y1=ngv_t["Ngv"].max()*1.1,
                    fillcolor=ROUGE, opacity=0.07, line_width=0)
    fig10.add_hline(y=0.3, line_dash="dash", line_color=ROUGE,
                    annotation_text="Seuil critique")
    fig10.add_hline(y=0.15, line_dash="dash", line_color=ORANGE,
                    annotation_text="Seuil dégradé")
    fig10.update_layout(height=280,
                        title=f"Évolution Ngv — {cv_sel}",
                        yaxis_title="Ngv", xaxis_title="Date")
    st.plotly_chart(fig10, use_container_width=True, key='chart_22')

# ────────────────────────────────────────────────────────────
# ONGLET 5 — IA Prédictive
# ────────────────────────────────────────────────────────────
with t6:
    st.subheader("🤖 Maintenance Prédictive — Random Forest")

    st.info("""
    **Comment fonctionne l'IA ?**
    Le modèle Random Forest analyse 6 indicateurs pour chaque convoyeur :
    Nga max, Ngv max, Température max, Nga moyen, Ngv moyen, Nb pannes historiques.
    Il calcule ensuite un **Health Score** (0-100) et une **probabilité de panne**.
    """)

    c1,c2,c3 = st.columns(3)
    c1.metric("Convoyeurs analysés", len(feats))
    c2.metric("Score santé moyen",
              f"{feats['Health_Score'].mean():.0f}/100")
    c3.metric("En état critique",
              (feats["Niveau"]=="CRITIQUE").sum())

    st.markdown("---")
    st.markdown("**Health Score et probabilité de panne**")

    ft_tri = feats.sort_values("Health_Score")
    cols_h = [ROUGE if s<40 else ORANGE if s<65 else VERT
              for s in ft_tri["Health_Score"]]
    fig11 = go.Figure()
    fig11.add_trace(go.Bar(
        x=ft_tri["Convoyeur"],
        y=ft_tri["Health_Score"],
        marker_color=cols_h,
        text=ft_tri["Health_Score"].astype(int),
        textposition="outside", name="Health Score"
    ))
    fig11.add_hline(y=40, line_dash="dash", line_color=ROUGE,
                    annotation_text="Seuil critique")
    fig11.add_hline(y=65, line_dash="dash", line_color=ORANGE,
                    annotation_text="Seuil dégradé")
    fig11.update_layout(height=320, yaxis_range=[0,115],
                        yaxis_title="Health Score /100",
                        xaxis_title="Convoyeur",
                        title="Health Score — BenguerirMaint IA")
    st.plotly_chart(fig11, use_container_width=True, key='chart_23')

    st.markdown("**Tableau complet des prédictions**")
    aff_ia = feats[[
        "Convoyeur","Nga_max","Ngv_max","Temp_max",
        "Nb_Pannes","Health_Score","Proba_Panne_%","Niveau"
    ]].copy()
    aff_ia["Niveau"] = aff_ia["Niveau"].apply(
        lambda n: "🔴 CRITIQUE" if n=="CRITIQUE"
                  else "🟡 DÉGRADÉ" if n=="DÉGRADÉ" else "🟢 BON"
    )
    aff_ia = aff_ia.rename(columns={
        "Nga_max":"Nga Max",
        "Ngv_max":"Ngv Max",
        "Temp_max":"Temp Max °C",
        "Nb_Pannes":"Nb Pannes",
        "Health_Score":"Score /100",
        "Proba_Panne_%":"Proba Panne %"
    })
    st.dataframe(aff_ia.sort_values("Score /100"),
                 use_container_width=True, height=350)

    # Importance des variables
    st.markdown("**Importance des variables pour l'IA**")
    if len(y.unique()) > 1:
        importances = rf.feature_importances_
        imp_df = pd.DataFrame({
            "Variable": ["Nga max","Nga moyen","Ngv max",
                         "Ngv moyen","Temp max","Nb pannes"],
            "Importance": importances
        }).sort_values("Importance", ascending=True)
        fig12 = px.bar(imp_df, x="Importance", y="Variable",
                       orientation="h",
                       color="Importance",
                       color_continuous_scale=[ORANGE, VERT],
                       title="Quels capteurs influencent le plus la prédiction ?")
        fig12.update_layout(height=280,
                            coloraxis_showscale=False)
        st.plotly_chart(fig12, use_container_width=True, key='chart_rf_old')
        st.markdown("---")
        st.subheader("Validation du modèle Random Forest")

    if validation_ok:

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Accuracy", f"{accuracy*100:.1f}%")
        c2.metric("Précision", f"{precision*100:.1f}%")
        c3.metric("Rappel", f"{recall*100:.1f}%")
        c4.metric("F1-score", f"{f1*100:.1f}%")

        st.write("Matrice de confusion")

        st.dataframe(
            pd.DataFrame(
                cm,
                index=["Réel BON", "Réel DÉGRADÉ", "Réel CRITIQUE"],
                columns=["Prédit BON", "Prédit DÉGRADÉ", "Prédit CRITIQUE"]
            )
        )

    else:
        st.warning("Validation non disponible")

st.subheader("Validation du modèle Random Forest")

if validation_ok:
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Accuracy", f"{accuracy*100:.1f}%")
    c2.metric("Précision", f"{precision*100:.1f}%")
    c3.metric("Rappel", f"{recall*100:.1f}%")
    c4.metric("F1-score", f"{f1*100:.1f}%")

    st.write("Matrice de confusion")
    st.dataframe(
        pd.DataFrame(
            cm,
            index=["Réel BON", "Réel DÉGRADÉ", "Réel CRITIQUE"],
            columns=["Prédit BON", "Prédit DÉGRADÉ", "Prédit CRITIQUE"]
        )
    )
else:
    st.warning("Validation non disponible : données insuffisantes.")
# ────────────────────────────────────────────────────────────
# ONGLET 6 — Alertes
# ────────────────────────────────────────────────────────────
with t7:
    st.subheader("🚨 Centre d'alertes — BenguerirMaint")

    critiques = feats[feats["Niveau"]=="CRITIQUE"]
    degrades  = feats[feats["Niveau"]=="DÉGRADÉ"]
    bons      = feats[feats["Niveau"]=="BON"]

    st.markdown(f"### 🔴 {len(critiques)} convoyeur(s) CRITIQUE(S)")
    if len(critiques)==0:
        st.success("✅ Aucun convoyeur en état critique")
    for _, r in critiques.iterrows():
        st.markdown(f"""
<div class="alert-r">
  <b>🔴 {r['Convoyeur']}</b>
  — Score santé : <b>{int(r['Health_Score'])}/100</b>
  — Probabilité panne : <b>{r['Proba_Panne_%']:.0f}%</b><br>
  Nga={r['Nga_max']:.3f} | Ngv={r['Ngv_max']:.3f}
  | Temp={r['Temp_max']:.1f}°C
  | Nb pannes : {int(r['Nb_Pannes'])}<br>
  <b>→ Intervention immédiate recommandée</b>
</div>""", unsafe_allow_html=True)

    st.markdown(f"### 🟡 {len(degrades)} convoyeur(s) DÉGRADÉ(S)")
    for _, r in degrades.iterrows():
        st.markdown(f"""
<div class="alert-o">
  <b>🟡 {r['Convoyeur']}</b>
  — Score santé : <b>{int(r['Health_Score'])}/100</b>
  — Probabilité panne : <b>{r['Proba_Panne_%']:.0f}%</b><br>
  Nga={r['Nga_max']:.3f} | Ngv={r['Ngv_max']:.3f}
  | Temp={r['Temp_max']:.1f}°C<br>
  <b>→ Planifier maintenance préventive sous 30 jours</b>
</div>""", unsafe_allow_html=True)

    st.markdown(f"### 🟢 {len(bons)} convoyeur(s) en BON état")
    st.success(f"✅ {len(bons)} convoyeurs fonctionnent normalement.")

# ════════════════════════════════════════════════════════════
# ONGLET 1 — ACCUEIL
# ════════════════════════════════════════════════════════════
with t1:
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,{VERT},#005a2b);
                padding:2rem;border-radius:16px;color:white;margin-bottom:1.5rem;">
      <div style="font-size:2rem;font-weight:800;margin-bottom:8px;">
        ⚙️ BenguerirMaint
      </div>
      <div style="font-size:1rem;opacity:0.9;line-height:1.7;">
        Plateforme de maintenance prédictive intelligente<br>
        <b>OCP Benguerir</b> — Installations fixes de convoyage<br>
        Épierrage · Criblage · Chargement
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(f"""
        <div style="background:white;border-radius:12px;padding:1.4rem;
                    border-left:4px solid {VERT};
                    box-shadow:0 2px 8px rgba(0,0,0,0.07);margin-bottom:1rem;">
          <div style="font-size:1rem;font-weight:700;color:{VERT};margin-bottom:10px;">
            🎯 Objectifs du projet
          </div>
          <div style="font-size:13px;color:#374151;line-height:1.8;">
            ✅ Analyser la fiabilité des convoyeurs à bande<br>
            ✅ Identifier les équipements critiques (AMDEC)<br>
            ✅ Calculer MTBF, MTTR et disponibilité<br>
            ✅ Intégrer la surveillance vibratoire i-SENSE<br>
            ✅ Prédire les pannes par Intelligence Artificielle<br>
            ✅ Proposer un plan de maintenance optimisé
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:white;border-radius:12px;padding:1.4rem;
                    border-left:4px solid {ORANGE};
                    box-shadow:0 2px 8px rgba(0,0,0,0.07);margin-bottom:1rem;">
          <div style="font-size:1rem;font-weight:700;color:{ORANGE};margin-bottom:10px;">
            🏭 Site étudié
          </div>
          <div style="font-size:13px;color:#374151;line-height:1.8;">
            <b>Site :</b> OCP Benguerir — Maroc<br>
            <b>Unité 1 :</b> Épierrage<br>
            <b>Unité 2 :</b> Criblage<br>
            <b>Unité 3 :</b> Chargement<br>
            <b>Équipements :</b> Convoyeurs à bande (CVB)<br>
            <b>Période :</b> 2024 – 2025
          </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div style="background:white;border-radius:12px;padding:1.4rem;
                    border-left:4px solid #3b82f6;
                    box-shadow:0 2px 8px rgba(0,0,0,0.07);margin-bottom:1rem;">
          <div style="font-size:1rem;font-weight:700;color:#1d4ed8;margin-bottom:10px;">
            🔧 Technologies utilisées
          </div>
          <div style="font-size:13px;color:#374151;line-height:1.8;">
            <b>Python</b> — Pandas, NumPy, Scikit-learn<br>
            <b>Streamlit</b> — Interface web interactive<br>
            <b>Plotly</b> — Graphiques dynamiques<br>
            <b>Power BI</b> — Dashboard KPI<br>
            <b>i-SENSE</b> — Surveillance vibratoire<br>
            <b>Random Forest</b> — Algorithme IA
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:white;border-radius:12px;padding:1.4rem;
                    border-left:4px solid {VERT};
                    box-shadow:0 2px 8px rgba(0,0,0,0.07);margin-bottom:1rem;">
          <div style="font-size:1rem;font-weight:700;color:{VERT};margin-bottom:10px;">
            📊 Modules de l'application
          </div>
          <div style="font-size:13px;color:#374151;line-height:1.8;">
            📊 <b>Tableau de bord</b> — KPI globaux<br>
            🔍 <b>Convoyeurs</b> — État individuel<br>
            📈 <b>Pareto</b> — Causes dominantes<br>
            📡 <b>Vibrations</b> — Données i-SENSE<br>
            🤖 <b>IA Prédictive</b> — Health Score<br>
            🚨 <b>Alertes</b> — Interventions urgentes<br>
            🔧 <b>Interventions</b> — Suivi terrain
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📋 Données sources")
    d1, d2 = st.columns(2)
    with d1:
        st.info("""
        **📂 Fichier 1 — Historique des arrêts**
        - Sous-unité, DATE, Equipement
        - Description de l'arrêt
        - Début, Fin, Durée, Nature
        """)
    with d2:
        st.info("""
        **📡 Fichier 2 — Rapport i-SENSE**
        - Date, Convoyeur, Organe
        - Nga (Acc.) — vibration accélération
        - Ngv (Vit.) — vibration vitesse
        - Temp (°C) — température composant
        """)

    st.markdown("---")
    st.markdown("### 👥 Équipe projet")
    e1, e2, e3 = st.columns(3)
    e1.markdown(f"""
    <div style="text-align:center;padding:1rem;background:white;
                border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,0.07);">
      <div style="font-size:2rem;">👨‍🎓</div>
      <div style="font-weight:600;color:{BLEU if False else VERT};">[ASSYA EL BADAOUI]</div>
      <div style="font-size:12px;color:#6b7280;">Étudiant PFE</div>
    </div>
    """, unsafe_allow_html=True)
    e2.markdown(f"""
    <div style="text-align:center;padding:1rem;background:white;
                border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,0.07);">
      <div style="font-size:2rem;">👨‍💼</div>
      <div style="font-weight:600;color:{VERT};">[IMAD EL HARRAKI]</div>
      <div style="font-size:12px;color:#6b7280;">Encadrant académique</div>
    </div>
    """, unsafe_allow_html=True)
    e3.markdown(f"""
    <div style="text-align:center;padding:1rem;background:white;
                border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,0.07);">
      <div style="font-size:2rem;">🏭</div>
      <div style="font-weight:600;color:{VERT};">[JAWAD FATIH]</div>
      <div style="font-size:12px;color:#6b7280;">Encadrant industriel</div>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# ONGLET 8 — INTERVENTIONS ET HISTORIQUE
# ════════════════════════════════════════════════════════════
with t8:
    st.subheader("🔧 Gestion des interventions")

    tab_new, tab_hist = st.tabs([
        "➕ Nouvelle intervention",
        "📋 Historique des interventions"
    ])

    # ── Formulaire nouvelle intervention ────────────────────
    with tab_new:
        st.markdown("### Enregistrer une intervention")

        c1, c2 = st.columns(2)
        with c1:
            conv_list = sorted(df_p["Equipement"].dropna().unique().tolist())
            conv_sel  = st.selectbox("🏭 Convoyeur", conv_list)
            type_int  = st.selectbox("🔧 Type d'intervention", [
                "Maintenance préventive",
                "Maintenance corrective",
                "Inspection vibratoire",
                "Remplacement bande",
                "Remplacement rouleau",
                "Remplacement roulement",
                "Réglage alignement",
                "Nettoyage",
                "Autre"
            ])
            priorite  = st.selectbox("⚡ Priorité", [
                "P1 — Urgent",
                "P2 — Important",
                "P3 — Planifié",
                "P4 — Surveillance"
            ])
        with c2:
            technicien = st.text_input("👤 Technicien responsable",
                                        placeholder="Nom du technicien")
            date_int   = st.date_input("📅 Date d'intervention")
            duree_int  = st.number_input("⏱️ Durée (heures)",
                                          min_value=0.0, max_value=24.0,
                                          value=1.0, step=0.5)
            statut     = st.selectbox("📌 Statut", [
                "Planifiée",
                "En cours",
                "Terminée",
                "Annulée"
            ])

        pieces = st.text_input("🔩 Pièces utilisées",
                                placeholder="Ex: Roulement SKF 6205, Bande EP400...")
        commentaire = st.text_area("📝 Commentaire / Observations",
                                    placeholder="Décrire l'intervention réalisée...",
                                    height=100)

        if st.button("💾 Enregistrer l'intervention",
                     use_container_width=True, type="primary"):
            if technicien.strip() == "":
                st.error("❌ Veuillez renseigner le nom du technicien")
            else:
                nouvelle = {
                    "Date":         str(date_int),
                    "Convoyeur":    conv_sel,
                    "Type":         type_int,
                    "Priorité":     priorite,
                    "Technicien":   technicien,
                    "Durée (h)":    duree_int,
                    "Statut":       statut,
                    "Pièces":       pieces,
                    "Commentaire":  commentaire,
                    "Enregistré par": st.session_state.nom,
                }
                st.session_state.interventions.append(nouvelle)
                st.success(f"✅ Intervention enregistrée pour {conv_sel} "
                           f"par {technicien} !")
                st.balloons()

    # ── Historique ──────────────────────────────────────────
    with tab_hist:
        st.markdown("### 📋 Historique des interventions enregistrées")

        if len(st.session_state.interventions) == 0:
            st.info("Aucune intervention enregistrée pour l'instant. "
                    "Utilisez l'onglet 'Nouvelle intervention' pour en ajouter.")
        else:
            df_int = pd.DataFrame(st.session_state.interventions)

            # ── KPI interventions ────────────────────────────
            ki1, ki2, ki3, ki4 = st.columns(4)
            ki1.metric("Total interventions",   len(df_int))
            ki2.metric("Terminées",
                       (df_int["Statut"]=="Terminée").sum())
            ki3.metric("En cours",
                       (df_int["Statut"]=="En cours").sum())
            ki4.metric("Planifiées",
                       (df_int["Statut"]=="Planifiée").sum())

            st.markdown("---")

            # ── Filtres ──────────────────────────────────────
            fc1, fc2, fc3 = st.columns(3)
            f_cv  = fc1.selectbox("Filtrer convoyeur",
                                   ["Tous"] + sorted(df_int["Convoyeur"].unique().tolist()))
            f_st  = fc2.selectbox("Filtrer statut",
                                   ["Tous"] + sorted(df_int["Statut"].unique().tolist()))
            f_pr  = fc3.selectbox("Filtrer priorité",
                                   ["Tous"] + sorted(df_int["Priorité"].unique().tolist()))

            df_filt = df_int.copy()
            if f_cv != "Tous": df_filt = df_filt[df_filt["Convoyeur"]==f_cv]
            if f_st != "Tous": df_filt = df_filt[df_filt["Statut"]==f_st]
            if f_pr != "Tous": df_filt = df_filt[df_filt["Priorité"]==f_pr]

            # ── Tableau ──────────────────────────────────────
            def colorier_statut(val):
                if val == "Terminée":   return "background-color:#dcfce7"
                if val == "En cours":   return "background-color:#fff7ed"
                if val == "Planifiée":  return "background-color:#dbeafe"
                if val == "Annulée":    return "background-color:#fee2e2"
                return ""

            st.dataframe(
                df_filt.style.applymap(
                    colorier_statut, subset=["Statut"]
                ),
                use_container_width=True,
                height=350
            )

            # ── Export CSV ───────────────────────────────────
            csv = df_filt.to_csv(index=False, encoding="utf-8-sig")
            st.download_button(
                "📥 Télécharger l'historique (CSV)",
                data=csv,
                file_name="historique_interventions_BenguerirMaint.csv",
                mime="text/csv",
                use_container_width=True
            )

            # ── Graphique interventions par convoyeur ────────
            if len(df_int) > 1:
                st.markdown("**Interventions par convoyeur**")
                cnt = df_int["Convoyeur"].value_counts().reset_index()
                cnt.columns = ["Convoyeur","Nb"]
                fig_int = px.bar(cnt, x="Convoyeur", y="Nb",
                                 color="Nb",
                                 color_continuous_scale=[VERT, ORANGE],
                                 title="Nombre d'interventions par convoyeur")
                fig_int.update_layout(height=280,
                                      coloraxis_showscale=False)
                st.plotly_chart(fig_int, use_container_width=True, key='chart_25')

# ─── Pied de page ────────────────────────────────────────────
st.markdown(f"""
<footer>
  ⚙️ <b>BenguerirMaint</b> — PFE 2025-2026 &nbsp;·&nbsp;
  OCP Benguerir &nbsp;·&nbsp;
  Pannes · Vibrations i-SENSE · Random Forest IA &nbsp;·&nbsp;
  Épierrage · Criblage · Chargement
</footer>
""", unsafe_allow_html=True)
