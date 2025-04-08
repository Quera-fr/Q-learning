from agent import *
from environement import *

st.set_page_config(layout="centered")
# --- Interface Streamlit ---
st.title("Q-Learning - Agent in GridWorld")

# Position du tableau
placeholder = st.empty()

# Création de l'agent et du tableau
gw = GridWorld()
agent = Agent(0, 0, gw, placeholder)


# Boutons pour déplacer l'agent
c1, c2, c3, c4 = st.columns(4)

if c1.button("↑ Up"):
    agent.move_agent("up")

if c2.button("← Left"):  
    agent.move_agent("left")

if c3.button("→ Right"):
    agent.move_agent("right")

if c4.button("↓ Down"):
    agent.move_agent("down")

    

# Bouton Reset
if st.sidebar.button("Reset Position"):
    gw.reset_position()
    gw.dessiner_grille(placeholder)


if st.sidebar.button("Code movement"):
    gw.reset_position()
    gw.dessiner_grille(placeholder)

    for _ in range(3):
        # On “suspend” le script pour 2 secondes pour donner le temps de voir la position
        time.sleep(2)
        agent.move_agent("right")