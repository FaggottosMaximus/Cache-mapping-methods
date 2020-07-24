import tkinter as tk 
import math 

def avg_access_time(cache_time, penalty_time, hit_rate):
    return cache_time+(1-hit_rate)*(penalty_time)

def hex_to_binary(hex, mem_size, kb_or_mb):
    if kb_or_mb == 'kb':
        size = math.log(mem_size * 1024, 2)
    else:
        size = math.log(mem_size * 1024 * 1024, 2)
    binary = str(bin(int(hex[2:], 16))[2:].zfill(int(size)))[-int(size):]
    return binary

def tag_index_offset_direct(binary, block_size, cache_size, cache_kb_or_mb):
    full_length = len(binary)
    if cache_kb_or_mb == 'kb':
        cache_size = cache_size * 1024
    else:
        cache_size = cache_size * 1024 * 1024
    offset_length = math.log(block_size, 2)
    index_length = math.log(cache_size/block_size, 2)
    tag_length = full_length - (offset_length + index_length)
    return [int(tag_length), int(index_length), int(offset_length)]

def tag_index_offset_sa(binary, block_size, cache_size, cache_kb_or_mb, number_of_ways):
    full_length = len(binary)
    if cache_kb_or_mb == 'kb':
        cache_size = cache_size * 1024
    else:
        cache_size = cache_size * 1024 * 1024
    offset_length = math.log(block_size, 2)
    index_length = math.log((cache_size/block_size)/number_of_ways, 2)
    tag_length = full_length - (offset_length + index_length)
    return [int(tag_length), int(index_length), int(offset_length)]


def main():
    index_tag_dict = {}
    hits, misses=0, 0
    method = ''
    
    def method_choice():
      nonlocal method 
      method = method_var.get()  

    def step_pressed():
        try:
            binary = hex_to_binary(entry_list['hex address:'].get(), int(entry_list['memory size:'].get()), mem_var)
            tag_index_offset_list = tag_index_offset_direct(binary, int(entry_list['block size:'].get()), int(entry_list['cache size:'].get()), cache_var.get())
            tag = binary[0:tag_index_offset_list[0]]
            index = binary[tag_index_offset_list[0]:tag_index_offset_list[0] + tag_index_offset_list[1]]
            offset = binary[tag_index_offset_list[0] + tag_index_offset_list[1]: tag_index_offset_list[0] + tag_index_offset_list[1] + tag_index_offset_list[2]]
            binary_var = tk.StringVar()
            binary_var.set(tag + " " + index + " " + offset)
            entry_list['binary address:'].configure(textvariable = binary_var)
            nonlocal hits,misses
            fa_index = 0      
            number_of_sets = (entry_list['cache size:']/entry_list['block size:'])/entry_list['number of ways:']     
            sets = [{} for i in range(number_of_sets)]

            if method == 'direct':
                if index in index_tag_dict:
                    if index_tag_dict[index] == tag:
                        hit_or_miss = "Hit"
                        hits += 1
                    else:
                        hit_or_miss = "Miss"
                        index_tag_dict[index] = tag
                        misses += 1
                else:
                    hit_or_miss = "Miss"
                    index_tag_dict[index] = tag
                    misses += 1

            if method == 'fa':
                tag = tag+index
                if tag in index_tag_dict.values():
                    for key in index_tag_dict.keys():
                        if index_tag_dict[key] == tag:
                            index_tag_dict.pop(key)
                            break
                    index_tag_dict[fa_index] = tag
                    hit_or_miss = "Hit"
                    hits += 1
                else:
                    if len(index_tag_dict) == 2 ** index  :
                        index_tag_dict.pop(min(index_tag_dict.keys()))
                        index_tag_dict[fa_index] = tag
                        fa_index += 1
                        misses += 1
                        hit_or_miss = "Miss"
                    else:
                        hit_or_miss = "Miss"
                        misses += 1
                        index_tag_dict[fa_index] = tag
                        fa_index += 1    

            if method == 'sa':
                tag_index_offset_list = tag_index_offset_sa(binary, int(entry_list['block size:'].get()), int(entry_list['cache size:'].get()), cache_var.get(), int(entry_list['number of ways:'].get()))
                tag = binary[0:tag_index_offset_list[0]]
                index = binary[tag_index_offset_list[0]:tag_index_offset_list[0] + tag_index_offset_list[1]]
                offset = binary[tag_index_offset_list[0] + tag_index_offset_list[1]: tag_index_offset_list[0] + tag_index_offset_list[1] + tag_index_offset_list[2]]
                if tag in sets[index].values():
                    for key in sets[index].keys():
                        if tag == sets[index][key]:
                            sets[index].pop(key)
                            break
                    sets[index][fa_index] = tag
                    hit_or_miss = "Hit"
                    hits += 1
                else:
                    if len(sets[index]) == 2 ** index:
                        sets[index].pop(min(sets[index].keys()))
                        sets[index][fa_index] = tag
                        fa_index += 1
                        misses += 1
                        hit_or_miss = "Miss"
                    else:
                        hit_or_miss = "Miss"
                        misses += 1
                        sets[index][fa_index] = tag
                        fa_index += 1 

            hit_or_miss_var = tk.StringVar()
            hit_or_miss_var.set(hit_or_miss)
            entry_list['hit or miss:'].configure(textvariable = hit_or_miss_var)
        except :
            pass #to be done
        
    def cacl_pressed():
        try:    
            access_time = avg_access_time(float(entry_list['cache access time:'].get()),float(entry_list['cache miss penalty time:'].get()),float(hits/(misses+hits)))
            time_var = tk.StringVar()
            time_var.set(access_time)
            entry_list['average access time:'].configure(textvariable = time_var)
        except:
            pass #to be done

    def res_pressed():
        nonlocal index_tag_dict, hits, misses
        index_tag_dict = {}
        hits, misses = 0, 0
        for key in entry_list:
            var = tk.StringVar()
            var.set('')
            entry_list[key].configure(textvariable = var)
        direct_radio.invoke()

    window = tk.Tk()
    window.title("Direct mapping simulator")
    window.geometry("600x750")
    window.resizable(False, False)

    btn_calc = tk.Button(master = window, text = "calculate", command = cacl_pressed, highlightbackground='black', relief='raised')
    btn_step = tk.Button(master = window, text = 'step', command = step_pressed, highlightbackground='black', relief='raised')
    btn_res = tk.Button(master = window, text = "reset", command = res_pressed, highlightbackground='black', relief='raised')
    
    labels_names = ['number of ways:', 'memory size:', 'cache size:', 'block size:', 'hex address:', 'cache miss penalty time:', 'cache access time:', 'hit or miss:', 'average access time:', 'binary address:']
    entry_list = {}
    for i in labels_names:
        label = tk.Label(master=window, text=i, font=(None, 15))
        x = 15
        y = 60*labels_names.index(i)+100
        label.place(x=x,y=y)
        entry_list[i] = tk.Entry(master = window, width = 15)
        entry_list[i].place(x=x+260,y=y)
        if i == 'binary address:' or i == 'hit or miss:' or i == 'average access time:':
            entry_list[i].config(state = 'disabled')
        if i == 'cache miss penalty time:':
            ns_label = tk.Label(master = window, text='ns', font=(None,15))
            ns_label.place(x=430,y=y)
            ns_label = tk.Label(master = window, text='ns', font=(None,15))
            ns_label.place(x=430,y=y+60)

    entry_list['binary address:'].config(width = 35)

    btn_step.place(x=x, y=690)
    btn_calc.place(x=x+70, y=690)
    btn_res.place(x=x+170, y=690)

    mem_var = tk.StringVar()
    mem_var.initialize("kb")
    mg_radio = tk.Radiobutton(master = window, text = "MB", variable = mem_var, value = 'mb')
    kb_radio = tk.Radiobutton(master = window, text = "KB", variable = mem_var, value = 'kb')
    mg_radio.place(x=500,y=100)
    kb_radio.place(x=430,y=100)

    cache_var = tk.StringVar()
    cache_var.initialize('kb')
    mg_radio = tk.Radiobutton(master = window, text = "MB", variable = cache_var, value = 'mb')
    kb_radio = tk.Radiobutton(master = window, text = "KB", variable = cache_var, value = 'kb')
    mg_radio.place(x=500,y=160)
    kb_radio.place(x=430,y=160)

    block_var = tk.StringVar()
    block_var.initialize('B')
    b_radio = tk.Radiobutton(master = window, text = "B", variable = block_var, value = "B")
    b_radio.place(x=430, y=220)
    method_var = tk.StringVar()
    method_var.initialize('direct')
    direct_radio = tk.Radiobutton(master = window, text = 'direct', variable = method_var, value = 'direct', command = method_choice)
    fa_radio = tk.Radiobutton(master = window, text = 'fully associative', variable = method_var, value = 'fa', command = method_choice)
    sa_radio = tk.Radiobutton(master = window, text = 'semi associative', variable = method_var, value = 'sa', command = method_choice)
    direct_radio.place(x=200,y=40)
    fa_radio.place(x=300,y=40)
    sa_radio.place(x=400, y=40)
    label = tk.Label(master = window, text = 'method:', font=(None, 15))
    label.place(x=15,y=40)
    
    direct_radio.invoke()
    entry_list['memory size:'].focus()
    window.mainloop()

main()
