import tkinter as tk 

def penalty_time():
    pass

def access_time():
    pass

def main():
    window = tk.Tk()
    window.title("Direct mapping simulator")
    window.geometry("600x600")
    window.resizable(False, False)
    
    btn_calc = tk.Button(master = window, text = "calculate", command = None, highlightbackground='black')
    btn_step = tk.Button(master = window, text = 'step', command = None, highlightbackground='black')
   
    labels_names = ['memory size:', 'cache size:', 'block size:', 'hex address', 'cache access time:', 'cache miss penalty time:', 'binary address:']
    entry_list = {}
    for i in labels_names:
        label = tk.Label(master=window, text=i, font=(None, 15))
        x = 15
        y = 60*labels_names.index(i)+30
        label.place(x=x,y=y)
        entry_list[i] = tk.Entry(master = window, width = 15)
        entry_list[i].place(x=x+260,y=y)
        if i == 'cache access time:' or i == 'cache miss penalty time:' or i == 'binary address:':
            entry_list[i].config(state = 'disabled')
    entry_list['binary address:'].config(width = 35)

    btn_step.place(x=x, y=480)
    btn_calc.place(x=x, y=530)

    mem_var = tk.StringVar()
    mem_var.initialize("kb")
    mg_radio = tk.Radiobutton(master = window, text = "MB", variable = mem_var, value = 'mb')
    kb_radio = tk.Radiobutton(master = window, text = "KB", variable = mem_var, value = 'kb')
    mg_radio.place(x=500,y=30)
    kb_radio.place(x=430,y=30)

    cache_var = tk.StringVar()
    cache_var.initialize('kb')
    mg_radio = tk.Radiobutton(master = window, text = "MB", variable = cache_var, value = 'mb')
    kb_radio = tk.Radiobutton(master = window, text = "KB", variable = cache_var, value = 'kb')
    mg_radio.place(x=500,y=90)
    kb_radio.place(x=430,y=90)

    block_var = tk.StringVar()
    block_var.initialize('B')
    b_radio = tk.Radiobutton(master = window, text = "B", variable = block_var, value = "B")
    b_radio.place(x=430, y=150)
    
    window.mainloop()

main()
