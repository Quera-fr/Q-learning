from agent import *
from environement import *
from training import epsilon_greedy_choice

# --- Interface Streamlit ---
st.set_page_config(layout="centered")
st.title("Q-Learning - Agent in GridWorld")

col1, col2, col3 = st.columns(3)

with col1 : alpha = st.slider("Learning rate", 0.0, 1.0, 0.50)
with col2 : gama = st.slider("gama", 0.0, 1.0, 0.20)
with col3 : epsilon = st.slider("epsilon", 0.0, 1.0, 0.4)


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


sleep_time = st.sidebar.slider("Speed step in second", 0.0, 2.0, 0.5)
n_episodes = st.sidebar.slider("N episode", 0, 20, 10)


if st.sidebar.button("Code movement"):
    for episode in range(n_episodes):
        gw.reset_position(placeholder)
        while st.session_state.agent_pos != gw.goal_pos:
            x, y = st.session_state.agent_pos
            # st.session_state.Q[x][y][a] 
            # a : 0=up, 1=down, 2=left, 3=right
            dict_actions = {
                                0:'up', 
                                1:'down', 
                                2:'left', 
                                3:'right'
                            }

            
            # On “suspend” le script pour 2 secondes pour donner le temps de voir la position
            time.sleep(sleep_time)
            
            Q_a_s = st.session_state.Q[x][y]

            actions = epsilon_greedy_choice(Q_a_s, epsilon)

            if agent.move_agent(dict_actions[actions]):
                x_next, y_next = st.session_state.agent_pos

                Q_a_s_next = st.session_state.Q[x_next][y_next]

                # Q(s,a) ← Q(s,a) + α[r + γmaxQ(s′,a′) − Q(s,a)] (à compléter)
                st.session_state.Q[x][y][actions] = Q_a_s[actions] + alpha * (st.session_state.R[x_next][y_next] \
                                                                            + gama * max(Q_a_s_next) - Q_a_s[actions])

                gw.dessiner_grille(placeholder)