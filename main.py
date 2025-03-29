import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

class EcosystemGraph:
    def __init__(self):
        self.G = nx.DiGraph()
        self.nodes = {}
        self.ecosystem_type = "Terrestrial"

    def set_ecosystem(self, eco_type):
        self.ecosystem_type = eco_type
        print(f"\n🔹 ประเภทระบบนิเวศ: {eco_type}")

    def add_species(self, name, category):
        self.G.add_node(name)
        self.nodes[name] = category
        print(f"✅ เพิ่ม {name} เป็น {category}")

    def edit_species(self, old_name, new_name, new_category):
        if old_name in self.nodes:
            # แก้ไขชื่อและประเภท
            self.nodes.pop(old_name)
            self.G = nx.relabel_nodes(self.G, {old_name: new_name})
            self.nodes[new_name] = new_category
            print(f"✏️ แก้ไข {old_name} → {new_name} ({new_category})")
        else:
            print(f"❗️ ไม่พบชื่อ {old_name}")

    def delete_species(self, name):
        if name in self.nodes:
            self.G.remove_node(name)
            self.nodes.pop(name)
            print(f"🗑️ ลบสิ่งมีชีวิต {name} แล้ว")
        else:
            print(f"❗️ ไม่พบชื่อ {name}")

    def add_relationship(self, predator, prey):
        if predator in self.nodes and prey in self.nodes:
            self.G.add_edge(prey, predator)
            print(f"🔗 {predator} ล่า {prey}")
        else:
            print(f"❗️ ไม่พบชื่อ '{predator}' หรือ '{prey}'")

    def auto_generate_relationship(self):
        print("\n🔄 กำลังสร้างความสัมพันธ์อัตโนมัติ...")
        producers = [n for n in self.nodes if self.nodes[n] == "Producer"]
        herbivores = [n for n in self.nodes if self.nodes[n] == "Herbivore"]
        carnivores = [n for n in self.nodes if self.nodes[n] == "Carnivore"]
        decomposers = [n for n in self.nodes if self.nodes[n] == "Decomposer"]

        for herb in herbivores:
            for prod in producers:
                if not self.G.has_edge(prod, herb):
                    self.G.add_edge(prod, herb)
                    print(f"🔗 {herb} ล่า {prod}")

        for carn in carnivores:
            for herb in herbivores:
                if not self.G.has_edge(herb, carn):
                    self.G.add_edge(herb, carn)
                    print(f"🔗 {carn} ล่า {herb}")

        for deco in decomposers:
            for other in self.nodes:
                if other != deco and not self.G.has_edge(other, deco):
                    self.G.add_edge(other, deco)
                    print(f"♻️ {deco} ย่อยซากของ {other}")

        print("✅ สร้างความสัมพันธ์อัตโนมัติเรียบร้อย")
    def analyze_ecosystem(self):
        producers = [n for n in self.nodes if self.nodes[n] == "Producer"]
        herbivores = [n for n in self.nodes if self.nodes[n] == "Herbivore"]
        carnivores = [n for n in self.nodes if self.nodes[n] == "Carnivore"]
        decomposers = [n for n in self.nodes if self.nodes[n] == "Decomposer"]

        messages = []
        warning = False

        if len(herbivores) > len(carnivores) * 3:
            messages.append("⚠️ Herbivore มากเกินไป อาจทำให้ Producer ถูกกินหมด")
            warning = True
        if len(carnivores) < len(herbivores) / 2:
            messages.append("⚠️ Carnivore น้อยเกินไป อาจทำให้ Herbivore เพิ่มเร็วเกิน")
            warning = True
        if len(carnivores) > len(herbivores):
            messages.append("⚠️ Carnivore มากเกินไป อาจทำให้ Herbivore สูญพันธุ์")
            warning = True

        if not messages:
            messages.append("✅ ระบบนิเวศสมดุลดี")

        # Popup
        root = tk.Tk()
        root.withdraw()
        if warning:
            messagebox.showwarning("📊 วิเคราะห์ผลกระทบ", "\n".join(messages))
        else:
            messagebox.showinfo("📊 วิเคราะห์ผลกระทบ", "\n".join(messages))
        root.destroy()

        # Graph
        pos = nx.spring_layout(self.G, seed=42, k=1.2, scale=3)
        color_map = {"Producer": "green", "Herbivore": "blue", "Carnivore": "red", "Decomposer": "brown"}
        node_colors = [color_map.get(self.nodes[n], "gray") for n in self.G.nodes]

        plt.figure(figsize=(10, 6))
        nx.draw(self.G, pos, with_labels=True, node_color=node_colors, edge_color="gray",
                node_size=2000, font_size=10, font_weight="bold", arrows=True)
        plt.title(f"🌱 Network Graph - {self.ecosystem_type}")
        plt.axis('off')
        plt.tight_layout()
        plt.show()

        # Bar Chart
        categories = ['Producer', 'Herbivore', 'Carnivore', 'Decomposer']
        counts = [len(producers), len(herbivores), len(carnivores), len(decomposers)]

        plt.figure(figsize=(7, 5))
        bars = plt.bar(categories, counts, color=["green", "blue", "red", "brown"])
        plt.title("📊 โครงสร้างระบบนิเวศ")
        plt.ylabel("จำนวนสิ่งมีชีวิต")

        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, yval, ha='center', fontsize=10)

        plt.tight_layout()
        plt.show()

    def draw_graph(self):
        pos = nx.spring_layout(self.G, seed=42, k=1.2, scale=3)
        color_map = {"Producer": "green", "Herbivore": "blue", "Carnivore": "red", "Decomposer": "brown"}
        node_colors = [color_map.get(self.nodes[n], "gray") for n in self.G.nodes]

        plt.figure(figsize=(10, 6))
        nx.draw(self.G, pos, with_labels=True, node_color=node_colors, edge_color="gray",
                node_size=2000, font_size=10, font_weight="bold", arrows=True)
        plt.title(f"🌍 โครงสร้างความสัมพันธ์ของระบบนิเวศ ({self.ecosystem_type})")
        plt.axis('off')
        plt.tight_layout()
        plt.show()
# ======= แสดง Popup ต้อนรับ =======
root = tk.Tk()
root.withdraw()
messagebox.showinfo(
    "🌱 Ecosystem Simulation",
    "ยินดีต้อนรับสู่โปรแกรมจำลองระบบนิเวศ\nพร้อมวิเคราะห์ผลกระทบและความสัมพันธ์ของสิ่งมีชีวิต"
)
root.destroy()

# ======= เมนูหลัก =======
eco = EcosystemGraph()

while True:
    print("\n🌍 โปรแกรมจำลองระบบนิเวศ")
    print("1️⃣ กำหนดประเภทระบบนิเวศ (บก[Terrestrial] / น้ำ[Aquatic])")
    print("2️⃣ เพิ่มสิ่งมีชีวิต")
    print("3️⃣ แก้ไขสิ่งมีชีวิต")
    print("4️⃣ ลบสิ่งมีชีวิต")
    print("5️⃣ สร้างความสัมพันธ์อาหารอัตโนมัติ")
    print("6️⃣ วิเคราะห์ผลกระทบระบบนิเวศ")
    print("7️⃣ แสดงกราฟโครงสร้างความสัมพันธ์")
    print("0️⃣ ออกจากโปรแกรม")
    choice = input("เลือกเมนู: ")

    if choice == "1":
        while True:
            t = input("กรอกประเภท (Terrestrial / Aquatic): ").capitalize()
            if t in ["Terrestrial", "Aquatic"]:
                eco.set_ecosystem(t)
                break
            else:
                print("❗️ กรุณากรอกเฉพาะ Terrestrial หรือ Aquatic เท่านั้น")

    elif choice == "2":
        name = input("กรอกชื่อสิ่งมีชีวิต: ")

        valid_categories = ["Producer", "Herbivore", "Carnivore", "Decomposer"]
        while True:
            print("ประเภท: ผู้ผลิต[Producer] / สัตว์กินพืช[Herbivore] / สัตว์กินเนื้อ[Carnivore] / ผู้ย่อยสลาย[Decomposer]")
            cat = input("กรอกประเภท: ").capitalize()
            if cat in valid_categories:
                break
            else:
                print("❗️ กรุณากรอกเฉพาะ Producer / Herbivore / Carnivore / Decomposer เท่านั้น")

        eco.add_species(name, cat)

    elif choice == "3":
        old = input("กรอกชื่อสิ่งมีชีวิตเดิมที่ต้องการแก้ไข: ")
        new = input("กรอกชื่อใหม่: ")
        new_cat = input("กรอกประเภทใหม่ (Producer / Herbivore / Carnivore / Decomposer): ").capitalize()
        eco.edit_species(old, new, new_cat)

    elif choice == "4":
        name = input("กรอกชื่อสิ่งมีชีวิตที่ต้องการลบ: ")
        eco.delete_species(name)

    elif choice == "5":
        eco.auto_generate_relationship()

    elif choice == "6":
        eco.analyze_ecosystem()

    elif choice == "7":
        eco.draw_graph()

    elif choice == "0":
        print("👋 ออกจากโปรแกรม...")
        break

    else:
        print("❌ เลือกเมนูไม่ถูกต้อง กรุณาลองใหม่")
