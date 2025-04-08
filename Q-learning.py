from agent import *
from environement import *


# --- Interface Streamlit ---
st.set_page_config(layout="centered")
st.title("Q-Learning - Agent in GridWorld")


# Position du tableau
placeholder = st.empty()

# Création de l'agent et du tableau
gw = GridWorld()
agent = Agent(0, 0, gw, placeholder)


# Boutons pour déplacer l'agent
c1, c2, c3, c4 = st.columns(4)

if c1.button("↑ Up"): agent.move_agent("up")
if c2.button("← Left"): agent.move_agent("left")
if c3.button("→ Right"): agent.move_agent("right")
if c4.button("↓ Down"): agent.move_agent("down")


# Bouton Reset
if st.sidebar.button("Reset Position"): gw.reset_position(placeholder)

# Bouton Reset all value
if st.sidebar.button("Reset all values"):
    del st.session_state.Q, gw, agent, st.session_state.agent_pos
    gw = GridWorld()
    agent = Agent(0, 0, gw, placeholder)


sleep_time = st.sidebar.slider("Speed step in second", 0.0, 2.0)

if st.sidebar.button("Code movement"):
    gw.reset_position(placeholder)

    for _ in range(3):
        # st.session_state.Q[x][y][a] 
        # a : 0=up, 1=down, 2=left, 3=right

        st.session_state.Q[_][0][2]+=1
        
        # On “suspend” le script pour 2 secondes pour donner le temps de voir la position
        time.sleep(sleep_time)
        agent.move_agent("right")


