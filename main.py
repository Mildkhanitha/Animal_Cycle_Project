import networkx as nx
import matplotlib.pyplot as plt

class EcosystemGraph:
    def __init__(self):
        self.G = nx.DiGraph()
        self.nodes = {}  # เก็บประเภทของสัตว์
        self.ecosystem_type = "สัตว์บก"

    def set_ecosystem(self, eco_type):
        """กำหนดประเภทของระบบนิเวศ (สัตว์บก / สัตว์น้ำ)"""
        self.ecosystem_type = eco_type
        print(f"\n🔹 ระบบนิเวศถูกตั้งค่าเป็น: {eco_type}")

    def add_species(self, name, category):
        """เพิ่มสิ่งมีชีวิตเข้าไปในระบบนิเวศ"""
        self.G.add_node(name)
        self.nodes[name] = category
        print(f"✅ เพิ่ม {name} เป็น {category} ในระบบ {self.ecosystem_type}")

    def add_relationship(self, predator, prey):
        """เพิ่มความสัมพันธ์ระหว่างสัตว์"""
        if predator in self.nodes and prey in self.nodes:
            self.G.add_edge(prey, predator)
            print(f"🔗 {predator} ล่า {prey}")
        else:
            print("❌ ไม่พบชื่อสัตว์ กรุณาเพิ่มสัตว์ก่อน!")

    def analyze_ecosystem(self):
        """วิเคราะห์ผลกระทบของระบบนิเวศ"""
        herbivores = [n for n in self.nodes if self.nodes[n] == "Herbivore"]
        predators = [n for n in self.nodes if self.nodes[n] == "Carnivore"]

        print("\n📊 วิเคราะห์ระบบนิเวศ:")
        if len(herbivores) > len(predators) * 3:
            print("⚠️ สัตว์กินพืชเยอะเกินไป อาจทำให้พืชลดลง!")
        if len(predators) < len(herbivores) / 2:
            print("⚠️ ผู้ล่ามีน้อย อาจทำให้สัตว์กินพืชเพิ่มขึ้นเร็ว!")
        if len(predators) > len(herbivores):
            print("⚠️ ผู้ล่าเยอะเกินไป อาจทำให้สัตว์กินพืชลดลง!")

    def draw_graph(self):
        """แสดงผลกราฟของระบบนิเวศ"""
        pos = nx.spring_layout(self.G, seed=42)
        node_colors = {"Producer": "green", "Herbivore": "blue", "Carnivore": "red", "Decomposer": "brown"}
        colors = [node_colors[self.nodes[node]] for node in self.G.nodes]

        plt.figure(figsize=(8, 6))
        nx.draw(self.G, pos, with_labels=True, node_color=colors, edge_color="gray",
                node_size=2000, font_size=10, font_weight="bold", arrows=True)
        plt.title(f"Ecosystem Graph - {self.ecosystem_type}")
        plt.show()

# ==========================
# ระบบเมนูหลัก
# ==========================
eco = EcosystemGraph()

while True:
    print("\n🌍 ระบบจำลองระบบนิเวศ")
    print("1️⃣ เลือกระบบนิเวศ (สัตว์บก / สัตว์น้ำ)")
    print("2️⃣ เพิ่มสิ่งมีชีวิตในระบบนิเวศ")
    print("3️⃣ เพิ่มห่วงโซ่อาหาร")
    print("4️⃣ วิเคราะห์ผลกระทบของระบบนิเวศ")
    print("5️⃣ แสดงกราฟระบบนิเวศ")
    print("0️⃣ ออกจากโปรแกรม")
    
    choice = input("🔹 เลือกเมนู: ")

    if choice == "1":
        eco_type = input("🟢 เลือกประเภทระบบนิเวศ (สัตว์บก / สัตว์น้ำ): ")
        eco.set_ecosystem(eco_type)

    elif choice == "2":
        name = input("✏️ กรอกชื่อสิ่งมีชีวิต: ")
        print("🔸 ประเภทที่สามารถเลือกได้: Producer, Herbivore, Carnivore, Decomposer")
        category = input("🟡 เลือกประเภท: ")
        eco.add_species(name, category)

    elif choice == "3":
        predator = input("🔴 กรอกชื่อผู้ล่า: ")
        prey = input("🔵 กรอกชื่อเหยื่อ: ")
        eco.add_relationship(predator, prey)

    elif choice == "4":
        eco.analyze_ecosystem()

    elif choice == "5":
        eco.draw_graph()

    elif choice == "0":
        print("👋 ออกจากโปรแกรม...")
        break

    else:
        print("❌ กรุณาเลือกเมนูที่ถูกต้อง!")
