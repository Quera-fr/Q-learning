from agent import *
from environement import *
from training import *
import numpy as np
import pandas as pd
import random
import time

# --- Interface Streamlit ---
st.set_page_config(layout="centered")
st.title("Q-Learning - Agent in GridWorld")

col1, col2, col3 = st.columns(3)

# Position du tableau
placeholder = st.empty()


with col1 : alpha = st.slider("Learning rate", 0.0, 1.0, 0.50)
with col2 : gama = st.slider("gama", 0.0, 1.0, 0.20)
with col3 : epsilon = st.slider("epsilon", 0.0, 1.0, 0.4)

if st.sidebar.checkbox("Set up grid size"):

    try:
        del st.session_state.Q, gw, agent, st.session_state.agent_pos
    except:
        pass
    width = st.sidebar.number_input("Width", 1, 10, 4)
    height = st.sidebar.number_input("Height", 1, 10, 3)
    goal_pos_x = st.sidebar.number_input("Goal position x", 0, width-1, 3)
    goal_pos_y = st.sidebar.number_input("Goal position y", 0, height-1, 2)
    wall_pos_x = st.sidebar.number_input("Wall position x", 0, width-1, 1)
    wall_pos_y = st.sidebar.number_input("Wall position y", 0, height-1, 1)
    danger_pos_x = st.sidebar.number_input("Danger position x", 0, width-1, 3)
    danger_pos_y = st.sidebar.number_input("Danger position y", 0, height-1, 1)
    gw = GridWorld(width=width, height=height, 
                   goal_pos=(goal_pos_x, goal_pos_y),
                   danger_pos=(danger_pos_x, danger_pos_y),
                     wall_pos=(wall_pos_x, wall_pos_y))
    agent = Agent(0, 0, gw, placeholder)
else:
    # Initialisation de la grille par défaut
    gw = GridWorld()
    agent = Agent(0, 0, gw, placeholder)
    # Initialisation de la position de l'agent




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
dict_actions = {
                0:'up', 
                1:'down', 
                2:'left', 
                3:'right'
            }

def get_state():
    x, y = st.session_state.agent_pos
    return np.array([x / (gw.GRID_WIDTH-1), y / (gw.GRID_HEIGHT-1)])  # Normalisé

if st.sidebar.button("Code movement"):
    for episode in range(n_episodes):
        gw.reset_position(placeholder)
        while st.session_state.agent_pos != gw.goal_pos:
            x, y = st.session_state.agent_pos
            # st.session_state.Q[x][y][a] 
            # a : 0=up, 1=down, 2=left, 3=right
            
            # On “suspend” le script pour 2 secondes pour donner le temps de voir la position
            time.sleep(sleep_time)
            
            Q_a_s = st.session_state.Q[x][y]

            action = epsilon_greedy_choice(Q_a_s, epsilon)

            if agent.move_agent(dict_actions[action]):
                x_next, y_next = st.session_state.agent_pos

                Q_a_s_next = st.session_state.Q[x_next][y_next]

                # Q(s,a) ← Q(s,a) + α[r + γmaxQ(s′,a′) − Q(s,a)] (à compléter)
                st.session_state.Q[x][y][action] = Q_a_s[action] + alpha * (st.session_state.R[x_next][y_next] \
                                                                            + gama * max(Q_a_s_next, key=abs) - Q_a_s[action])

                gw.dessiner_grille(placeholder)



if st.sidebar.button("Entraîner Deep Q-Learning"):
    model = build_model(input_dim=2, output_dim=4)
    model = train_dqn(model, gw, agent, placeholder, epsilon, gama,alpha, episodes=10)
    model.save("dqn_model.h5")
