import tkinter as tk 
import math 

def penalty_time():
    pass

def access_time():
    pass

def hex_to_binary(hex, mem_size, kb_or_mb):
    if kb_or_mb == 'kb':
        size = math.log(mem_size * 1024, 2)
    else:
        size = math.log(mem_size * 1024 * 1024, 2)
    return str(bin(int(hex[2:], 16))[2:].zfill(int(size)))

def tag_index_offset(binary, block_size, cache_size, cache_kb_or_mb):
    full_length = len(binary)
    if cache_kb_or_mb == 'kb':
        cache_size = cache_size * 1024
    else:
        cache_size = cache_size * 1024 * 1024
    offset_length = math.log(block_size, 2)
    index_length = math.log(cache_size/block_size, 2)
    tag_length = full_length - (offset_length + index_length)
    return [int(tag_length), int(index_length), int(offset_length)]

def main():
    def step_pressed():
        binary = hex_to_binary(entry_list['hex address'].get(), int(entry_list['memory size:'].get()), mem_var)
        tag_index_offset_list = tag_index_offset(binary, int(entry_list['block size:'].get()), int(entry_list['cache size:'].get()), cache_var.get())
        tag = binary[0:tag_index_offset_list[0]]
        index = binary[tag_index_offset_list[0]:tag_index_offset_list[0] + tag_index_offset_list[1]]
        offset = binary[tag_index_offset_list[0] + tag_index_offset_list[1]: tag_index_offset_list[0] + tag_index_offset_list[1] + tag_index_offset_list[2]]
        print(binary,"\n",tag,index,offset)

    def cacl_pressed():
        pass

    window = tk.Tk()
    window.title("Direct mapping simulator")
    window.geometry("600x600")
    window.resizable(False, False)
    btn_calc = tk.Button(master = window, text = "calculate", command = None, highlightbackground='black')
    btn_step = tk.Button(master = window, text = 'step', command = step_pressed, highlightbackground='black')
   
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
