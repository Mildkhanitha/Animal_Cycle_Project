from flask import Flask
import dash
from dash import dcc, html, Input, Output, State
import networkx as nx
import plotly.graph_objects as go

# สร้าง Flask App
server = Flask(__name__)
app = dash.Dash(__name__, server=server)

# กราฟระบบนิเวศ
class EcosystemGraph:
    def __init__(self):
        self.G = nx.DiGraph()
        self.nodes = {}
        self.ecosystem_type = "สัตว์บก"

    def set_ecosystem(self, eco_type):
        self.ecosystem_type = eco_type

    def add_species(self, name, category):
        self.G.add_node(name)
        self.nodes[name] = category

    def add_relationship(self, predator, prey):
        if predator in self.nodes and prey in self.nodes:
            self.G.add_edge(prey, predator)

    def analyze_ecosystem(self):
        herbivores = [n for n in self.nodes if self.nodes[n] == "Herbivore"]
        predators = [n for n in self.nodes if self.nodes[n] == "Carnivore"]

        analysis = []
        if len(herbivores) > len(predators) * 3:
            analysis.append("⚠️ สัตว์กินพืชเยอะเกินไป อาจทำให้พืชลดลง!")
        if len(predators) < len(herbivores) / 2:
            analysis.append("⚠️ ผู้ล่ามีน้อย อาจทำให้สัตว์กินพืชเพิ่มขึ้นเร็ว!")
        if len(predators) > len(herbivores):
            analysis.append("⚠️ ผู้ล่าเยอะเกินไป อาจทำให้สัตว์กินพืชลดลง!")
        return analysis

    def draw_graph(self):
        pos = nx.spring_layout(self.G, seed=42)
        edge_x, edge_y = [], []
        for edge in self.G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        node_x, node_y, node_color, node_labels = [], [], [], []
        color_map = {"Producer": "green", "Herbivore": "blue", "Carnivore": "red", "Decomposer": "brown"}
        
        for node in self.G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_color.append(color_map[self.nodes[node]])
            node_labels.append(node)

        edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1, color="gray"), mode="lines")
        node_trace = go.Scatter(
            x=node_x, y=node_y, mode="markers+text", marker=dict(size=15, color=node_color),
            text=node_labels, textposition="top center"
        )

        fig = go.Figure(data=[edge_trace, node_trace])
        fig.update_layout(title=f"ระบบนิเวศ: {self.ecosystem_type}", showlegend=False)
        return fig

# สร้าง EcosystemGraph
eco = EcosystemGraph()

# UI ของ Dash
app.layout = html.Div([
    html.H1("🌍 ระบบนิเวศเชิงโต้ตอบ"),
    
    html.Label("เลือกประเภทระบบนิเวศ:"),
    dcc.RadioItems(
        id="select-ecosystem",
        options=[{"label": "สัตว์บก", "value": "สัตว์บก"}, {"label": "สัตว์น้ำ", "value": "สัตว์น้ำ"}],
        value="สัตว์บก",
        inline=True
    ),
    
    html.Label("เพิ่มสิ่งมีชีวิต:"),
    dcc.Input(id="species-name", type="text", placeholder="ชื่อสัตว์"),
    dcc.Dropdown(
        id="species-category",
        options=[
            {"label": "ผู้ผลิต (Producer)", "value": "Producer"},
            {"label": "สัตว์กินพืช (Herbivore)", "value": "Herbivore"},
            {"label": "ผู้ล่า (Carnivore)", "value": "Carnivore"},
            {"label": "ผู้ย่อยสลาย (Decomposer)", "value": "Decomposer"}
        ],
        placeholder="เลือกประเภท"
    ),
    html.Button("เพิ่มสัตว์", id="add-species", n_clicks=0),

    html.Label("กำหนดห่วงโซ่อาหาร:"),
    dcc.Input(id="predator", type="text", placeholder="ผู้ล่า"),
    dcc.Input(id="prey", type="text", placeholder="เหยื่อ"),
    html.Button("เพิ่มความสัมพันธ์", id="add-relationship", n_clicks=0),

    html.H3("📊 การวิเคราะห์ระบบนิเวศ"),
    html.Div(id="ecosystem-analysis"),
    
    dcc.Graph(id="ecosystem-graph")
])

# Callbacks
@app.callback(
    Output("ecosystem-graph", "figure"),
    Output("ecosystem-analysis", "children"),
    Input("select-ecosystem", "value"),
    Input("add-species", "n_clicks"),
    Input("add-relationship", "n_clicks"),
    State("species-name", "value"),
    State("species-category", "value"),
    State("predator", "value"),
    State("prey", "value"),
)
def update_ecosystem(eco_type, _, __, species_name, species_category, predator, prey):
    eco.set_ecosystem(eco_type)
    
    if species_name and species_category:
        eco.add_species(species_name, species_category)
    
    if predator and prey:
        eco.add_relationship(predator, prey)
    
    analysis = eco.analyze_ecosystem()
    return eco.draw_graph(), html.Ul([html.Li(item) for item in analysis])

# Run Server
if __name__ == "__main__":
    app.run_server(debug=True)
