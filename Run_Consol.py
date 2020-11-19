from Data import *

# консоль
main_target = ('вид', )
targets_stack = []
context = {}
used_rules = set()


def start():
    targets_stack.append(main_target)
    log_attr = False
    while not log_attr:

        cur_target = targets_stack[-1][0]
        cur_rules_indexes = [ind for ind, rule in enumerate(rules)
                             if rule.then_name == cur_target and ind not in used_rules]

        if cur_rules_indexes:
            rule_num = cur_rules_indexes[0]

        else:
            # если имеется вопрос, связанный с текущей целью
            if questions.get(cur_target):
                print(questions[cur_target])
                for _, o in enumerate(attributes[cur_target]):
                     print(_ + 1, '. ' + o)
                answer = input()
                context.update({cur_target: attributes[cur_target][int(answer) - 1]})
                # удаление из стека целей
                last_target = targets_stack.pop()

                rule_num = last_target[1]
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
                    last_target = targets_stack.pop()   # удаляем цель
                    rule_num = last_target[1] if targets_stack else None
                else:
                    # если значение признака неизвестно
                    targets_stack.append((key, rule_num))
                    break
            else:
                used_rules.add(rule_num)
                break

        if targets_stack:
            continue
        else:
            log_attr = True

    print('Вердикт: ')
    if context.get(main_target[0]):
        print(context.get(main_target[0]))
    else:
        print("Не стоило сворачивать с тропинки в Лихолесьи... ")


start()