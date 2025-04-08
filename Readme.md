# 🧠 Q-Learning - Agent in GridWorld

Une démonstration interactive de l'algorithme **Q-learning** appliqué à un environnement simplifié de type GridWorld, le tout visualisé avec **Streamlit**.

---

## 🚀 Présentation

Ce projet propose une **interface web interactive** permettant de visualiser les déplacements d’un agent dans une grille 4x3 avec :

- Une cellule **objectif** (but)
- Une cellule **danger**
- Une cellule **mur** (obstacle)
- Une **Q-table** visualisée avec des couleurs pour chaque action possible
- Des **commandes manuelles** de déplacement de l’agent
- Un affichage en **temps réel** via PIL (Python Imaging Library)

L’objectif est d’expérimenter les concepts fondamentaux de l’**apprentissage par renforcement** sans avoir recours à une boucle d’apprentissage automatique complexe.

---

## 🗂️ Structure du projet

```
Q-learning/
├── Q-learning.py         # Script principal Streamlit
├── agent.py              # Logique de déplacement et affichage de l'agent
├── environement.py       # Environnement GridWorld avec rendu de la Q-table
├── requirements.txt      # Dépendances Python
└── README.md             # Ce fichier
```

---

## ⚙️ Fonctionnalités

- 🔼🔽🔽🔁 Déplacement manuel de l’agent (via boutons Streamlit)
- 🧠 Visualisation des **Q-values** sous forme de triangles colorés
- 🎯 Grille 4x3 avec positions spéciales :
  - ✅ But : cellule verte
  - ❌ Danger : cellule rouge
  - ⬛ Mur : cellule grise
- ♻️ **Reset** de la position de l’agent
- 🧭 Option "Code Movement" pour lancer une séquence de mouvements automatisés
- 💾 Q-table stockée dans la session Streamlit (`st.session_state`)

---

## 🧪 Installation & Lancement

### Prérequis

- Python 3.7+
- pip

### Installation

```bash
git clone https://github.com/ton-utilisateur/Q-learning.git
cd Q-learning
pip install -r requirements.txt
```

### Lancement de l'app Streamlit

```bash
streamlit run Q-learning.py
```

---

## 📦 Requirements (exemple)

```txt
streamlit
Pillow
```

*(Ajoute ici les autres dépendances si tu en ajoutes plus tard)*

---

## 📚 Concepts pédagogiques

Ce projet met en avant :

- La **Q-table** comme représentation de la politique de l’agent
- La **visualisation des actions** avec des triangles colorés :
  - 🔴 valeurs Q négatives
  - 🟢 valeurs Q positives
- La **prise de décision de l’agent** selon les valeurs Q (à étendre)
- La structure typique d’un environnement pour **apprentissage par renforcement**

---

## 🛠️ Prochaines évolutions possibles

- Implémentation d’une vraie **boucle d’apprentissage Q-Learning**
- Ajout de la **politique ε-greedy**
- Affichage de l’évolution de la Q-table au fil du temps
- Historique des épisodes / récompenses
- Sauvegarde / chargement de la Q-table

---

## 🙌 Auteur

**Kévin Duranty**  
Ingénieur IA | Passionné par l’apprentissage par renforcement, TensorFlow, Docker & Streamlit.