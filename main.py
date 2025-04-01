
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import tkinter as tk
from tkinter import messagebox

# ======= ตั้งค่าฟอนต์ =======
font_path = "./fonts/THSarabunNew.ttf"
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    font_name = font_prop.get_name()
else:
    font_name = 'Tahoma'
    font_prop = fm.FontProperties(family=font_name)


# ======= ตั้งค่าฟอนต์ =======
class EcosystemGraph:
    def __init__(self):
        self.G = nx.DiGraph()
        self.nodes = {}
        self.ecosystem_type = "Terrestrial"

    def add_species(self, name, category):
        self.G.add_node(name)
        self.nodes[name] = category
        print(f"✅ เพิ่ม {name} เป็น {category}")

    def delete_species(self, name):
        if name in self.nodes:
            self.G.remove_node(name)
            self.nodes.pop(name)
            print(f"🗑️ ลบสิ่งมีชีวิต {name} แล้ว")
        else:
            print(f"❗️ ไม่พบชื่อ {name}")

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

    def edit_species(self, old_name, new_name, new_category):
        if old_name not in self.nodes:
            print(f"❗️ ไม่พบ {old_name} ในระบบ")
            return

        # อัปเดตชื่อในกราฟ
        self.G = nx.relabel_nodes(self.G, {old_name: new_name})
        
        # อัปเดตข้อมูลใน nodes
        self.nodes.pop(old_name)
        self.nodes[new_name] = new_category
        print(f"✏️ แก้ไข {old_name} เป็น {new_name} ({new_category}) เรียบร้อย")

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
            messages.append("⚠️ สัตว์กินพืช มากเกินไป อาจทำให้ ผู้ผลิต ถูกกินหมด")
            warning = True
        if len(carnivores) < len(herbivores) / 2:
            messages.append("⚠️ สัตว์กินเนื้อ น้อยเกินไป อาจทำให้ สัตว์กินพืช เพิ่มเร็วเกิน")
            warning = True
        if len(carnivores) > len(herbivores):
            messages.append("⚠️ สัตว์กินเนื้อ มากเกินไป อาจทำให้ สัตว์กินพืช สูญพันธุ์")
            warning = True

        if not messages:
            messages.append("✅ ระบบนิเวศสมดุลดี")

        root = tk.Tk()
        root.withdraw()
        if warning:
            messagebox.showwarning("📊 วิเคราะห์ผลกระทบ", "\n".join(messages))
        else:
            messagebox.showinfo("📊 วิเคราะห์ผลกระทบ", "\n".join(messages))
        root.destroy()


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

# ======= ชุดข้อมูลตัวอย่าง =======
sample_datasets = {
    "1": [
        {"name": "หญ้า", "category": "Producer"},
        {"name": "ต้นไม้", "category": "Producer"},
        {"name": "กระต่าย", "category": "Herbivore"},
        {"name": "กวาง", "category": "Herbivore"},
        {"name": "วัว", "category": "Herbivore"},
        {"name": "สิงโต", "category": "Carnivore"},
        {"name": "เหยี่ยว", "category": "Carnivore"},
        {"name": "งู", "category": "Carnivore"},
        {"name": "เชื้อรา", "category": "Decomposer"},
        {"name": "แมลง", "category": "Decomposer"}
    ],
    "2": [
        {"name": "ไผ่", "category": "Producer"},
        {"name": "ต้นหญ้า", "category": "Producer"},
        {"name": "กระต่าย", "category": "Herbivore"},
        {"name": "แพะ", "category": "Herbivore"},
        {"name": "หมาป่า", "category": "Carnivore"},
        {"name": "เหยี่ยว", "category": "Carnivore"},
        {"name": "เชื้อรา", "category": "Decomposer"},
        {"name": "แบคทีเรียดิน", "category": "Decomposer"}
    ],
    "3": [
        {"name": "เฟิร์น", "category": "Producer"},
        {"name": "ไม้ใหญ่", "category": "Producer"},
        {"name": "วัว", "category": "Herbivore"},
        {"name": "ควาย", "category": "Herbivore"},
        {"name": "ช้าง", "category": "Herbivore"},
        {"name": "เสือ", "category": "Carnivore"},
        {"name": "สิงโต", "category": "Carnivore"},
        {"name": "งู", "category": "Carnivore"},
        {"name": "เหยี่ยว", "category": "Carnivore"},
        {"name": "เชื้อรา", "category": "Decomposer"},
        {"name": "แมลง", "category": "Decomposer"},
        {"name": "แบคทีเรียดิน", "category": "Decomposer"}
    ]
}


def show_current_species():
    if not eco.nodes:
        print("⚠️ ยังไม่มีข้อมูลสิ่งมีชีวิตในระบบ")
    else:
        print("\n📄 สิ่งมีชีวิตปัจจุบันในระบบ:")
        for name, cat in eco.nodes.items():
            print(f"- {name} ({cat})")



def clear_all_species():
    eco.G.clear()
    eco.nodes.clear()
    print("🗑️ ลบข้อมูลสิ่งมีชีวิตทั้งหมดแล้ว")


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

root = tk.Tk()
root.withdraw()
messagebox.showinfo(
    "🌱 Ecosystem Simulation",
    "ยินดีต้อนรับสู่โปรแกรมจำลองระบบนิเวศบนบก"
)
root.destroy()

while True:
    print("\n🌍 โปรแกรมจำลองระบบนิเวศ (บนบก)")
    print("1️⃣ เพิ่มสิ่งมีชีวิต")
    print("2️⃣ ลบสิ่งมีชีวิต")
    print("3️⃣ สร้างความสัมพันธ์ในลำดับห่วงโซ่อาหาร")
    print("4️⃣ วิเคราะห์ผลกระทบระบบนิเวศ")
    print("5️⃣ แสดงกราฟโครงสร้างความสัมพันธ์")
    print("6️⃣ แก้ไขสิ่งมีชีวิต")
    print("9️⃣ ใช้ชุดข้อมูลตัวอย่าง")
    print("0️⃣ ออกจากโปรแกรม")
    choice = input("เลือกเมนู: ").strip()

    
    if choice == "1":
        show_current_species()
        while True:
            name = input("กรอกชื่อสิ่งมีชีวิต (พิมพ์ 'ออก' เพื่อกลับ): ").strip()
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
            
            if name in eco.nodes:
                print(f"❗️ '{name}' มีอยู่แล้วในระบบ")
                continue
            eco.add_species(name, cat)

    
    elif choice == "2":
        while True:  # วนลูปจนกว่าผู้ใช้จะพิมพ์ "ออก"
            print("\n🗑️ เมนูการลบสิ่งมีชีวิต")
            print("1️⃣ ลบสิ่งมีชีวิตเฉพาะตัว")
            print("2️⃣ ลบข้อมูลสิ่งมีชีวิตทั้งหมด")
            print("0️⃣ กลับไปหน้าหลัก")
            sub_choice = input("เลือกตัวเลือก: ").strip()

            if sub_choice == "1":
                show_current_species()
                name = input("กรอกชื่อสิ่งมีชีวิตที่ต้องการลบ: ").strip()
                eco.delete_species(name)

            elif sub_choice == "2":
                confirm = input("⚠️ คุณต้องการลบข้อมูลทั้งหมดหรือไม่? (พิมพ์ 'ยืนยัน'): ").strip()
                if confirm == "ยืนยัน":
                    clear_all_species()
                else:
                    print("❌ ยกเลิกการลบข้อมูลทั้งหมด")

            elif sub_choice == "0":
                break  # ออกจากเมนูการลบและกลับไปหน้าหลัก

            else:
                print("❌ เลือกตัวเลือกไม่ถูกต้อง กรุณาลองใหม่")

    elif choice == "3":
        eco.auto_generate_relationship()

    elif choice == "4":
        eco.analyze_ecosystem()

    
    elif choice == "5":
        if not eco.nodes:
            print("⚠️ ยังไม่มีข้อมูลสิ่งมีชีวิต กรุณาเพิ่มข้อมูลก่อนแสดงกราฟ")
        else:
            eco.draw_graph()

    elif choice == "9":
        print("\n📂 เลือกชุดข้อมูลตัวอย่าง:")
        print("1️⃣ ป่าเขตร้อน (10 ชนิด)")
        print("2️⃣ ทุ่งหญ้า (8 ชนิด)")
        print("3️⃣ ป่าดิบชื้น (12 ชนิด)")
        sub_choice = input("เลือกชุดข้อมูล (1-3): ").strip()
        if sub_choice in sample_datasets:
            for data in sample_datasets[sub_choice]:
                eco.add_species(data["name"], data["category"])
            print("✅ เพิ่มชุดข้อมูลตัวอย่างเรียบร้อย")
        else:
            print("❌ เลือกชุดข้อมูลไม่ถูกต้อง")

    
    elif choice == "6":
        show_current_species()
        old = input("กรอกชื่อสิ่งมีชีวิตที่ต้องการแก้ไข: ").strip()
        if old not in eco.nodes:
            print(f"❗️ ไม่พบ {old}")
            continue
        new = input("กรอกชื่อใหม่: ").strip()
        while True:
            print("ประเภท: ผู้ผลิต / กินพืช / กินเนื้อ / ย่อยสลาย")
            new_cat_input = input("กรอกประเภทใหม่: ").strip()
            if new_cat_input in valid_categories:
                new_cat = valid_categories[new_cat_input]
                break
            else:
                print("❗️ กรุณากรอกประเภทให้ถูกต้อง")
        eco.edit_species(old, new, new_cat)

    elif choice == "0":
        print("👋 ออกจากโปรแกรม...")
        break

    else:
        print("❌ เลือกเมนูไม่ถูกต้อง กรุณาลองใหม่")
