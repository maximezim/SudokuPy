import tkinter
from timeit import default_timer
import customtkinter
import generation as gn
import os
from tkinter import filedialog as fd

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    count = [0]
    pos = [1000,1000,1,2]
    difficulte = [1]
    WIDTH = 860
    HEIGHT = 530
    grille_vide= [[0 for w in range(9)] for z in range(9)]
    etat = [0]

    def __init__(self):
        super().__init__()
        #définition de la fenêtre
        self.title("Sudoku Sinoquet - Zimmermann")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # appelle .on_closing() à la fermeture
        self.iconbitmap(self, os.path.join(os.path.dirname(__file__), "sudoku.ico"))

        # ============ création de 2 frames ============

        # configure le layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure le layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)
        self.frame_left.grid_rowconfigure(9, weight=1)
        self.frame_left.grid_rowconfigure(10, minsize=20)  
        self.frame_left.grid_rowconfigure(11, minsize=10) 

        #définition des différents éléments du frame_left
        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Sudoku",
                                              text_font=("Roboto Medium", -16))
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Jouer",
                                                fg_color=("gray75", "gray30"),
                                                command=self.jouer_event)
        self.button_1.grid(row=4, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Résoudre",
                                                fg_color=("gray75", "gray30"),
                                                command=self.resoudre)
        self.button_2.grid(row=6, column=0, pady=10, padx=20)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Quitter",
                                                fg_color=("gray75", "gray30"),  
                                                command=self.on_closing)
        self.button_3.grid(row=8, column=0, pady=10, padx=20)

        self.button_clear = customtkinter.CTkButton(master=self.frame_left,
                                                text="Effacer",
                                                fg_color=("gray75", "gray30"),  
                                                command=self.effacer)
        self.button_clear.grid(row=7, column=0, pady=10, padx=20)

        self.button_5 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Valider",
                                                command=self.valider)
        self.button_5.grid(row=10, column=0, pady=10, padx=20)

        self.switch_2 = customtkinter.CTkSwitch(master=self.frame_left,
                                                text="Mode sombre",
                                                command=self.change_mode)
        self.switch_2.grid(row=11, column=0, pady=10, padx=20, sticky="w")

#switch de l'indice

        self.switch_3 = customtkinter.CTkSwitch(master=self.frame_left,
                                                text="Annotation",
                                                command=self.indice)
        self.switch_3.grid(row=13, column=0, pady=10, padx=20, sticky="w")



        self.slider_1 = customtkinter.CTkSlider(master=self.frame_left,
                                                from_=1,
                                                to=4,
                                                number_of_steps=3,
                                                command=self.value_changed)
        self.slider_1.grid(row=3, column=0, columnspan=1, pady=10, padx=20, sticky="we")

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Difficulté :",
                                              text_font=("Roboto Medium", -12))
        self.label_1.grid(row=2, column=0, pady=(10,0), padx=10)

        self.button_import = customtkinter.CTkButton(master=self.frame_left, text="Importer", fg_color=("gray75", "gray30"), command=self.import_event)
        self.button_import.grid(row=5, column=0, pady=10, padx=20)

        # ============ frame_right ============

        # configure le layout (3x7)
        self.frame_right.rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)
        self.frame_right.columnconfigure((0,1), weight=1)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=1, rowspan=10, pady=20, padx=20, sticky="nsew")
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)
        # valeurs par défaut
        self.switch_2.select()
        self.slider_1.set(1)

        #défintion des boutons
        self.b1 = customtkinter.CTkButton(master=self.frame_right,text="1",command=self.callbt1)
        self.b1.grid(row=0, column=1, pady=5, padx=10)
        self.b2 = customtkinter.CTkButton(master=self.frame_right,text="2",command=self.callbt2)
        self.b2.grid(row=1, column=1, pady=5, padx=10)
        self.b3 = customtkinter.CTkButton(master=self.frame_right,text="3",command=self.callbt3)
        self.b3.grid(row=2, column=1, pady=5, padx=10)
        self.b4 = customtkinter.CTkButton(master=self.frame_right,text="4",command=self.callbt4)
        self.b4.grid(row=3, column=1, pady=5, padx=10)
        self.b5 = customtkinter.CTkButton(master=self.frame_right,text="5",command=self.callbt5)
        self.b5.grid(row=4, column=1, pady=5, padx=10)
        self.b6 = customtkinter.CTkButton(master=self.frame_right,text="6",command=self.callbt6)
        self.b6.grid(row=5, column=1, pady=5, padx=10)
        self.b7 = customtkinter.CTkButton(master=self.frame_right,text="7",command=self.callbt7)
        self.b7.grid(row=6, column=1, pady=5, padx=10)
        self.b8 = customtkinter.CTkButton(master=self.frame_right,text="8",command=self.callbt8)
        self.b8.grid(row=7, column=1, pady=5, padx=10)
        self.b9 = customtkinter.CTkButton(master=self.frame_right,text="9",command=self.callbt9)
        self.b9.grid(row=8, column=1, pady=5, padx=10)
        self.b0 = customtkinter.CTkButton(master=self.frame_right,text="Supprimer",command=self.bt0)
        self.b0.grid(row=9, column=1, pady=5, padx=10)

        #définition du canvas
        self.can = customtkinter.CTkCanvas(master=self.frame_info, width=426, height=426)
        self.can.grid(row=1, column=0, sticky="we", padx=(20, 20), pady=20)
        self.can.create_rectangle(3,3,426,426, width=3, fill="white")
        #on trace la grille
        for i in range(3,426,47):
            w=1
            if i==144 or i==285:
                w=2
            self.can.create_line(i,3,i,426, width=w)
            self.can.create_line(3,i,426,i, width=w)

        #définition de l'horloge
        self.can2= customtkinter.CTkCanvas(master=self.frame_info, width=40, height=20)
        self.can2.config(highlightthickness=0)
        self.can2.grid(row=0, column=0, sticky="we", padx=(20, 20), pady=20)
        self.text_clock = (self.can2).create_text(40, 10, anchor=tkinter.CENTER)
        

        self.can.bind("<Button-1>", self.button_event2)
        #bind le clavier et la souris à la fenêtre
        self.can.focus_set()
        self.can.bind("<Key>", self.f)
        
    # ============ fonctions ============

    #fonction pour changer la difficulté
    def value_changed(self, value):
        self.difficulte = value


    #permet de mettre en avant la case sur laquelle on se situe 
    def button_event2(self, event):
        (i,j) = (event.x, event.y)
        if i != self.pos[0] or j != self.pos[1]:
            self.pos[2] = self.pos[0]
            self.pos[3] = self.pos[1]
            #clear position of previous cell
            try:
                self.can.delete(self.rec)
            except:
                pass
            self.pos = [i-4,j-4,self.pos[2],self.pos[3]]
            self.rec=self.can.create_rectangle(27+(self.pos[0]//47)*47-20,27+(self.pos[1]//47)*47-20,27+(self.pos[0]//47)*47+20,27+(self.pos[1]//47)*47+20, fill="blue", width=0, stipple="gray50")

            try:
                if self.grille_vide[self.pos[2]//47][self.pos[3]//47] != 0:
                    self.can.create_text(27+(self.pos[2]//47)*47,27+(self.pos[3]//47)*47, text=self.grille_vide[self.pos[2]//47][self.pos[3]//47], fill="black", font=("Arial", 20))
                    try:
                        if self.grid_original[self.pos[2]//47][self.pos[3]//47] != 0:
                            self.can.create_text(27+(self.pos[2]//47)*47,27+(self.pos[3]//47)*47, text=self.grid_original[self.pos[2]//47][self.pos[3]//47], fill="blue", font=("Arial", 20))
                    except:
                        pass
            except:
                pass


    #assigne l'entrée du clavier à la fonction bt
    def f(self, event):
        t=event.keysym
        if (t<='9' and t>='0'):
            if t=='0':
                self.bt0()
            else:
                self.bt(int(t))

    #efface le canva et le recréé avec une grille vide
    def effacer(self):
        self.can.delete("all")
        self.can.create_rectangle(3,3,426,426, width=3, fill="white")
        for i in range(3,426,47):
            w=1
            if i==144 or i==285:
                w=2
            self.can.create_line(i,3,i,426, width=w)
            self.can.create_line(3,i,426,i, width=w)
        self.grille_vide= [[0 for w in range(9)] for z in range(9)]

    #appelle une génération de grille et l'affiche
    def jouer_event(self):
        self.start = default_timer()
        diff = self.difficulte
        print("jouer_event:", diff)
        if diff == 1.0:
            self.gridToPlay = gn.grille_joueur(43)
        elif diff == 2.0:
            self.gridToPlay = gn.grille_joueur(51)
        elif diff == 3.0:
            self.gridToPlay = gn.grille_joueur(56)
        elif diff == 4.0:
            self.gridToPlay = gn.grille_joueur(63)
        self.grid_original = [[self.gridToPlay[x][y] for y in range(len(self.gridToPlay[0]))] for x in range(len(self.gridToPlay))]
        self.grille_vide = [[self.gridToPlay[x][y] for y in range(len(self.gridToPlay[0]))] for x in range(len(self.gridToPlay))]
        self.can.delete("all")
        self.can = customtkinter.CTkCanvas(master=self.frame_info, width=426, height=426)
        self.can.grid(row=1, column=0, sticky="we", padx=(20, 20), pady=20)
        self.can.create_rectangle(3,3,426,426, width=3, fill="white")
        for i in range(3,426,47):
            w=1
            if i==144 or i==285:
                w=2
            self.can.create_line(i,3,i,426, width=w)
            self.can.create_line(3,i,426,i, width=w)
        for i in range(9):
            for j in range(9):
                if self.grid_original[i][j] != 0:
                    self.can.create_text(27+i*47,27+j*47, text=str(self.grid_original[i][j]), font=("Arial", 20), fill="blue")
        self.can.bind("<Button-1>", self.button_event2)
        self.can.focus_set()
        self.can.bind("<Key>", self.f)

    #appelle la fonction solution et affiche les cases résolues en rouge
    def resoudre(self):
        sol = gn.solution(self.grille_vide,0,0)
        if sol != False:
            for i in range(9):
                for j in range(9):
                    if sol[i][j] != self.grille_vide[i][j]:
                        self.can.create_text(27+i*47,27+j*47, text=str(sol[i][j]), font=("Arial", 20), fill="red")
                        self.grille_vide[i][j] = sol[i][j]


    def valider(self):
        #en cas de réussite
        if self.grille_vide == gn.solution(self.grid_original,0,0):
            #create rectangle behind
            self.can.create_rectangle(80,162,340,262, width=0, fill="white")
            self.can.create_text(212,212, text="Bravo", font=("Arial", 50), fill="pink")
        #en cas d'échec
        else:
            for i in range(3,426,47):
                w=1
                if i==144 or i==285:
                    w=2
                self.can.create_line(i,3,i,426, width=w, fill="red")
                self.can.create_line(3,i,426,i, width=w, fill="red")
        #sauvegarde la grille dans le fichier grille.txt dans le répertoire courant
        basedir = os.path.dirname(os.path.abspath(__file__))
        categorization_file = os.path.join(basedir,'grille.txt')
        f = open(categorization_file, 'w')
        for i in range(9):
            for j in range(9):
                if j !=8:
                    f.write(str(self.grille_vide[j][i]) + " ")
                else:
                    f.write(str(self.grille_vide[j][i]))
            f.write("\n")
        f.close()
        
    
    def change_mode(self):
        #change l'apparence de la fenêtre
        if self.switch_2.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def on_closing(self, event=0):
        self.destroy()

    start = default_timer()

    def updateTime(self):
        #permet de gérer le chronomètre
        now = default_timer() - self.start
        minutes, seconds = divmod(now, 60)
        hours, minutes = divmod(minutes, 60)
        str_time = "%d:%02d:%02d" % (hours, minutes, seconds)
        self.can2.itemconfigure((self.text_clock), text=str_time)
        self.frame_info.after(1000, self.updateTime)
        

    def indice(self):
        #permet de mettre de schiffres en annotation
        if self.switch_3.get() == 1:
            self.etat[0]=1
        else:
            self.etat[0]=0


    def bt(self, nbr):
        #affiche le nombre en annotation ou non
        if self.etat[0]==1:
            self.rep_indice(nbr)
        else:
            if self.pos[0] != 0 and self.pos[1] != 0 and gn.CheckValid(self.grille_vide, self.pos[0]//47, self.pos[1]//47, nbr):
                self.can.create_rectangle(27+(self.pos[0]//47)*47-21,27+(self.pos[1]//47)*47-21,27+(self.pos[0]//47)*47+21,27+(self.pos[1]//47)*47+21, fill="white", width=0)
                self.can.create_text(27+(self.pos[0]//47)*47,27+(self.pos[1]//47)*47, text=str(nbr), font=("Arial", 20), fill="black")
                self.grille_vide[(self.pos[0]//47)][(self.pos[1]//47)] = nbr
            #en rouge si le nombre n'est pas valide :
            elif self.pos[0] != 0 and self.pos[1] != 0 and not gn.CheckValid(self.grille_vide, self.pos[0]//47, self.pos[1]//47, nbr):
                self.can.create_rectangle(27+(self.pos[0]//47)*47-21,27+(self.pos[1]//47)*47-21,27+(self.pos[0]//47)*47+21,27+(self.pos[1]//47)*47+21, fill="white", width=0)
                self.can.create_text(27+(self.pos[0]//47)*47,27+(self.pos[1]//47)*47, text=str(nbr), font=("Arial", 20), fill="red")
                self.grille_vide[(self.pos[0]//47)][(self.pos[1]//47)] = nbr
        


    def rep_indice(self,nb):
        if self.pos[0] != 0 and self.pos[1] != 0:
                self.can.create_text(10+15*((nb-1)%3)+(self.pos[0]//47)*47,10+15*((nb-1)//3)+(self.pos[1]//47)*47, text=nb, font=("Arial", 7), fill="black")

    #--------- fonctions pour mettre les chiffres dans la grille ----------#
    def callbt1(self):
            self.bt(1)
    
    def callbt2(self):
        if self.etat[0]==1: 
            self.rep_indice(2)
        else:
            self.bt(2)
    
    def callbt3(self):
        if self.etat[0]==1: 
            self.rep_indice(3)
        else:
            self.bt(3)
    
    def callbt4(self):
        if self.etat[0]==1: 
            self.rep_indice(4)
        else:
            self.bt(4)
    
    def callbt5(self):
        if self.etat[0]==1: 
            self.rep_indice(5)
        else:
            self.bt(5)
    
    def callbt6(self):
        if self.etat[0]==1: 
            self.rep_indice(6)
        else:
            self.bt(6)
    
    def callbt7(self):
        if self.etat[0]==1: 
            self.rep_indice(7)
        else:
            self.bt(7)
    
    def callbt8(self):
        if self.etat[0]==1: 
            self.rep_indice(8)
        else:
            self.bt(8)
    
    def callbt9(self):
        if self.etat[0]==1: 
            self.rep_indice(9)
        else:
            self.bt(9)

    def bt0(self):
        if self.pos[0] != 0 and self.pos[1] != 0:
            self.can.create_rectangle(27+(self.pos[0]//47)*47-22,27+(self.pos[1]//47)*47-22,27+(self.pos[0]//47)*47+20,27+(self.pos[1]//47)*47+20, fill="white", width=0)
            self.grille_vide[(self.pos[0]//47)][(self.pos[1]//47)] = 0
        

    def import_event(self):
        #importe une grille en format txt
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        with open(filename) as f:
            grid_data = [i.split() for i in f.readlines()]
            for x in grid_data:
                #essaye de convertir en entier
                for i in range(9):
                    try:
                        x[i] = int(x[i])
                    except ValueError:
                        self.can.create_rectangle(80,162,340,262, width=0, fill="white")
                        self.can.create_text(212,212, text="Non valide", font=("Arial", 30), fill="pink")
                        return False
                    except IndexError:
                        self.can.create_rectangle(80,162,340,262, width=0, fill="white")
                        self.can.create_text(212,212, text="Non valide", font=("Arial", 30), fill="pink")
                        return False
                    if x[i] > 9 or x[i] < 0:
                        return False
        reversegrid = [[0 for i in range(9)] for j in range(9)]
        #change le sens de la grile
        for i in range(9):
            for j in range(9):
                reversegrid[j][i] = grid_data[i][j]

        if gn.solution(reversegrid, 0, 0)== False:
            #dit si la grille n'est pas valide
            self.can.create_rectangle(80,162,340,262, width=0, fill="white")
            self.can.create_text(212,212, text="Non valide", font=("Arial", 30), fill="pink")
            print("La grille n'est pas valide")
            return False
        self.grid_original = [[reversegrid[x][y] for y in range(len(reversegrid[0]))] for x in range(len(reversegrid))]
        self.grille_vide = [[reversegrid[x][y] for y in range(len(reversegrid[0]))] for x in range(len(reversegrid))]
        self.can.delete("all")
        self.can = customtkinter.CTkCanvas(master=self.frame_info, width=426, height=426)
        self.can.grid(row=1, column=0, sticky="we", padx=(20, 20), pady=20)
        self.can.create_rectangle(3,3,426,426, width=3, fill="white")
        for i in range(3,426,47):
            w=1
            if i==144 or i==285:
                w=2
            self.can.create_line(i,3,i,426, width=w)
            self.can.create_line(3,i,426,i, width=w)
        
        for i in range(9):
            for j in range(9):
                if self.grid_original[i][j] != 0:
                    self.can.create_text(27+i*47,27+j*47, text=str(self.grid_original[i][j]), font=("Arial", 20), fill="blue")
        self.can.bind("<Button-1>", self.button_event2)
        self.can.focus_set()
        self.can.bind("<Key>", self.f)
        self.start = default_timer()

if __name__ == "__main__":
    app = App()
    app.updateTime()
    app.mainloop()