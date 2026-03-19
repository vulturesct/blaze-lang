import sys
import re
import tkinter as tk
import math
import random

variables = {}
functions = {}
WIN = None
CAN = None
keys = set()

def evaluate(expr, local_vars=None):
    expr = str(expr).strip()
    if expr.startswith('"') and expr.endswith('"'):
        return expr[1:-1]
    if expr == 'true': return True
    if expr == 'false': return False

    # list literal
    if expr.startswith('[') and expr.endswith(']'):
        inner = expr[1:-1].strip()
        if not inner: return []
        return [evaluate(x.strip(), local_vars) for x in inner.split(',')]

    # variable lookup first
    if local_vars and expr in local_vars:
        return local_vars[expr]
    if expr in variables:
        return variables[expr]

    # list index  mylist[0]
    m = re.match(r'^(\w+)\[(\d+)\]$', expr)
    if m:
        lst = evaluate(m.group(1), local_vars)
        if isinstance(lst, list):
            return lst[int(m.group(2))]

    # built-in functions
    # math
    if expr.startswith('sqrt(') and expr.endswith(')'):
        return math.sqrt(float(evaluate(expr[5:-1], local_vars)))
    if expr.startswith('pow(') and expr.endswith(')'):
        a,b = expr[4:-1].split(',',1)
        return math.pow(float(evaluate(a.strip(),local_vars)), float(evaluate(b.strip(),local_vars)))
    if expr.startswith('abs(') and expr.endswith(')'):
        return abs(float(evaluate(expr[4:-1], local_vars)))
    if expr.startswith('round(') and expr.endswith(')'):
        return round(float(evaluate(expr[6:-1], local_vars)))
    if expr.startswith('floor(') and expr.endswith(')'):
        return math.floor(float(evaluate(expr[6:-1], local_vars)))
    if expr.startswith('ceil(') and expr.endswith(')'):
        return math.ceil(float(evaluate(expr[5:-1], local_vars)))
    if expr.startswith('random(') and expr.endswith(')'):
        a,b = expr[7:-1].split(',',1)
        return random.randint(int(float(evaluate(a.strip(),local_vars))), int(float(evaluate(b.strip(),local_vars))))

    # string functions
    if expr.startswith('length(') and expr.endswith(')'):
        val = evaluate(expr[7:-1], local_vars)
        return len(str(val)) if not isinstance(val, list) else len(val)
    if expr.startswith('upper(') and expr.endswith(')'):
        return str(evaluate(expr[6:-1], local_vars)).upper()
    if expr.startswith('lower(') and expr.endswith(')'):
        return str(evaluate(expr[6:-1], local_vars)).lower()
    if expr.startswith('str(') and expr.endswith(')'):
        return str(evaluate(expr[4:-1], local_vars))
    if expr.startswith('num(') and expr.endswith(')'):
        v = evaluate(expr[4:-1], local_vars)
        try: return int(v)
        except: return float(v)
    if expr.startswith('get(') and expr.endswith(')'):
        a,b = expr[4:-1].split(',',1)
        lst = evaluate(a.strip(), local_vars)
        idx = int(float(evaluate(b.strip(), local_vars)))
        if isinstance(lst, list): return lst[idx]
    if expr.startswith('size(') and expr.endswith(')'):
        lst = evaluate(expr[5:-1], local_vars)
        if isinstance(lst, list): return len(lst)
        return len(str(lst))

    # math expressions
    for op in ['+', '-', '*', '/']:
        if op in expr:
            parts = expr.split(op, 1)
            try:
                left = evaluate(parts[0].strip(), local_vars)
                right = evaluate(parts[1].strip(), local_vars)
                # string concat
                if op == '+' and (isinstance(left, str) or isinstance(right, str)):
                    return str(left) + str(right)
                left, right = float(left), float(right)
                if op == '+': r = left + right
                elif op == '-': r = left - right
                elif op == '*': r = left * right
                elif op == '/': r = left / right
                return int(r) if r == int(r) else r
            except: pass

    try: return int(expr)
    except: pass
    try: return float(expr)
    except: pass
    return expr

def evaluate_condition(cond, local_vars=None):
    cond = cond.strip()
    if cond.startswith('key(') and cond.endswith(')'):
        return cond[4:-1].strip().strip('"') in keys
    if cond.startswith('near(') and cond.endswith(')'):
        a = [evaluate(x.strip(), local_vars) for x in cond[5:-1].split(',')]
        dx = float(a[0]) - float(a[2])
        dy = float(a[1]) - float(a[3])
        return (dx*dx + dy*dy) ** 0.5 < float(a[4])
    if cond.startswith('has(') and cond.endswith(')'):
        a,b = cond[4:-1].split(',',1)
        lst = evaluate(a.strip(), local_vars)
        val = evaluate(b.strip(), local_vars)
        return val in lst if isinstance(lst, list) else False
    for op in ['>=','<=','!=','==','>','<']:
        if op in cond:
            l,r = cond.split(op,1)
            lv = evaluate(l.strip(), local_vars)
            rv = evaluate(r.strip(), local_vars)
            try: lv,rv = float(lv),float(rv)
            except: pass
            if op == '==': return lv == rv
            if op == '!=': return lv != rv
            if op == '>':  return lv > rv
            if op == '<':  return lv < rv
            if op == '>=': return lv >= rv
            if op == '<=': return lv <= rv
    return bool(evaluate(cond, local_vars))

def collect_block(lines, start):
    block = []
    depth = 1
    i = start
    while i < len(lines):
        l = lines[i].strip()
        i += 1
        if l.endswith('{'):
            depth += 1
            block.append(l)
        elif l == '}':
            depth -= 1
            if depth == 0: return block, i
            else: block.append(l)
        else:
            block.append(l)
    return block, i

def run_block(lines, local_vars=None):
    global WIN, CAN
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line or line.startswith('--'):
            continue

        # include
        if line.startswith('include '):
            module = line[8:].strip()
            if module == 'draw':
                WIN = tk.Tk()
                WIN.title("Blaze")
                CAN = tk.Canvas(WIN, width=800, height=600, bg='black')
                CAN.pack()
                WIN.bind('<KeyPress>',   lambda e: keys.add(e.keysym.lower()))
                WIN.bind('<KeyRelease>', lambda e: keys.discard(e.keysym.lower()))
                WIN.focus_force()
            continue

        # let
        if line.startswith('let ') and '=' in line:
            name, val = line[4:].split('=', 1)
            variables[name.strip()] = evaluate(val.strip(), local_vars)
            continue

        # set
        if line.startswith('set ') and '=' in line:
            name, val = line[4:].split('=', 1)
            variables[name.strip()] = evaluate(val.strip(), local_vars)
            continue

        # add(list, value)
        if line.startswith('add(') and line.endswith(')'):
            a,b = line[4:-1].split(',',1)
            lst_name = a.strip()
            val = evaluate(b.strip(), local_vars)
            if lst_name in variables and isinstance(variables[lst_name], list):
                variables[lst_name].append(val)
            continue

        # remove(list, index)
        if line.startswith('remove(') and line.endswith(')'):
            a,b = line[7:-1].split(',',1)
            lst_name = a.strip()
            idx = int(float(evaluate(b.strip(), local_vars)))
            if lst_name in variables and isinstance(variables[lst_name], list):
                variables[lst_name].pop(idx)
            continue

        # print
        if line.startswith('print(') and line.endswith(')'):
            print(evaluate(line[6:-1], local_vars))
            continue

        # draw commands
        if line == 'draw.clear()':
            if CAN: CAN.delete('g')
            continue
        if line.startswith('draw.bgcolor(') and line.endswith(')'):
            if CAN: CAN.config(bg=line[13:-1].strip().strip('"'))
            continue
        if line.startswith('draw.rect(') and line.endswith(')'):
            if CAN:
                a = [x.strip().strip('"') for x in line[10:-1].split(',')]
                if len(a) == 5:
                    x,y,w,h = int(float(evaluate(a[0],local_vars))), int(float(evaluate(a[1],local_vars))), int(float(evaluate(a[2],local_vars))), int(float(evaluate(a[3],local_vars)))
                    CAN.create_rectangle(x,y,x+w,y+h, fill=a[4], outline=a[4], tags='g')
            continue
        if line.startswith('draw.circle(') and line.endswith(')'):
            if CAN:
                a = [x.strip().strip('"') for x in line[12:-1].split(',')]
                if len(a) == 4:
                    x,y,s = int(float(evaluate(a[0],local_vars))), int(float(evaluate(a[1],local_vars))), int(float(evaluate(a[2],local_vars)))
                    CAN.create_oval(x-s,y-s,x+s,y+s, fill=a[3], outline=a[3], tags='g')
            continue
        if line.startswith('draw.text(') and line.endswith(')'):
            if CAN:
                a = [x.strip().strip('"') for x in line[10:-1].split(',')]
                if len(a) == 4:
                    x,y = int(float(evaluate(a[0],local_vars))), int(float(evaluate(a[1],local_vars)))
                    CAN.create_text(x,y, text=str(evaluate(a[2],local_vars)), fill=a[3], font=('Arial',16), tags='g')
            continue
        if line == 'draw.show()':
            if WIN: WIN.mainloop()
            continue

        # game.loop
        if line == 'game.loop {':
            block, i = collect_block(lines, i)
            def tick(b=block):
                run_block(b, None)
                WIN.after(16, lambda: tick(b))
            WIN.after(16, lambda: tick(block))
            WIN.mainloop()
            continue

        # if
        if line.startswith('if ') and line.endswith('{'):
            condition = line[3:-1].strip()
            block, i = collect_block(lines, i)
            else_block = []
            if i < len(lines) and lines[i].strip() == '} else {':
                i += 1
                else_block, i = collect_block(lines, i)
            if evaluate_condition(condition, local_vars):
                run_block(block, local_vars)
            elif else_block:
                run_block(else_block, local_vars)
            continue

        # loop N times
        if line.startswith('loop ') and 'times' in line:
            count = int(float(evaluate(line.split()[1], local_vars)))
            block, i = collect_block(lines, i)
            for _ in range(count):
                run_block(block, local_vars)
            continue

        # loop while
        if line.startswith('loop while ') and line.endswith('{'):
            condition = line[11:-1].strip()
            block, i = collect_block(lines, i)
            while evaluate_condition(condition, local_vars):
                run_block(block, local_vars)
            continue

        # loop each item in list
        if line.startswith('loop each ') and ' in ' in line and line.endswith('{'):
            parts = line[10:-1].strip().split(' in ')
            var_name = parts[0].strip()
            list_name = parts[1].strip()
            block, i = collect_block(lines, i)
            lst = evaluate(list_name, local_vars)
            if isinstance(lst, list):
                for item in lst:
                    variables[var_name] = item
                    run_block(block, local_vars)
            continue

        # func
        if line.startswith('func ') and line.endswith('{'):
            header = line[5:-1].strip()
            fname = header[:header.index('(')].strip()
            args_str = header[header.index('(')+1:header.index(')')].strip()
            arg_names = [a.strip() for a in args_str.split(',')] if args_str else []
            block, i = collect_block(lines, i)
            functions[fname] = (arg_names, block)
            continue

        # function call
        m = re.match(r'^(\w+)\((.*)\)$', line)
        if m:
            fname = m.group(1)
            arg_vals = [evaluate(a.strip(), local_vars) for a in m.group(2).split(',')] if m.group(2).strip() else []
            if fname in functions:
                an, bl = functions[fname]
                run_block(bl, dict(zip(an, arg_vals)))
            continue

def run_file(filepath):
    try:
        with open(filepath,'r') as f: code = f.read()
    except FileNotFoundError:
        print(f"[Blaze Error] File not found: {filepath}")
        return
    print(f"[Blaze] Running {filepath}...\n")
    run_block(code.splitlines())
    print("\n[Blaze] Done.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: py blaze.py yourfile.bz")
    else:
        run_file(sys.argv[1])
