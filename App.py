import tkinter as tk
from Data import *


def app():

    root = tk.Tk()
    root.title('Виды спорта')
    root.geometry('800x500')

    start_label = tk.Label(text='Загадайте вид спорта! Загадали?', font='Times 12', pady=15)
    start_button = tk.Button(text='В путь!', width=40, height=3, bg='green', font='Times 15')
    question_label = tk.Label(font='Times 12', pady=15)

    answers_listbox = tk.Listbox(selectbackground='yellow', font='Times 14', selectmode=tk.SINGLE, width=54)
    send_button = tk.Button(text='Ответить', width=15, bg='blue', fg='yellow', font='Times 10', state='disabled')
    result_label = tk.Label(font='Times 16', pady=15)
    result_text_label = tk.Label(width=60, font='Times 16', pady=15)

    start_label.pack()
    start_button.pack()
    question_label.pack()
    answers_listbox.pack()
    send_button.pack()
    result_label.pack()
    result_text_label.pack()

    main_target = 'вид'
    targets_stack = [(main_target, )]
    context = {}
    used_rules = set()
    log_attr = False

    # Ответ, выбранный пользователем
    option = None

    def algo(q_label, ans_listbox, se_button, question=False):
        nonlocal targets_stack, context, used_rules, log_attr, option
        rule_num = None  # индекс текущего правила
        if question:
            cur_target = targets_stack[-1][0]
            context.update({cur_target: attributes[cur_target][option]})
            option = None
            last_target = targets_stack.pop()
            rule_num = last_target[1]
        while not log_attr:
            cur_target = targets_stack[-1][0]
            if not rule_num:
                cur_rules = [_ for _, rule in enumerate(rules) if rule.then_name == cur_target and _ not in used_rules]
                if cur_rules:
                    rule_num = cur_rules[0]
                else:
                    if questions.get(cur_target):
                        prepare_question(cur_target, q_label, ans_listbox, se_button)
                        return
                    else:
                        log_attr = True
                        continue
            while targets_stack:
                cur_rule = rules[rule_num]
                # проверка правила на true/false/?
                res = cur_rule.check_rule(context)
                if res:
                    key, value = res.popitem()

                    if value:  # если получили значение признака
                        context.update({key: value})
                        used_rules.add(rule_num)
                        last_target = targets_stack.pop()
                        rule_num = last_target[1] if targets_stack else None
                    else:  # если значение признака неизвестно
                        targets_stack.append((key, rule_num,))
                        rule_num = None
                        break
                else:
                    used_rules.add(rule_num)
                    rule_num = None
                    break

            if targets_stack:
                continue
            else:
                log_attr = True

        get_result(q_label, ans_listbox)

    def send_click(event, q_label, se_button, ans_listbox):
        nonlocal option
        options = ans_listbox.curselection()
        if options:
            option = options[0]
        else:
            return
        se_button.config(state='disabled')
        algo(q_label, ans_listbox, se_button, True)

    def prepare_question(param, q_label, ans_listbox, send_b):
        q_label.config(text=questions[param])
        ans_listbox.delete(0, tk.END)
        options = attributes[param]
        assert options is not None
        ans_listbox.config(height=len(options))
        for ans in options:
            ans_listbox.insert(tk.END, ans)
        send_b.config(state='normal')

    def get_result(q_label, ans_listbox):
        nonlocal context, result_text_label
        ans_listbox.delete(0, tk.END)
        if context.get(main_target):
            question_label.config(text='')
            result_text_label.config(text='Вердикт:'
                                     ' загаданный вид спорта - ' + context[main_target])
        else:
            question_label.config(text='')
            result_text_label.config(text='Вердикт: Не стоило сворачивать с тропинки в Лихолесьи. ')

    def start_click(event, st_button, q_label, ans_listbox, se_button):
        if st_button['text'] == 'В путь!':
            st_button.config(text='Попробовать еще раз')
            algo(q_label, ans_listbox, se_button)
        else:
            nonlocal option, result_text_label, targets_stack, context, used_rules, log_attr

            st_button.config(text='В путь!')
            answers_listbox.delete(0, tk.END)
            result_text_label.config(text='')
            option = None
            targets_stack = [(main_target,)]
            context = {}
            used_rules = set()
            log_attr = False

    send_button.bind('<Button-1>', lambda e, btn=send_button, lst=answers_listbox,
                                          q_lab=question_label:
                                   send_click(e, q_lab, btn, lst))
    start_button.bind('<Button-1>',
                      lambda e, st_btn=start_button, q_l=question_label,
                             ans_l=answers_listbox, se_btn=send_button:
                      start_click(e, st_btn, q_l, ans_l, se_btn))

    root.mainloop()
