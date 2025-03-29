import networkx as nx
import matplotlib.pyplot as plt

class EcosystemGraph:
    def __init__(self):
        self.G = nx.DiGraph()
        self.nodes = {}
        self.ecosystem_type = "Terrestrial"

    def set_ecosystem(self, eco_type):
        self.ecosystem_type = eco_type
        print(f"\n🔹 Ecosystem type set to: {eco_type}")

    def add_species(self, name, category):
        self.G.add_node(name)
        self.nodes[name] = category
        print(f"✅ Added {name} as {category}")

    def add_relationship(self, predator, prey):
        if predator in self.nodes and prey in self.nodes:
            self.G.add_edge(prey, predator)
            print(f"🔗 {predator} eats {prey}")
        else:
            print("❌ Species not found. Please check the names again.")

    def analyze_ecosystem(self):
        producers = [n for n in self.nodes if self.nodes[n] == "Producer"]
        herbivores = [n for n in self.nodes if self.nodes[n] == "Herbivore"]
        carnivores = [n for n in self.nodes if self.nodes[n] == "Carnivore"]
        decomposers = [n for n in self.nodes if self.nodes[n] == "Decomposer"]

        print("\n📊 Ecosystem Analysis:")
        messages = []

        if len(herbivores) > len(carnivores) * 3:
            messages.append("⚠️ มีจำนวนผู้บริโภคพืชมากเกินไป อาจส่งผลให้ผู้ผลิตถูกบริโภคจนหมด")
        if len(carnivores) < len(herbivores) / 2:
            messages.append("⚠️ ผู้บริโภคระดับที่ 2 มีน้อยเกินไป อาจทำให้ผู้บริโภคพืชเพิ่มจำนวนเกินควบคุม")
        if len(carnivores) > len(herbivores):
            messages.append("⚠️ ผู้บริโภคระดับที่ 2 มากเกินไป อาจส่งผลให้ผู้บริโภคพืชลดลงอย่างรวดเร็ว")

        if not messages:
            messages.append("✅ ระบบนิเวศมีความสมดุลในระดับหนึ่ง")

        for msg in messages:
            print(msg)

        # วาดกราฟความสัมพันธ์แสดงผลกระทบ
        pos = nx.spring_layout(self.G, seed=42)
        color_map = {
            "Producer": "green",
            "Herbivore": "blue",
            "Carnivore": "red",
            "Decomposer": "brown"
        }
        node_colors = [color_map.get(self.nodes[n], "gray") for n in self.G.nodes]

        plt.figure(figsize=(10, 6))
        nx.draw(self.G, pos, with_labels=True, node_color=node_colors, edge_color="gray",
                node_size=2000, font_size=10, font_weight="bold", arrows=True)
        
        # แสดงคำอธิบายด้านบนกราฟ
        plt.title("🌐 ผลกระทบจากโครงสร้างระบบนิเวศ", fontsize=14)
        explanation = "\n".join(messages)
        plt.figtext(0.5, 0.01, explanation, wrap=True, horizontalalignment='center', fontsize=10)
        
        plt.tight_layout()
        plt.show()

    def draw_graph(self):
        pos = nx.spring_layout(self.G, seed=42)
        color_map = {
            "Producer": "green",
            "Herbivore": "blue",
            "Carnivore": "red",
            "Decomposer": "brown"
        }
        node_colors = [color_map.get(self.nodes[n], "gray") for n in self.G.nodes]

        plt.figure(figsize=(10, 6))
        nx.draw(self.G, pos, with_labels=True, node_color=node_colors, edge_color="gray",
                node_size=2000, font_size=10, font_weight="bold", arrows=True)
        plt.title(f"🌱 Ecosystem Graph ({self.ecosystem_type})")
        plt.show()


# Interactive Menu
eco = EcosystemGraph()

while True:
    print("\n🌍 Ecosystem Simulation")
    print("1️⃣ Set Ecosystem Type (Terrestrial / Aquatic)")
    print("2️⃣ Add Species")
    print("3️⃣ Add Food Chain Relationship")
    print("4️⃣ Analyze Ecosystem")
    print("5️⃣ Show Ecosystem Graph")
    print("0️⃣ Exit")
    choice = input("Select an option: ")

    if choice == "1":
        t = input("Enter ecosystem type (Terrestrial / Aquatic): ")
        eco.set_ecosystem(t)

    elif choice == "2":
        name = input("Enter species name: ")
        print("Available roles: Producer / Herbivore / Carnivore / Decomposer")
        cat = input("Enter category: ")
        eco.add_species(name, cat)

    elif choice == "3":
        predator = input("Enter predator name: ")
        prey = input("Enter prey name: ")
        eco.add_relationship(predator, prey)

    elif choice == "4":
        eco.analyze_ecosystem()

    elif choice == "5":
        eco.draw_graph()

    elif choice == "0":
        print("👋 Exiting program...")
        break

    else:
        print("❌ Invalid choice. Please try again.")
