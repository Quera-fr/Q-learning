import random
from tensorflow import keras
import numpy as np
import pandas as pd
import streamlit as st

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
        keras.layers.Dense(24, activation='relu'),
        keras.layers.Dense(output_dim, activation='linear')
    ])
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001), loss='mse')
    return model


def get_normalise_state(x, y, gw):
    return np.array([x / (gw.GRID_WIDTH-1), y / (gw.GRID_HEIGHT-1)]).reshape(1,-1)  # Normalisé

def train_dqn(model, gw, agent, placeholder, epsilon,gama,alpha, episodes=10):
    dict_actions = {
                0:'up', 
                1:'down', 
                2:'left', 
                3:'right'
            }
    
    for episode in range(episodes):
        target = list()
        X = list()

        gw.reset_position( placeholder)
        while st.session_state.agent_pos != gw.goal_pos :
            x, y = st.session_state.agent_pos
            state = get_normalise_state(x, y, gw)

            u = random.random()

            # Si on explore...
            if u < epsilon:
                # Choix aléatoire parmi toutes les actions
                action = random.randint(0, len(dict_actions) - 1)
            else:
                q_pred = model.predict(state, verbose=0)[0]
                action = np.argmax(q_pred)
            
            if agent.move_agent(dict_actions[action]):
                x_next, y_next = st.session_state.agent_pos
                next_state = get_normalise_state(x_next, y_next, gw)
                q_next = model.predict(next_state, verbose=0)[0]

                reward = st.session_state.R[x_next][y_next]

                target_value = reward + gama * np.max(q_next)
                q_pred[action] = (1 - alpha) * q_pred[action] + alpha * target_value

                st.session_state.Q[x][y] = q_pred
                gw.dessiner_grille(placeholder)

                X.append(state.flatten())
                target.append(q_pred)

                df = pd.DataFrame(X, columns=['x', 'y'])
                df_target = pd.DataFrame(target, columns=['q_up', 'q_down', 'q_left', 'q_right'])
                df = pd.concat([df, df_target], axis=1)
                df.to_csv("data.csv", index=False)

    
        model.fit( df[['x', 'y']], df[['q_up', 'q_down', 'q_left', 'q_right']], 
                  batch_size=32, shuffle=True,  # epochs=10, verbose=0
                  validation_split=0.2,  # Pour valider le modèle
            epochs=10, verbose=0)
        
    return model