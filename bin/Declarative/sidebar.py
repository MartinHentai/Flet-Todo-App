import traceback
import flet as ft
from dataclasses import dataclass, field
from typing import Callable, cast
from itertools import zip_longest

# logging.basicConfig(level=logging.INFO)






import sys
import os

# Adds the absolute path of the folder to the search path
sys.path.append(os.path.relpath('bin'))


import data_json as dj

import re



#------------LISTS THAT SHALL BE PASSED FROM OTHER FILE--------------

groups_list = [ "test_group_1", "test_group_2"]

tabs_list = ["My Day","Important", "Planned", "Assigned to me", "Tasks", #  _main
             "Todo App", "tests", "tests2"]     #_general

ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]





#----------------PROTOYPE FOR MAIN LOGIC.PY---------------

def get_unique_name(name, existing_names):
    if name not in existing_names:
        return name

    # Group 1: The base name
    # Group 2: The number inside the parentheses
    match = re.search(r"^(.*)\((\d+)\)$", name)  #  Regex pattern: look for "(some_number)" at the very end of the string

    if match:
        base_name = match.group(1).strip()
        counter = int(match.group(2)) + 1
    else:
        base_name = name
        counter = 1

    # Try to find the next available slot
    new_name = f"{base_name}({counter})"
    while new_name in existing_names:
        counter += 1
        new_name = f"{base_name}({counter})"

    return new_name







TabIndex = ft.IdCounter(start=0)

@ft.observable
@dataclass
class SideBar:
    current_tab_index : int = 0
    groups : list[str] = field(default_factory=list)
    tabs : list[str] = field(default_factory=list)
    width : int = 260
    

@ft.observable
@dataclass
class SideBarItem:
    id : int = field(default_factory=TabIndex)
    height : int = 40
    label : str = "Untitled list"      
    icon : ft.Icon = ft.Icons.MENU
    tasks_count: int = 0 
    group : SideBarGroup = None 
    is_selected : bool = False

@ft.observable
@dataclass
class SideBarGroup:
    pass
    # label : str = "Untitled group" 
    # icon : ft.Icon = ft.Icons.FOLDER_OUTLINED
    # lists_in_group : list[SideBarItem]

@ft.component
def SideBarView(on_tab_change: Callable[[str], None]):

    try:

        sidebar, _ = ft.use_state(lambda: SideBar())
        sidebar.tabs = ["My Day","Important", "Planned", "Assigned to me", "Tasks", #  _main
             "Todo App", "tests", "tests2", "My Day","Important", "Planned", "Assigned to me", "Tasks", #  _main
             "Todo App", "tests", "tests2"]


        width, _ = ft.use_state(sidebar.width)
        main_tabs = ["My Day","Important", "Planned", "Assigned to me", "Tasks"]
        user_lists, _ = ft.use_state(sidebar.tabs)
        main_tabs_icons = [ft.Icons.LIGHTBULB_OUTLINE,ft.Icons.STAR_BORDER,ft.Icons.CALENDAR_MONTH,ft.Icons.PERSON_OUTLINE,ft.Icons.HOME_OUTLINED,]
        current_tab, set_tab = ft.use_state(sidebar.current_tab_index)
        ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
        



        def add_new_list():
            pass

        def add_new_group():
            pass


            



        def select_tab(new_id):
            set_tab(new_id)



        def send_tab_name():
            if current_tab+1 > len(main_tabs):
                name_list = user_lists
                start_index = (current_tab)-len(main_tabs)
            else:
                name_list = main_tabs
                start_index = current_tab

            tab_name = name_list[start_index]
            on_tab_change(tab_name)            

        ft.use_effect(send_tab_name, [current_tab])



        def build_sidebar_items(labels, current_tab, tab_set_func, icons=None, start_id=0):
            DEFAULT_ICON = SideBarItem.icon
            
            # If icons is None (not passed), make it an empty list so zip_longest can use it
            icons_list = icons if icons is not None else []
            
            views = []
            for i, (label, icon) in enumerate(zip_longest(labels, icons_list, fillvalue=DEFAULT_ICON)):
                
                global_id = i + start_id

                item = SideBarItem(
                    label=label, 
                    icon=icon,
                    id=ids[global_id], 
                )
                item.is_selected = (item.id == current_tab)
                views.append(SideBarItemView(item,tab_set_func))
            
                
            return views



        return ft.Container(
            width=width,
            # expand=True,

            # bgcolor="#ff00ff",
            content=ft.Column(
                controls=[
                    ft.Container(         #Top area
                        padding=10,
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                    ft.CircleAvatar(foreground_image_src=dj.user_avatar),
                                    ft.Text(value=dj.user_name)
                                    ]
                                ),
                                ft.SearchBar(
                                    bar_hint_text="Search...", 
                                    bar_trailing=ft.Icon(ft.Icons.SEARCH), 
                                    width=(width-20), 
                                    height=40
                                )
                            ]
                        )
                    ),
                                    ft.Container(       #Tabs area
                                        content=ft.ListView( 
                                            expand=1, 
                                            spacing= 8, 
                                            controls=[
                                                
                                                ft.Container(
                                                    content=ft.Column(
                                                        controls=[
                                                               
                                                                *build_sidebar_items(
                                                                    labels=main_tabs,
                                                                    current_tab=current_tab, 
                                                                    icons=main_tabs_icons,
                                                                    tab_set_func=select_tab
                                                                ),
                                                             
                                                            ft.Divider(color=ft.Colors.WHITE12, height=20,),
                                                        ]
                                                    )
                                                ),
                                                   
                                                    *build_sidebar_items(
                                                        labels=sidebar.tabs,
                                                        current_tab=current_tab,
                                                        tab_set_func=select_tab,
                                                        start_id=len(main_tabs)
                                                    ),



                                            ]
                                        ),
                                        expand=1
                                    ), 
                                    ft.Container(       #Bottom area
                                        content=ft.Row(
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                                ft.TextButton(
                                                    content="New list",
                                                    style=ft.ButtonStyle(alignment=ft.Alignment.CENTER_LEFT,), 
                                                    icon=ft.Icons.ADD,
                                                    expand=True, 
                                                    icon_color=ft.Colors.WHITE
                                                ),
                                                ft.IconButton(
                                                    icon=ft.Icons.CREATE_NEW_FOLDER_OUTLINED, 
                                                    icon_size=20, 
                                                    icon_color=ft.Colors.WHITE70
                                                ),
                                            ]
                                        )
                                    )                     
                ]
            )
        )

    except Exception:
        print(traceback.format_exc()) # This will show the full error in your terminal
        return ft.Text("Component Failed to Load", color="red")


@ft.component
def SideBarItemView(tab : SideBarItem, tab_select):
    
    label, _ = ft.use_state(tab.label)
    count, _ = ft.use_state(tab.tasks_count)
    # status, set_status = ft.use_state(tab.is_selected)
    is_hovered, handle_hover = ft.use_state(False)


    def render_hover(e):
        handle_hover(e.data == True)
        

    def seto_status():
        print(tab.id)
        tab_select(tab.id)
        # set_status(True)
    

    bg_color = ft.Colors.WHITE10 if (tab.is_selected or is_hovered) else ft.Colors.TRANSPARENT
    border_color = ft.Colors.BLUE if tab.is_selected else ft.Colors.TRANSPARENT

    return ft.Container(
        height=tab.height,
        border_radius = ft.BorderRadius.all(50),
        padding = ft.Padding.only(left=10, right=10),
        on_hover= render_hover,
        on_click=seto_status,
        bgcolor=bg_color,
        border=ft.Border.only(
            left=ft.BorderSide(
                width=3,  
                color=border_color,
            )
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.START,
            
            controls=[
                ft.Icon(tab.icon, size=20, color=ft.Colors.WHITE70), 
                ft.Text(label, size=14, expand=True, color=ft.Colors.WHITE),
                ft.Container(
                    content=ft.Text(str(count), size=12, color=ft.Colors.WHITE70),
                    padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                    border_radius=10,
                    visible=bool(count),

                )
                                
                               
            ],
        )
    )















        
def test_func(mes):
    print(mes)











@ft.component
def AppLayout():
    return ft.Row(
            expand=True,
            spacing=0,
            controls=[
                # Main app area
                SideBarView(on_tab_change=test_func),
                ft.Container(expand=True, bgcolor=ft.Colors.BLUE) 
            ]
        )


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.bgcolor = ft.Colors.BLACK_87

    def handle_exception(e):
        print(f"FLET ERROR: {e.data}")
        print(traceback.format_exc())

    page.on_error = handle_exception


    
    # Add to page alongside a dummy main content area
    
    page.render(AppLayout)
    # page.render(SideBarView)

ft.run(main)