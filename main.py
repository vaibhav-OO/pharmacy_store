import tkinter as tk
from tkinter import ttk
from datetime import datetime
import pymysql

#Design part
class pharmacy():
    def __init__(self,root):
        self.root = root
        self.root.title("Pharamcy managment")

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")

        title = tk.Label(self.root, text="Medicine Management System", bd=4,
                         relief="groove", font=("Arial",50,"bold"), bg=self.clr(240,150,200))
        title.pack(side="top", fill="x")


        #add Frame
        addFrame = tk.Frame(self.root, bd=4, relief="ridge", bg=self.clr(200, 240, 150))
        addFrame.place(width=self.width/3, height=self.height-180, x=20, y=100)

        #nameLabel
        nameLbl = tk.Label(addFrame, text="Medicine:", bg=self.clr(200, 240, 150), font=("Arail",15,"bold"))
        nameLbl.grid(row=0, column=0, padx=20, pady=30)
        self.nameIn = tk.Entry(addFrame, bd=2, width=20, font=("Arial", 15))
        self.nameIn.grid(row=0, column=1, padx=10, pady=30)

        #Pricelabel
        priceLbl = tk.Label(addFrame, text="Price:", bg=self.clr(200, 240, 150), font=("Arail",15,"bold"))
        priceLbl.grid(row=1, column=0, padx=20, pady=30)
        self.priceIn = tk.Entry(addFrame, bd=2, width=20, font=("Arial", 15))
        self.priceIn.grid(row=1, column=1, padx=10, pady=30)

        #total customer
        quantLbl = tk.Label(addFrame, text="Quantity:", bg=self.clr(200, 240, 150), font=("Arail",15,"bold"))
        quantLbl.grid(row=2, column=0, padx=20, pady=30)
        self.quantIn = tk.Entry(addFrame, bd=2, width=20, font=("Arial", 15))
        self.quantIn.grid(row=2, column=1, padx=10, pady=30)

        #expiry date
        expLbl = tk.Label(addFrame, text="Expiry date:", bg=self.clr(200, 240, 150), font=("Arail",15,"bold"))
        expLbl.grid(row=3, column=0, padx=20, pady=30)
        self.expIn = tk.Entry(addFrame, bd=2, width=20, font=("Arial",15))
        self.expIn.grid(row=3, column=1, padx=10, pady=30)

        #Button
        addBtn = tk.Button(addFrame, text="Add Medicine", bd=2, relief="raised", font=("Arial", 20,"bold"),width=20)
        addBtn.grid(row=4, column=0, padx=30, pady=40, columnspan=2)


        #DEtail frame
        self.detFrame = tk.Frame(self.root, bd=4, relief="ridge", bg=self.clr(220,200,240))
        self.detFrame.place(width=self.width/2-100, height=self.height-180, x=self.width/3+40, y=100)
        
        lbl = tk.Label(self.detFrame, text="Detail", bg="gray", bd=3, relief="groove", font=("Arial",20,"bold"))
        lbl.pack(side="top", fill="x")
        self.tabfun()

        #Optional frame Buttons
        optFrame = tk.Frame(self.root, bd=4, relief="ridge",bg=self.clr(200,240,150))
        optFrame.place(width=self.width/2-200, height=self.height-180, x=self.width/3+self.width/2-40, y=100)

        searchBtn = tk.Button(optFrame , text="Search", width=10, font=("Arial",20,"bold"), bg="gray")
        searchBtn.grid(row=0, column=0, padx=10, pady=25)

        allBtn = tk.Button(optFrame, text="Show all", width=10, font=("Arail", 20, "bold"),bg="gray")
        allBtn.grid(row=1, column=0, padx=20, pady=25)

        quantBtn = tk.Button(optFrame, text="Add Quantity", width=10, font=("Arial", 20, "bold"),bg="gray")
        quantBtn.grid(row=2, column=0, padx=20, pady=25)

        purBtn = tk.Button(optFrame, text="Purcharse", width=10, font=("Arial", 20, "bold"),bg="gray")
        purBtn.grid(row=3, column=0, padx=20, pady=25)

        closeBtn = tk.Button(optFrame, text="Exit", width=10, font=("Arial", 20, "bold"),bg="gray")
        closeBtn.grid(row=4, column=0, padx=20, pady=25)

    def insertFun(self):
        name = self.nameIn.get()
        price = int(self.priceIn.get())
        quant = int(self.quantIn.get())
        exp = self.expIn.get()
        expDate = datetime.strptime(exp, "%Y-%m-%d")

        if name and price and quant and expDate:
            try:
                self.dbFun()
                query = f"insert into pharmacy(name, price, quant, exp) values(%s,%s,%s,%s)"
                self.cur.execute(query, (name,price,quant,expDate))
                self.con.commit()
                tk.messagebox.showinfo("Success",f"{name} medicine is added successfull")

            except Exception as e:
                tk.messagebox.showerror("Error", f"Error: {e}")

        else:
            tk.messagebox.showerror("Error","Fill all Input Fields")


    def dbFun(self):
        self.con = pymysql.connect(host="localhost", user="root", passwd="admin", database="rec")
        self.cur.execute(())


    def clr(self,r,g,b):
        return f"#{r:02x}{g:02x}{b:02x}"

    def tabfun(self):
        tabFrame = tk.Frame(self.detFrame, bd=4, relief="sunken", bg="cyan")
        tabFrame.place(width=self.width/2-140, height=self.height-270, x=20, y=70)

        x_scrol = tk.Scrollbar(tabFrame,orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")

        y_scrol = tk.Scrollbar(tabFrame, orient="vertical")
        y_scrol.pack(side="right", fill="y")

        self.table = ttk.Treeview(tabFrame, columns=("name","price","quant","exp"), xscrollcommand=x_scrol.set, yscrollcommand=y_scrol.set)

        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)
        
        self.table.heading("name", text="Medicine")
        self.table.heading("price", text="price")
        self.table.heading("quant",text="quant")
        self.table.heading("exp", text="exp")
        self.table["show"]= "headings"

        self.table.column("name", width=150)
        self.table.column("price",width=150)
        self.table.column("quant",width=150)
        self.table.column("exp",width=150)

        self.table.pack(fill="both", expand=1)

        self.table.pack(fill="both", expand=1)















root = tk.Tk()
obj = pharmacy(root)
root.mainloop()