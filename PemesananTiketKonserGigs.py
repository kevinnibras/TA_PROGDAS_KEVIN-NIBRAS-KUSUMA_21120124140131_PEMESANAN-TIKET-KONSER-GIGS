import tkinter as tk
from tkinter import messagebox
from collections import deque

# Manager tiket dengan stack dan queue
class TicketManager:
    def __init__(self):
        # Struktur data tiket: stack untuk setiap kategori
        self.tickets = {
            "VIP": [200],
            "Regular": [300],
            "Economy": [400]
        }
        self.queue = []  # Queue untuk antrean pembeli
    def get_vip (self):
        return self.tickets ["VIP"]
    def get_regular (self):
        return self.tickets ["Regular"]
    def get_economy (self):
        return self.tickets ["Economy"]
    def add_ticket(self, category, price, count):
        for i in range(count):
            ticket = {"category": category, "price": price, "id": f"{category}#{i+1}"}
            self.tickets[category].append(ticket)

    def sell_ticket(self, buyer, category, amount):
        if len(self.tickets[category]) >= amount:
            purchased_tickets = []
            for _ in range(amount):
                purchased_tickets.append(self.tickets[category].pop())
            self.queue.append((buyer, purchased_tickets))
            return purchased_tickets
        else:
            return None

# Aplikasi GUI dengan OOP
class ConcertApp:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager

        self.root.title("Pemesanan Tiket Konser")
        self.root.geometry("500x500")


        self.jumlah_vip = 200
        self.jumlah_regular = 300
        self.jumlah_economy = 400

        self.kuota_label = tk.Label(root, text="Kuota Tiket Tersedia:", font=("Arial", 12))
        self.kuota_label.pack()

        self.kuota_vip_label = tk.Label(root, text=f"VIP: 200 tiket")
        self.kuota_vip_label.pack()

        self.kuota_regular_label = tk.Label(root, text=f"Regular: 300 tiket")
        self.kuota_regular_label.pack()

        self.kuota_economy_label = tk.Label(root, text=f"Economy: 400 tiket")
        self.kuota_economy_label.pack()
        
        
        self.name_label = tk.Label(root, text="Masukkan Nama:")#ketik nama
        self.name_label.pack()
        self.name_entry = tk.Entry(root)
        self.name_entry.pack()
        
        self.artis_label = tk.Label(root, text ="Pilih artis")
        self.artis_label.pack()#milih artis

        self.artis_var = tk.StringVar(value="The Adams")
        self.satu_radio = tk.Radiobutton(root, text="The Adams", variable=self.artis_var ,value="The Adams")
        self.satu_radio.pack()
        self.dua_radio = tk.Radiobutton(root, text="Superman Is Dead", variable=self.artis_var ,value="Superman Is Dead")
        self.dua_radio.pack()
        
        self.category_label = tk.Label(root, text="Pilih Kategori:")
        self.category_label.pack()#milih kategori

        self.category_var = tk.StringVar(value="VIP")
        self.vip_radio = tk.Radiobutton(root, text="VIP (Rp 1.000.000)", variable=self.category_var, value="VIP")
        self.vip_radio.pack()
        self.regular_radio = tk.Radiobutton(root, text="Regular (Rp 500.000)", variable=self.category_var, value="Regular")
        self.regular_radio.pack()
        self.economy_radio = tk.Radiobutton(root, text="Economy (Rp 200.000)", variable=self.category_var, value="Economy")
        self.economy_radio.pack()

        self.amount_label = tk.Label(root, text="Jumlah Tiket:")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(root)
        self.amount_entry.pack()#ketik jumlah tiket

        self.order_button = tk.Button(root, text="Pesan Tiket", command=self.order_ticket)
        self.order_button.pack()#tombol pesen

        self.queue_button = tk.Button(root, text="Lihat Antrean", command=self.view_queue)
        self.queue_button.pack() #tombol antri

        
        self.message_label = tk.Label(root, text="") #buat pesen
        self.message_label.pack()

    def order_ticket(self):
        name = self.name_entry.get()
        artis = self.artis_var.get()
        category = self.category_var.get()
        try:
            amount = int(self.amount_entry.get())
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Jumlah tiket harus berupa angka positif!")
            return

        if not name.strip():
            messagebox.showerror("Error", "Nama tidak boleh kosong!")
            return

        tickets = self.manager.sell_ticket(name, category, amount)
        if tickets:
            total_price = sum(ticket["price"] for ticket in tickets)
            if category== "VIP":
                self.jumlah_vip -= amount
                self.kuota_vip_label.config(
                    text=f"VIP: {self.jumlah_vip} tiket"
                )
            elif category== "Regular":
                self.jumlah_regular -= amount
                self.kuota_regular_label.config(
                    text=f"Regular: {self.jumlah_regular}tiket"
                )
            elif category== "Economy":
                self.jumlah_economy -= amount
                self.kuota_economy_label.config(
                    text=f"Economy: {self.jumlah_economy}tiket"
                )
            ticket_ids = ", ".join(ticket["id"] for ticket in tickets)
            self.message_label.config(
                text=f"Tiket berhasil dipesan!\nNama: {name}\nArtis: {artis}\nKategori: {category}\nJumlah: {amount}\nTotal Harga: Rp {total_price:,}\nTiket: {ticket_ids}"
            )
        else:
            self.message_label.config(
                text=f"Maaf, tiket kategori {category} tidak mencukupi atau habis!"
            )

    def view_queue(self):
        if self.manager.queue:
            queue_list = "\n".join([
                f"{buyer} - {', '.join(ticket['id'] for ticket in tickets)} ({len(tickets)} tiket)"
                for buyer, tickets in self.manager.queue
            ])
            messagebox.showinfo("Antrean Pembeli", queue_list)
        else:
            messagebox.showinfo("Antrean Pembeli", "Belum ada antrean.")


manager = TicketManager() #buat inisiasi data tiket
manager.add_ticket("VIP", 1000000, 200)  # 200 tiket VIP
manager.add_ticket("Regular", 500000, 300)  # 300 tiket Regular
manager.add_ticket("Economy", 200000, 400)  # 400 tiket Economy

root = tk.Tk() #buat jalanin aplikasi
app = ConcertApp(root, manager)
root.mainloop()
