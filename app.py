import streamlit as st
import pygambit as gbt
import networkx as nx
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Game Tree Builder",
    page_icon="🧩",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600&family=Nunito:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}


.stApp {
    background-color: #fdf7f9;
    color: #2d2d2d;
}



/* Main container */
.block-container {
    max-width: 680px;
    padding-top: 4rem;
    padding-bottom: 4rem;
}

/* Title area */
.title-block {
    margin-bottom: 3rem;
}
.title-block h1 {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 600;
    color: #d63384;
    letter-spacing: -0.01em;
    margin-bottom: 0.4rem;
}
.title-block p {
    font-size: 1.5rem;
    color: #5a9e3a;
    margin: 0;
    font-weight: 500;
}

/* Section labels */
.section-label {
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #5ba13b;
    margin-bottom: 0.75rem;
    margin-top: 2rem;
}

/* Divider */
.thin-divider {
    border: none;
    border-top: 1px solid #f0d6e4;
    margin: 2rem 0;
}

/* Inputs */
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input {
    background-color: #fff0f5 !important;
    border: 1.5px solid #f0b8d0 !important;
    border-radius: 8px !important;
    color: #2d2d2d !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.92rem !important;
    padding: 0.55rem 0.85rem !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus {
    border-color: #d63384 !important;
    box-shadow: 0 0 0 3px rgba(214,51,132,0.1) !important;
}

/* Select box */
div[data-testid="stSelectbox"] > div > div {
    background-color: #fff0f5 !important;
    border: 1.5px solid #f0b8d0 !important;
    border-radius: 8px !important;
    color: #2d2d2d !important;
}

/* Labels */
label, .stTextInput label, .stNumberInput label, .stSelectbox label {
    font-size: 0.83rem !important;
    color: #b0556e !important;
    font-weight: 600 !important;
    margin-bottom: 0.3rem !important;
}

/* Stage sub-headers */
.stMarkdown strong {
    color: #d63384 !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 1rem !important;
}

/* Button */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #77b52b 30%, #3a9e6f 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    padding: 0.7rem 2rem !important;
    width: 100% !important;
    margin-top: 1rem !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.15s !important;
}
div[data-testid="stButton"] > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}

/* Summary box */
.summary-box {
    background: #fff8fb;
    border: 1.5px solid #f0b8d0;
    border-left: 4px solid #d63384;
    border-radius: 8px;
    padding: 1.3rem 1.5rem;
    margin-top: 2rem;
    font-size: 0.88rem;
    color: #7a7a7a;
    line-height: 1.8;
}
.summary-box span {
    color: #3a9e6f;
    font-weight: 600;
}

/* Success message */
div[data-testid="stAlert"] {
    background-color: #edfaf3 !important;
    border: 1.5px solid #3a9e6f !important;
    border-radius: 8px !important;
    color: #2a7a55 !important;
}
</style>
""", unsafe_allow_html=True)

# Header 
st.markdown("""
<div class="title-block">
    <h1>Game Tree Builder</h1>
    <p>Describe your game and I will make a tree :)</p>
</div>
""", unsafe_allow_html=True)

# Players
st.markdown('<div class="section-label">Players</div>', unsafe_allow_html=True)

num_players = st.selectbox(
    "Number of players",
    options=[2, 3],
    index=0,
)

player_names = []
cols = st.columns(num_players)
defaults = ["Alice", "Bob", "Carol"]
for i, col in enumerate(cols):
    with col:
        name = st.text_input(f"Player {i+1} name", value=defaults[i], key=f"player_{i}")
        player_names.append(name.strip() if name.strip() else defaults[i])

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)

# Stages
st.markdown('<div class="section-label">Stages</div>', unsafe_allow_html=True)

num_stages = st.selectbox(
    "Number of stages",
    options=[1, 2, 3, 4],
    index=1,
    help="A stage is one round of decisions. Most classic games have 2–3 stages."
)

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)

# Stage Details 
st.markdown('<div class="section-label">Stage Details</div>', unsafe_allow_html=True)

stage_data = []
for s in range(num_stages):
    st.markdown(f"**Stage {s+1}**")
    c1, c2 = st.columns([1, 1])
    with c1:
        whose_turn = st.selectbox(
            "Whose turn?",
            options=player_names,
            key=f"stage_{s}_player"
        )
    with c2:
        num_actions = st.selectbox(
            "Number of choices",
            options=[2, 3, 4],
            key=f"stage_{s}_actions"
        )
        
    actions_data = []
    action_names = []
    action_cols = st.columns(num_actions)
    for a, col in enumerate(action_cols):
        with col:
            action = st.text_input(
                f"Choice {a+1}",
                value=f"Action {a+1}",
                key=f"stage_{s}_action_{a}"
            )
            action_name = action.strip() if action.strip() else f"Action {a+1}"
            action_names.append(action_name)

            if s == num_stages - 1:
                st.caption("Terminal (last stage)")
                is_terminal = True
            else:
                is_terminal = st.checkbox(
                    "Terminal?",
                    key=f"stage_{s}_action_{a}_terminal"
                )

            if is_terminal:
                st.markdown(f"**Payoffs at: `{action_name}`**")
                payoff_cols = st.columns(num_players)
                action_payoffs = []
                for p, pcol in enumerate(payoff_cols):
                    with pcol:
                        payoff = st.number_input(
                            f"{player_names[p]}",
                            value=0,
                            step=1,
                            key=f"payoff_{s}_{a}_{p}"
                        )
                        action_payoffs.append(payoff)
            else:
                action_payoffs = None

            actions_data.append({
                "name": action_name,
                "terminal": is_terminal,
                "payoffs": action_payoffs
            })


    is_informed = st.checkbox(
        f"Does {whose_turn} know all previous moves?",
        value=True,
        key=f"stage_{s}_informed"
    )

    stage_data.append({
        "player": whose_turn,
        "num_actions": num_actions,
        "actions": action_names,
        "informed": is_informed,
        "actions_data": actions_data
    })

    

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)

# Game Name
st.markdown('<div class="section-label">Game Info</div>', unsafe_allow_html=True)

game_name = st.text_input("Game name (optional)", placeholder="e.g. Prisoner's Dilemma")



g = gbt.Game.new_tree(
    players = player_names,
    title = game_name
)

g.append_move(
    g.root,
    player=stage_data[0]["player"],
    actions=stage_data[0]["actions"]
)

pointer_nodes = [g.root]

for s in range(1, num_stages):
    next_nodes = []
    for node in pointer_nodes:
        for a in range(stage_data[s-1]["num_actions"]):
            if stage_data[s-1]["actions_data"][a]["terminal"] == False:
                g.append_move(
                    node.children[a],
                    player=stage_data[s]["player"],
                    actions=stage_data[s]["actions"]
                )
                next_nodes.append(node.children[a])
            else:
                g.set_outcome(
                    node.children[a],
                    g.add_outcome(stage_data[s-1]["actions_data"][a]["payoffs"])
                    )
    pointer_nodes = next_nodes

for node in pointer_nodes:
    for a in range(stage_data[num_stages-1]["num_actions"]):
        g.set_outcome(
            node.children[a],
            g.add_outcome(stage_data[num_stages-1]["actions_data"][a]["payoffs"])
        )

if not stage_data[s]["informed"] and len(next_nodes) > 1:
    for node in next_nodes[1:]:
        g.set_infoset(node, next_nodes[0].infoset)



G = nx.DiGraph()

def build_networkx_graph(gambit_node, graph):
    
    u_id = str(gambit_node)
    
    if gambit_node.is_terminal:
        payoffs = tuple([int(float(gambit_node.outcome[p])) for p in g.players])
        label = str(payoffs)
        color = "#58DF5F"
    else:
        label = gambit_node.player.label
        color = "#f9a8d4"
    
    graph.add_node(u_id, label=label, color=color)
    
    for i, child in enumerate(gambit_node.children):
        v_id = str(child)
        action_name = gambit_node.infoset.actions[i].label
        graph.add_edge(u_id, v_id, label=action_name)
        build_networkx_graph(child, graph)



G.clear()
build_networkx_graph(g.root, G)

fig, ax = plt.subplots(figsize=(12, 8))
try:
    pos = nx.drawing.nx_pydot.graphviz_layout(G, prog="dot")
except:
    pos = nx.shell_layout(G)

node_colors = [G.nodes[n].get('color', '#f9a8d4') for n in G.nodes()]
labels = nx.get_node_attributes(G, 'label')
edge_labels = nx.get_edge_attributes(G, 'label')

nx.draw(G, pos, ax=ax, with_labels=True, labels=labels,
        node_size=2000, node_color=node_colors, font_size=10,
        font_weight="bold", edge_color="#86efac", arrows=True)

nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
        font_color='#d63384', ax=ax)

st.pyplot(fig)


