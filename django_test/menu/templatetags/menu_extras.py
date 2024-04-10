from django import template
from django.shortcuts import get_list_or_404


from menu.models import MenuItem, Menu
from menu.utils.menu_tree import MenuTree


register = template.Library()


@register.inclusion_tag('menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context.get("request")
    menu_items = get_list_or_404(MenuItem.objects.order_by("title"), menu=menu_name)
    menu_tree = MenuTree(request, menu_items, menu_name)
    exposed_items = menu_tree.get_exposed_tree()
    return {"items": exposed_items, "menu_name": menu_name}
