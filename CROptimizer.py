import tkinter as tk
from tkinter import messagebox, ttk, Canvas
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk # type: ignore
import time

class Card:
    def __init__(self, name, elixir_cost, damage):
        self.name = name
        self.elixir_cost = elixir_cost
        self.damage = damage

class ClashRoyaleOptimizer:
    def __init__(self, master):
        self.master = master
        self.master.title("Clash Royale Strategy Optimizer")

        bg_image = Image.open("Clash_Royale.jpeg")  
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        self.cards = []
        self.selected_cards = []
        self.max_elixir = 10

        self.create_widgets()

    def create_widgets(self):
        canvas = Canvas(self.master, width=800, height=600)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        self.info_label = tk.Label(canvas, text="Clash Royale Strategy Optimizer", font=("Helvetica", 20, "bold"), bg="lightblue", fg="black")
        self.info_label.place(relx=0.5, y=10, anchor="n")

        self.add_card_frame = tk.Frame(canvas, bg="lightblue")
        self.add_card_frame.place(relx=0.5, y=50, anchor="n")

        tk.Label(self.add_card_frame, text="Card Name:", font=("Helvetica", 12), bg="lightblue", fg="black").grid(row=0, column=0)
        tk.Label(self.add_card_frame, text="Elixir Cost:", font=("Helvetica", 12), bg="lightblue", fg="black").grid(row=0, column=1)
        tk.Label(self.add_card_frame, text="Damage:", font=("Helvetica", 12), bg="lightblue", fg="black").grid(row=0, column=2)

        self.card_name_entry = tk.Entry(self.add_card_frame, font=("Helvetica", 12), bg="white", fg="black", insertbackground="black")
        self.card_name_entry.grid(row=1, column=0)

        self.card_elixir_entry = tk.Entry(self.add_card_frame, font=("Helvetica", 12), bg="white", fg="black", insertbackground="black")
        self.card_elixir_entry.grid(row=1, column=1)

        self.card_damage_entry = tk.Entry(self.add_card_frame, font=("Helvetica", 12), bg="white", fg="black", insertbackground="black")
        self.card_damage_entry.grid(row=1, column=2)

        self.add_card_button = tk.Button(self.add_card_frame, text="Add Card", command=self.add_card, font=("Helvetica", 12), bg="lightgreen")
        self.add_card_button.grid(row=1, column=3, padx=10)

        self.delete_card_button = tk.Button(self.add_card_frame, text="Delete Selected", command=self.delete_card, font=("Helvetica", 12), bg="salmon", fg="black")
        self.delete_card_button.grid(row=1, column=4, padx=10)

        self.refresh_button = tk.Button(canvas, text="Refresh", command=self.refresh_game, font=("Helvetica", 12), bg="lightblue")
        self.refresh_button.place(relx=0.5, y=100, anchor="n")

        self.cards_listbox = tk.Listbox(canvas, selectmode=tk.MULTIPLE, width=50, height=10, font=("Helvetica", 12), bg="white", fg="black")
        self.cards_listbox.place(relx=0.5, y=150, anchor="n")

        self.elixir_label = tk.Label(canvas, text="Max Elixir:", font=("Helvetica", 14), bg="lightblue", fg="black")
        self.elixir_label.place(relx=0.5, y=380, anchor="n")

        self.elixir_entry = tk.Entry(canvas, font=("Helvetica", 12), bg="white", fg="black", insertbackground="black")
        self.elixir_entry.insert(0, str(self.max_elixir))
        self.elixir_entry.place(relx=0.5, y=410, anchor="n")

        self.optimize_button = tk.Button(canvas, text="Optimize Strategy", command=self.optimize_strategy, font=("Helvetica", 14), bg="lightblue")
        self.optimize_button.place(relx=0.5, y=450, anchor="n")

        self.result_text = ScrolledText(canvas, width=50, height=10, font=("Helvetica", 12), bg="white", fg="black")
        self.result_text.place(relx=0.5, y=490, anchor="n")

    def add_card(self):
        name = self.card_name_entry.get()
        try:
            elixir_cost = int(self.card_elixir_entry.get())
            damage = int(self.card_damage_entry.get())
            if elixir_cost <= 0 or damage <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Elixir Cost and Damage must be positive integers.")
            return

        new_card = Card(name, elixir_cost, damage)
        self.cards.append(new_card)
        self.cards_listbox.insert(tk.END, f"{new_card.name} (Elixir: {new_card.elixir_cost}, Damage: {new_card.damage})")

        self.card_name_entry.delete(0, tk.END)
        self.card_elixir_entry.delete(0, tk.END)
        self.card_damage_entry.delete(0, tk.END)

    def delete_card(self):
        selected_indices = self.cards_listbox.curselection()
        if not selected_indices:
            messagebox.showinfo("Info", "Select cards to delete.")
            return
        
        selected_indices = list(selected_indices)
        selected_indices.sort(reverse=True)  

        for index in selected_indices:
            del self.cards[index]
            self.cards_listbox.delete(index)

    def refresh_game(self):
        self.cards = []
        self.cards_listbox.delete(0, tk.END)
        self.elixir_entry.delete(0, tk.END)
        self.elixir_entry.insert(0, str(self.max_elixir))
        self.result_text.delete(1.0, tk.END)

    def optimize_strategy(self):
        try:
            max_elixir = int(self.elixir_entry.get())
            if max_elixir <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Max Elixir must be a positive integer.")
            return

        # Sort cards based on damage per elixir cost ratio (Greedy strategy)
        self.cards.sort(key=lambda x: x.damage / x.elixir_cost, reverse=True)

        current_elixir = 0
        best_strategy_greedy = []
        best_damage_greedy = 0

        for card in self.cards:
            if current_elixir + card.elixir_cost <= max_elixir:
                best_strategy_greedy.append(card)
                best_damage_greedy += card.damage
                current_elixir += card.elixir_cost

        result_text_greedy = f"Greedy Strategy with max {max_elixir} elixir:\n"
        for card in best_strategy_greedy:
            result_text_greedy += f"{card.name} (Elixir: {card.elixir_cost}, Damage: {card.damage})\n"
        result_text_greedy += f"Total Damage: {best_damage_greedy}\n"

        # Branch and Bound
        best_strategy_bb, best_damage_bb = self.branch_and_bound_knapsack(self.cards, max_elixir)

        result_text_bb = f"Branch and Bound Strategy with max {max_elixir} elixir:\n"
        for card in best_strategy_bb:
            result_text_bb += f"{card.name} (Elixir: {card.elixir_cost}, Damage: {card.damage})\n"
        result_text_bb += f"Total Damage: {best_damage_bb}\n"

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text_greedy)
        self.result_text.insert(tk.END, "\n")
        self.result_text.insert(tk.END, result_text_bb)

    def branch_and_bound_knapsack(self, cards, max_elixir):
        # Sort cards based on profit/weight ratio in descending order
        cards.sort(key=lambda x: x.damage / x.elixir_cost, reverse=True)

        n = len(cards)
        best_strategy = []
        best_damage = 0

        def bound(W, F, i):
            cost = F
            weight = W
            while i < n and weight + cards[i].elixir_cost <= max_elixir:
                weight += cards[i].elixir_cost
                cost += cards[i].damage
                i += 1
            if i < n:
                cost += (max_elixir - weight) * (cards[i].damage / cards[i].elixir_cost)
            return cost

        def explore(current_strategy, current_damage, current_elixir, index):
            nonlocal best_strategy, best_damage

            if current_elixir > max_elixir:
                return

            if index == n:
                if current_damage > best_damage:
                    best_strategy = list(current_strategy)
                    best_damage = current_damage
                return

            # Check if including current card is feasible
            if current_elixir + cards[index].elixir_cost <= max_elixir:
                current_strategy.append(cards[index])
                explore(current_strategy, current_damage + cards[index].damage, current_elixir + cards[index].elixir_cost, index + 1)
                current_strategy.pop()

            # Calculate upper bound (cost)
            cost_with_current = bound(current_elixir, current_damage, index + 1)
            if cost_with_current > best_damage:
                explore(current_strategy, current_damage, current_elixir, index + 1)

        explore([], 0, 0, 0)
        return best_strategy, best_damage

if __name__ == "__main__":
    root = tk.Tk()
    app = ClashRoyaleOptimizer(root)
    root.mainloop()