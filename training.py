import random
from tensorflow import keras
import numpy as np
import pandas as pd
import streamlit as st
import time
from collections import deque

def epsilon_greedy_choice(Q_s, epsilon):
    """
    Q_s est la liste des Q-values pour l'état courant, 
    une par action. (Ex: [Q(s,UP), Q(s,DOWN), Q(s,LEFT), Q(s,RIGHT)])
    epsilon est le paramètre d'exploration.
    """
    # On tire un nombre aléatoire dans [0..1]
    u = random.random()

    # Si on explore...
    if u < epsilon:
        # Choix aléatoire parmi toutes les actions
        action = random.randint(0, len(Q_s) - 1)
    else:
        # Exploitation : choisir la meilleure action (ArgMax)
        max_q = max(Q_s)
        # S'il y a égalité, on peut choisir aléatoirement parmi les meilleurs
        best_actions = [i for i, q in enumerate(Q_s) if q == max_q]
        # On prend l'un des "meilleurs" au hasard (gestion d'éventuels ex æquo)
        action = random.choice(best_actions)

    return int(action)


# Q(s,a) ← Q(s,a) + α[r + γmaxQ(s′,a′) − Q(s,a)] (à compléter)

def build_model(input_dim, output_dim):
    model = keras.Sequential([
        keras.layers.Dense(24, activation='relu', input_shape=(input_dim,)),
        keras.layers.Dense(output_dim,),
    ])
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001), loss='mse')
    return model


def get_normalise_state(x, y, gw):
    return np.array([x / (gw.GRID_WIDTH-1), y / (gw.GRID_HEIGHT-1)]).reshape(1,-1)  # Normalisé


def train_dqn(model, gw, agent, placeholder, epsilon, gama,alpha, episodes=10, n_steps=30, sleep_time=0.1):
    memory = deque(maxlen=2000)  # Mémoire pour stocker les expériences
    batch_size = 32  # Taille du batch pour l'entraînement
    dict_actions = {
                0:'up', 
                1:'down', 
                2:'left', 
                3:'right'
            }

    for ep in range(episodes):
        print(f"Episode {ep+1}/{episodes}")
        gw.reset_position(placeholder)
        for step in range(n_steps):
            # On "suspend" le script pour 2 secondes pour donner le temps de voir la position
            #time.sleep(0.5)
            
            x, y = st.session_state.agent_pos
            state = get_normalise_state(x, y, gw)

            epsi = np.random.uniform(0, 1)

            if epsi < epsilon:
                action = random.randint(0, 3)

            else:
                q_pred = model.predict(state, verbose=0)[0]
                action = np.argmax(q_pred)
                
            time.sleep(sleep_time)
            agent.move_agent(dict_actions[action])
            x_next, y_next = st.session_state.agent_pos
            state_next = get_normalise_state(x_next, y_next, gw)

            reward = st.session_state.R[x_next][y_next]
            done = (x_next, y_next) == gw.goal_pos
            

            memory.append(((x,y), action, reward, (x_next,y_next), done))
            train_bash = random.sample(memory, min(len(memory), batch_size))
            if done:
                break

        print(f"Memory size: {len(memory)}")
        for state, action, reward, state_next, done in train_bash:
            x, y = state
            x_next, y_next = state_next
            state = get_normalise_state(x, y, gw)
            state_next = get_normalise_state(x_next, y_next, gw)

            target = reward if done else reward + gama * np.amax(model.predict(state_next, verbose=0)[0])
            target_f = model.predict(state, verbose=0)
            target_f[0][action] = target
            if (x_next, y_next) == gw.goal_pos:
                print(target_f)
                model.fit(state, target_f, epochs=10, verbose=0)
            else:
                model.fit(state, target_f, epochs=1, verbose=0)
            st.session_state.Q[x][y] = target_f[0]
        
    return model

    
