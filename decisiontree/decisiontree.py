import matplotlib.pyplot as plt
import numpy as np
import warnings
import re


class DecisionTree:
    def __init__(self):
        self.tree = {}
        self.fail = {}
        self.symbols = {"<", ">", "<=", ">=", "==", "!="}
        print(self.symbols)

    def add_rule(self, name, conditions, value=None, next_step=None):
        if value and next_step:
            raise ValueError(f"You can select next step or return output value")
        elif not value and not next_step:
            raise ValueError(f"Give outcome, or next step")
        elif value:
            try:
                value = int(value)
            except ValueError:
                print(f"This is not number: {value} in {name} - {conditions}")
                return False

        if conditions:
            tmp_conditions = conditions
            conditions = conditions.replace(" ", "")
            pattern = "|".join(self.symbols) + r"|\d+"
            conditions = re.findall(pattern, conditions)

            if len(conditions) == 1:
                try:
                    num = int(conditions[0])
                except ValueError as err:
                    print(f"This is not a number: {conditions[0]}")
                    return False

            elif len(conditions) > 1:
                if not self.validate_parse(conditions):
                    print("Not valid")

                good_syms = self.symbols.copy()
                kwargs = {}
                for sym, num in zip(conditions[0::2], conditions[1::2]):
                    "This loop checks if there is not condition conflicts, and produces kwargs for rule dictionary"

                    if len(good_syms) <= 1:
                        print(f"To much rules or incorrect combination: {conditions}")
                        return None

                    if sym == '<' or sym == '<=':
                        if sym == "<=":
                            kw = "sme"
                        else:
                            kw = 'sm'
                        this_types = ["<", "<="]
                        incorect = ["=="]

                    elif sym == '>' or sym == '>=':
                        if sym == ">=":
                            kw = "bige"
                        else:
                            kw = 'big'
                        this_types = [">", ">="]
                        incorect = ["=="]

                    elif sym == '==' or sym == '!=':
                        if sym == "==":
                            kw = "eq"
                        else:
                            kw = 'diff'
                        this_types = ["==", "!="]
                        incorect = ["<", "<=", ">", ">="]
                    else:
                        raise ValueError(f"Symbol unknown: {sym}")

                    #                     print(good_syms)
                    for s in incorect:
                        try:
                            good_syms.remove(s)
                        except KeyError:
                            pass
                    try:
                        good_syms.remove(this_types[0])
                        good_syms.remove(this_types[1])
                    except KeyError as err:
                        if "!=" in good_syms:
                            pass
                        else:
                            print(f"Invalid rule: {name} - {conditions}")
                            print(f"{err}")
                            return False

                    kwargs.update({kw: num})
                ruld = self.get_ruld(**kwargs)
                if value:
                    ruld.update({"val": value})
                else:
                    ruld.update({"next": next_step})
                self._update_tree_rules(name, ruld)

            else:
                warnings.warn(f"Conditions are empty, using boolean condition: ''{tmp_conditions}'")
                self._add_bool(name, value, next_step)
        else:
            self._add_bool(name, value, next_step)

    def add_fail(self, name, value=None, next_step=None):
        if name in self.fail.keys():
            warnings.warn(f"Overwriting fail outcome: {name}")
        self.fail.update({name: {'val': value, 'next': next_step}})

    def _add_bool(self, name, value, next_step):
        ruld = self.get_ruld(bl=True)
        if value:
            ruld.update({"val": value})
        else:
            ruld.update({"next": next_step})

        self._update_tree_rules(name, ruld)

    def get_ruld(self, bl=False, sm=False, sme=False, big=False, bige=False, eq=False, diff=False):
        """
        Smaller
        Smaller equal
        Bigger
        Bigger equal
        Equal
        Different
        """
        ruld = dict().fromkeys(['bl', 'sm', 'sme', 'big', 'bige', 'eq', 'diff', 'val', 'next'], False)
        if bl:
            ruld.update({'bl': True})

        elif sm and sme or big and bige or eq and diff:
            raise ValueError("Can not interpret conditions. Some types are not allowed simultaneously")

        elif sm or sme or big or bige:
            if sm:
                ruld.update({'sm': sm})
            elif sme:
                ruld.update({'sm': sme})

            if sm:
                ruld.update({'big': big})
            elif sme:
                ruld.update({'bige': bige})

            max_val = sm or sme
            min_val = big or bige

            if max_val and min_val and min_val > max_val:
                raise ValueError(f"Conditions are impossible: {min_val} < {max_val}")
        return ruld

    def _update_tree_rules(self, name, new_rule):
        current = self.tree.get(name, [])
        current += [new_rule]
        self.tree.update({name: current})

    def check_tree(self):
        fkeys = set(self.fail.keys())
        for key in self.tree.keys():
            if key not in fkeys:
                warnings.warn(f"{key} has not fail outcome. use 'dt.add_fail()'")
        self.build_hierarchy()

    def build_hierarchy(self):
        print(f"Building hierarchy")
        nodes = {key: set() for key in self.tree.keys()}

        for name, rules in self.tree.items():
            print(name)
            for rul in rules:
                _next = rul.get('next', None)
                if _next:
                    parents = nodes.get(_next)
                    parents.add(name)
                    nodes.update({_next: parents})

            fail_outcome = self.fail.get(name, None)
            if fail_outcome:
                _next = fail_outcome.get("next", None)
                if _next:
                    parents = nodes.get(_next)
                    parents.add(name)
                    print(_next, parents)
                    nodes.update({_next: parents})

        print(nodes)

    def validate_parse(self, rules_to_check):
        size = len(rules_to_check)
        if size == 1:
            "Must be equal to value"
            try:
                int(rules_to_check[0])
                return True
            except ValueError as err:
                return False
        elif size == 0:
            print(f"pared rules are empty: {rules_to_check}")
            return False

        elif not size % 2:
            return True

        else:
            print("Rules are not even, len:", size)


dt = DecisionTree()

dt.add_rule('worktime', "<1", value=5)
dt.add_rule('worktime', ">=1<10", next_step='criminal')
dt.add_rule('worktime', ">=10", next_step='member')

dt.add_rule('criminal', "", value=5)
dt.add_fail('criminal', next_step='member')

dt.add_rule('member', '<5', value=5)
dt.add_rule('member', '>=5', value=15)
dt.add_fail('member', next_step='unhappy')

dt.add_rule('unhappy', '', value=20)
dt.add_fail('unhappy', value=10)

dt.check_tree()

# for key, val in dt.tree.items():
#     print(key, val)
#
# for key, val in dt.fail.items():
#     print(key, val)
