"""
Так как я ограничен одним запросом к БД для каждой таблицы,
я не могу использовать префетч чтобы взять всех чайлдов для
каждого итема, прикручивю дерево, которое строится по паренту,
и с помощью поиска в глубину нахожу раскрытые ноды
"""

from collections import defaultdict
from itertools import dropwhile


class ExposedTreeNode:
    def __init__(self, model):
        self.model = model
        self.children = []


class MenuTree:
    def __init__(self, request, items, menu_name):
        self._name = menu_name
        self._selected_menu = request.GET.get("selected_menu", "")
        self._selected = int(request.GET.get("selected_row", "-1"))

        self._items = items
        self._roots = [i for i in items if i.parent is None]
        self._full_tree = self.build_tree(self._items)
        self._exposed_nodes = self.init_exposed()

    def __str__(self):
        return f"{self._full_tree}"

    def build_tree(self, items):
        tree = defaultdict(list)
        for item in items:
            if item.parent is None and item not in tree:
                tree[item] = []
            else:
                tree[item.parent].append(item)
        return tree

    def get_exposed_tree(self):
        exposed_dict = self.build_tree(self._exposed_nodes)
        exposed_tree = []
        for root in self._roots:
            curr_tree = self.build_tree_from_dict(exposed_dict, root)
            exposed_tree.append(curr_tree)
        return exposed_tree

    def build_tree_from_dict(self, node_dict, root):
        root_node = ExposedTreeNode(root)
        if root in node_dict:
            for child in node_dict[root]:
                child_node = self.build_tree_from_dict(node_dict, child)
                root_node.children.append(child_node)
        return root_node

    def init_exposed(self):
        if self._selected == -1 or self._selected_menu != self._name:
            return self._roots
        res = self.dfs()
        res.extend([
            i for i in dropwhile(
                lambda x: x.id != self._selected, self._items
            )
            if i.parent is None
        ][1:])
        return res

    def dfs(self):
        res = []
        to_visit = self._roots[::-1]
        curr_id = -1
        while to_visit and self._selected != curr_id:
            curr_node = to_visit.pop()
            curr_id = curr_node.id
            if curr_node.parent is None:
                res.append(curr_node)
            res.extend(self._full_tree[curr_node])
            to_visit.extend(reversed(self._full_tree[curr_node]))
        return res





