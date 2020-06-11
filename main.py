import tkinter as tk 

def penalty_time():
    pass

def access_time():
    pass

def main():
    window = tk.Tk()
    window.title("Direct mapping simulator")
    window.geometry("500x500")
    window.resizable(False, False)
    
    btn_calc = tk.Button(master = window, text = "calculate", command = None, highlightbackground='black')
    btn_step = tk.Button(master = window, text = 'step', command = None, highlightbackground='black')
   
    labels_list = ['memory size', 'cache size', 'block size', 'cache access time', 'cache miss penalty time']
    for i in labels_list:
        label = tk.Label(master=window, text=i,bg="lightblue")
        label.place(x=15,y=60*labels_list.index(i)+30)
        label.configure()
    window.mainloop()

main()
