import tkinter as tk

suma = 0.0

prieteni_list = []

with open("suma.txt", "r") as f:
    try:
        suma = float(f.read())
    except ValueError:
        suma = 0.0

def adauga_bani():
    global suma

    suma_adaugata = entry_adaugare_bani.get()
    try:
        valoare = float(suma_adaugata)
        suma += valoare
        with open("tranzactii.txt", "a") as f:
            f.write(f"{valoare} RON adaugati\n")
            f.close()
        entry_adaugare_bani.delete(0, tk.END)
        label_suma.config(text=f"Suma curentă: {suma:.2f} RON", fg="black")
        label_eroare.config(text="")
        with open("suma.txt", "w") as f:
            f.write(f"{str(suma)} RON adaugati")
    except ValueError:
        label_eroare.config(text="Introduceți un număr valid!", fg="red")
        entry_adaugare_bani.delete(0, tk.END)

def extrage_bani():
    global suma 

    suma_extrasa = entry_extras_bani.get()
    try:
        valoare = float(suma_extrasa)
        if valoare > suma:
            label_eroare.config(text="Fonduri insuficiente!", fg="red")
        else:
            suma -= valoare
            with open("tranzactii.txt", "a") as f:
                f.write(f"{valoare} RON extrasi\n")
                f.close()
            entry_extras_bani.delete(0, tk.END)
            label_suma.config(text=f"Suma curentă: {suma:.2f} RON", fg="black")
            label_eroare.config(text="")
            with open("suma.txt", "w") as f:
                f.write(f"{suma} RON retrasi")
    except ValueError:
        label_eroare.config(text="Introduceți un număr valid!", fg="red")
        entry_extras_bani.delete(0, tk.END)

def plateste():
    global suma

    suma_platita = entry_suma_platita.get()
    try:
        valoare = float(suma_platita)
        if valoare > suma:
            label_eroare.config(text="Fonduri insuficiente!", fg="red")
        else:
            if entry_plati.get() != "":
                suma -= valoare
                with open("tranzactii.txt", "a") as f:
                    f.write(f"{entry_plati.get()}: {valoare} RON\n")
                    f.close()
                entry_suma_platita.delete(0, tk.END)
                entry_plati.delete(0, tk.END)  
                label_suma.config(text=f"Suma curentă: {suma:.2f} RON", fg="black")
                label_eroare.config(text="")
                with open ("tranzactii.txt", "w") as f:
                    f.write(f"{entry_plati.get()}: {valoare} RON\n")
                    f.close()
            else :
                label_eroare.config(text="Introduceți un nume pentru plată!", fg="red")
                entry_suma_platita.delete(0, tk.END)
    except ValueError:
        label_eroare.config(text="Introduceți un număr valid!", fg="red")
        entry_suma_platita.delete(0, tk.END)


def deschide_fereastra():
    fereastra_noua = tk.Toplevel(window)
    fereastra_noua.title("Transfer bani")
    fereastra_noua.geometry("300x300")

    variable_check = tk.IntVar()

    def load_tranzactii():
        try:
            with open ("tranzactii.txt", "a") as f:
                f.write(f"{entry_nou.get()}: {entry_bani_transferati.get()} RON\n")
                f.close()
        except FileNotFoundError:
            label_eroare.config(text="Fișierul tranzactii.txt nu a fost găsit!", fg="red")
            entry_nou.delete(0, tk.END)
            entry_bani_transferati.delete(0, tk.END)
    
    def load_prieteni(name):
        try:
            with open("prieteni.txt", "r") as f:
                ok = 0
                for line in f:
                    if line.strip() == name:
                        ok = 1
                
                if ok == 1:
                    label_eroare.config(text="Prietenul există deja!", fg="red")
                    entry_nou.delete(0, tk.END)
                else :
                    label_eroare.config(text="Transfer realizat!", fg="green")
                    with open ("prieteni.txt", "a") as f:
                        f.write(name + "\n")
                        f.close()
                    entry_nou.delete(0, tk.END)
                    entry_bani_transferati.delete(0, tk.END)
                    
        except FileNotFoundError:
            label_eroare.config(text="Fișierul prieteni.txt nu a fost găsit!", fg="red")
            entry_nou.delete(0, tk.END)
            entry_bani_transferati.delete(0, tk.END)


    def transfer_bani_prieten():
        global suma
        suma_transferata = entry_bani_transferati.get()
        iban_transferat = entry_iban.get()

        prieteni_list = []
        iban_list = []

        with open("prieteni.txt", "r") as f:
            for line in f:
                campuri = line.strip().split(",")
                if len(campuri) >= 2:
                    nume = campuri[0]
                    iban = campuri[1]
                    prieteni_list.append(nume)
                    iban_list.append(iban)

        
        try:
            valoare = float(suma_transferata)
            if valoare > suma:
                label_eroare.config(text="Fonduri insuficiente!", fg="red")
                entry_bani_transferati.delete(0, tk.END)
            else:
                if entry_nou.get() == "":
                    label_eroare.config(text="Introduceți un nume pentru transfer!", fg="red")
                    entry_bani_transferati.delete(0, tk.END)
                    entry_nou.delete(0, tk.END)
                else:
                    if entry_iban.get() == "":
                            label_eroare.config(text="Introduceți un IBAN!", fg="red")
                            entry_bani_transferati.delete(0, tk.END)
                            entry_nou.delete(0, tk.END)
                            
                    else:
                        if entry_nou.get() not in prieteni_list:
                            label_eroare.config(text="Prietenul nu există!", fg="red")
                            entry_bani_transferati.delete(0, tk.END)
                            entry_nou.delete(0, tk.END)
                        else:
                            index_prieten = prieteni_list.index(entry_nou.get())
                            if iban_list[index_prieten] != entry_iban.get():
                                label_eroare.config(text="IBAN-ul gresit!", fg="red")
                                entry_bani_transferati.delete(0, tk.END)
                                entry_nou.delete(0, tk.END)
                                entry_iban.delete(0, tk.END)
                            else:
                                    label_eroare.config(text="")
                                    suma -= valoare
                                    load_tranzactii()
                                    entry_bani_transferati.delete(0, tk.END)
                                    label_suma.config(text=f"Suma curentă: {suma:.2f} RON", fg="black")
                                    entry_iban.delete(0, tk.END)
                                    label_eroare.config(text="Transfer realizat!", fg="green")
                                    entry_nou.delete(0, tk.END)
                                
        except ValueError:
            label_eroare.config(text="Introduceți un număr valid!", fg="red")
            entry_bani_transferati.delete(0, tk.END)

        

    label_nou = tk.Label(fereastra_noua, text="Transfer catre:")
    label_nou.grid(row=0, column=0, padx=10, pady=10)

    entry_nou = tk.Entry(fereastra_noua)
    entry_nou.grid(row=0, column=1, padx=10, pady=10)

    label_suma_transferata = tk.Label(fereastra_noua, text="Suma transferată:")
    label_suma_transferata.grid(row=1, column=0, padx=10, pady=10)

    entry_bani_transferati = tk.Entry(fereastra_noua)
    entry_bani_transferati.grid(row=1, column=1, padx=10, pady=10)

    label_iban = tk.Label(fereastra_noua, text="IBAN:")
    label_iban.grid(row=2, column=0, padx=10, pady=10)

    entry_iban = tk.Entry(fereastra_noua)
    entry_iban.grid(row=2, column=1, padx=10, pady=10)

    button_transfer_bani = tk.Button(fereastra_noua, text="Transferă", command=transfer_bani_prieten)
    button_transfer_bani.grid(row=4, column=0, columnspan=2, pady=10, padx=10)

    label_eroare = tk.Label(fereastra_noua, text="")
    label_eroare.grid(row=5, column=0, columnspan=2)

def deschide_fereastra_detalii():
    fereastra_detalii = tk.Toplevel(window)
    fereastra_detalii.title("Detalii cont")
    fereastra_detalii.geometry("300x200")

    label_detalii = tk.Label(fereastra_detalii, text="Detalii cont:")
    label_detalii.pack(pady=10)

    label_suma = tk.Label(fereastra_detalii, text=f"Suma curentă: {suma:.2f} RON")
    label_suma.pack(pady=5)

    label_nume = tk.Label(fereastra_detalii, text="Nume: Ion Popescu")
    label_nume.pack(pady=5)

    label_iban = tk.Label(fereastra_detalii, text="IBAN: RO49AAAA1B31007593840000")
    label_iban.pack(pady=5)

window = tk.Tk()
window.title("Bank App")
window.geometry("400x400")

label_adaugare_bani = tk.Label(window, text="Adăugare bani:")
label_adaugare_bani.grid(row=1, column=0, padx=10, pady=10)

label_extras_bani = tk.Label(window, text="Extrage bani:")
label_extras_bani.grid(row=2, column=0, padx=10, pady=10)

label_plata = tk.Label(window, text="Plătește catre:")
label_plata.grid(row=3, column=0, padx=10, pady=10)

entry_adaugare_bani = tk.Entry(window)
entry_adaugare_bani.grid(row=1, column=1, padx=10, pady=10)

entry_extras_bani = tk.Entry(window)
entry_extras_bani.grid(row=2, column=1, padx=10, pady=10)

entry_plati = tk.Entry(window)
entry_plati.grid(row=3, column=1, padx=10, pady=10)

entry_suma_platita = tk.Entry(window)
entry_suma_platita.grid(row=4, column=1, padx=10, pady=10)

button_adaugare = tk.Button(window, text="Adaugă", command=adauga_bani)
button_adaugare.grid(row=1, column=2, padx=10, pady=10)

button_extras = tk.Button(window, text="Extrage" ,command=extrage_bani)  
button_extras.grid(row=2, column=2, padx=10, pady=10)

button_plati = tk.Button(window, text="Plătește", command=plateste)
button_plati.grid(row=3, column=2, padx=10, pady=10)

button_transfer = tk.Button(window, text="Transfer nou", command=deschide_fereastra)
button_transfer.grid(row=5, column=1, padx=10, pady=10)

button_share_detalii = tk.Button(window, text="Detalii", command=deschide_fereastra_detalii)
button_share_detalii.grid(row=5, column=0, padx=10, pady=10)

label_suma = tk.Label(window, text=f"Suma curentă: {suma} RON")
label_suma.grid(row=0, column=0, columnspan=3, pady=10)

label_eroare = tk.Label(window, text="")
label_eroare.grid(row=6, column=0, columnspan=3)

label_suma_plata = tk.Label(window, text="Suma de:")
label_suma_plata.grid(row=4, column=0, padx=10, pady=10)


window.mainloop()

with open("suma.txt", "w") as f:
    f.write(str(suma))
