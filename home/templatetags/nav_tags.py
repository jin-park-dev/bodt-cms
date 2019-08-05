from django import template


register = template.Library()


def has_menu_children(page):
    return page.get_children().live().in_menu().exists()


@register.simple_tag(takes_context=True)
def get_site_root(context):
    '''
    Returns a core.Page, not the implementation-specific model used
    so object-comparison to self will return false as objects would differ
    '''
    return context['request'].site.root_page

# Retrieves the top menu items - the immediate children of the parent page
# The has_menu_children method is necessary because the bootstrap menu requires
# a dropdown class to be applied to a parent
# @register.inclusion_tag('bodt/include/navbar.html', takes_context=True)
@register.simple_tag(takes_context=True)
def top_menu(context):
    # site_root = get_site_root(context['request'])
    site_root = context['request'].site.root_page
    # print(site_root)
    # print(site_root.__dict__)
    menuitems = site_root.get_children().filter(
        live=True,
        show_in_menus=True
    )
    # print(menuitems)
    # for menuitem in menuitems:
    #     menuitem.show_dropdown = has_menu_children(menuitem)
    #     print(menuitem)

    return menuitems
    # return {
    #     # 'calling_page': calling_page,
    #     'menuitems': menuitems,
    #     # required by the pageurl tag that we want to use within this template
    #     # 'request': context['request'],
    # }
