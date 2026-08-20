def money(value):
    return f"₹{float(value):.2f}"


def clear_tree(tree):
    for item in tree.get_children():
        tree.delete(item)
