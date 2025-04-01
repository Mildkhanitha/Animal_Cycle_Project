
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import tkinter as tk
from tkinter import messagebox
# ระบุ path ของฟอนต์
font_path = "./fonts/THSarabunNew.ttf"
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    font_name = font_prop.get_name()
else:
    font_name = 'Tahoma'  # ใช้ฟอนต์สำรอง
    font_prop = fm.FontProperties(family=font_name)  # กำหนด font_prop ให้ใช้ฟอนต์สำรอง

font_path = "./fonts/THSarabunNew.ttf"
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    font_name = font_prop.get_name()
else:
    font_name = 'Tahoma'
    font_prop = fm.FontProperties(family=font_name)


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
        if not self.nodes:
            print("❗️ ยังไม่มีข้อมูลสิ่งมีชีวิต กรุณาเพิ่มข้อมูลก่อนวิเคราะห์")
            return

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

        # Network Graph
        pos = nx.spring_layout(self.G, seed=42, k=1.2, scale=3)
        color_map = {"Producer": "green", "Herbivore": "blue", "Carnivore": "red", "Decomposer": "brown"}
        node_colors = [color_map.get(self.nodes[n], "gray") for n in self.G.nodes]

        plt.figure(figsize=(10, 6), constrained_layout=True)
        nx.draw(self.G, pos, with_labels=True, node_color=node_colors, edge_color="gray",
                node_size=2000, font_size=10, font_weight="bold", font_family=font_name, arrows=True)
        plt.title(f"Network Graph - {self.ecosystem_type}")
        plt.axis('off')
        plt.show(block=True)

        # Bar Chart
        categories = ['Producer', 'Herbivore', 'Carnivore', 'Decomposer']
        counts = [len(producers), len(herbivores), len(carnivores), len(decomposers)]

        plt.figure(figsize=(7, 5), constrained_layout=True)
        bars = plt.bar(categories, counts, color=["green", "blue", "red", "brown"])
        plt.title("โครงสร้างระบบนิเวศ", fontproperties=font_prop)
        plt.ylabel("จำนวนสิ่งมีชีวิต", fontproperties=font_prop)

        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, yval, ha='center', fontsize=10)

        plt.show(block=True)

    def draw_graph(self):
        if not self.nodes:
            print("❗️ ยังไม่มีข้อมูลสิ่งมีชีวิต กรุณาเพิ่มข้อมูลก่อนแสดงกราฟ")
            return

        pos = nx.spring_layout(self.G, seed=42, k=1.2, scale=3)
        color_map = {"Producer": "green", "Herbivore": "blue", "Carnivore": "red", "Decomposer": "brown"}
        node_colors = [color_map.get(self.nodes[n], "gray") for n in self.G.nodes]

        plt.figure(figsize=(10, 6))
        nx.draw(self.G, pos, with_labels=True, node_color=node_colors, edge_color="gray",
                node_size=2000, font_size=10, font_weight="bold", font_family=font_name, arrows=True)
        plt.title(f"🌍 โครงสร้างความสัมพันธ์ของระบบนิเวศ ({self.ecosystem_type})")
        plt.axis('off')
        plt.tight_layout()
        plt.show(block=True)


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

valid_categories = {
    "ผู้ผลิต": "Producer",
    "กินพืช": "Herbivore",
    "กินเนื้อ": "Carnivore",
    "ย่อยสลาย": "Decomposer",
    "Producer": "Producer",
    "Herbivore": "Herbivore",
    "Carnivore": "Carnivore",
    "Decomposer": "Decomposer"
}

while True:
    print("\n🌍 โปรแกรมจำลองระบบนิเวศ")
    print("1️⃣ กำหนดประเภทระบบนิเวศ (บนบก / ในน้ำ)")
    print("2️⃣ เพิ่มสิ่งมีชีวิต")
    print("3️⃣ แก้ไขสิ่งมีชีวิต")
    print("4️⃣ ลบสิ่งมีชีวิต")
    print("5️⃣ สร้างความสัมพันธ์อาหารอัตโนมัติ")
    print("6️⃣ วิเคราะห์ผลกระทบระบบนิเวศ")
    print("7️⃣ แสดงกราฟโครงสร้างความสัมพันธ์")
    print("0️⃣ ออกจากโปรแกรม")
    choice = input("เลือกเมนู: ").strip()

    if choice == "1":
        while True:
            t = input("กรอกประเภท (บนบก / ในน้ำ): ").strip()
            if t in ["บนบก", "Terrestrial"]:
                eco.set_ecosystem("Terrestrial")
                break
            elif t in ["ในน้ำ", "Aquatic"]:
                eco.set_ecosystem("Aquatic")
                break
            else:
                print("❗️ กรุณากรอกเฉพาะ 'บนบก' หรือ 'ในน้ำ' เท่านั้น")

    elif choice == "2":
        while True:
            name = input("กรอกชื่อสิ่งมีชีวิต (พิมพ์ 'ออก' เพื่อกลับไปหน้าหลัก): ").strip()
            if name == "ออก":
                break 
            while True:
                print("ประเภท: ผู้ผลิต / กินพืช / กินเนื้อ / ย่อยสลาย")
                cat_input = input("กรอกประเภท: ").strip()
                if cat_input in valid_categories:
                    cat = valid_categories[cat_input]
                    break
                else:
                    print("❗️ กรุณากรอกประเภทให้ถูกต้อง")

            eco.add_species(name, cat)

    elif choice == "3":
        old = input("กรอกชื่อสิ่งมีชีวิตเดิมที่ต้องการแก้ไข: ").strip()
        new = input("กรอกชื่อใหม่: ").strip()
        while True:
            new_cat_input = input("กรอกประเภทใหม่ (ผู้ผลิต / กินพืช / กินเนื้อ / ย่อยสลาย): ").strip()
            if new_cat_input in valid_categories:
                new_cat = valid_categories[new_cat_input]
                break
            else:
                print("❗️ กรุณากรอกประเภทให้ถูกต้อง")
        eco.edit_species(old, new, new_cat)

    elif choice == "4":
        name = input("กรอกชื่อสิ่งมีชีวิตที่ต้องการลบ: ").strip()
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
