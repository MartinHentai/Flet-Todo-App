import flet as ft

LIGHT_THEME_COLOR = ft.Colors.PINK
def main(page: ft.Page):
    page.title = "Flet testing"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = 'light'
    page.theme = ft.Theme(color_scheme_seed=LIGHT_THEME_COLOR)

    input = ft.TextField( value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def minus_click(e):
        input.value = str(int(input.value) - 1)

    def plus_click(e):
        input.value = str(int(input.value) + 1)

    def animate(e: ft.Event[ft.Button]):
        e.control.rotate = 0.1 if e.data else 0
        page.update()

    def handle_item_click(e: ft.Event[ft.PopupMenuItem]):
            action = e.control.content
            page.show_dialog(ft.SnackBar(content=f"Item '{action}' selected."))

    

    def on_reorder(e: ft.OnReorderEvent):
        e.control.controls.insert(e.new_index, e.control.controls.pop(e.old_index))






    page.title = "Flet Tabs Example"



    tab2 = ft.Column(
             controls=[
                



        ft.ReorderableListView(
            expand=True,
            show_default_drag_handles=False,
            on_reorder=on_reorder,
            controls=[
                ft.ListTile(
                    title=ft.Text(f"Draggable Item {i}", color=ft.Colors.BLACK),
                    leading=ft.ReorderableDragHandle(
                        content=ft.Icon(ft.Icons.DRAG_INDICATOR, color=ft.Colors.RED),
                        mouse_cursor=ft.MouseCursor.GRAB,
                    ),
                    bgcolor=ft.Colors.ERROR
                    if i % 2 == 0
                    else ft.Colors.ON_ERROR_CONTAINER,
                )
                for i in range(10)
            ],
        )
    




             ]
    )




    tab3 = ft.Column(
             controls=[
            ft.Text("This is Tab 3 Content", size=20),
            ft.ElevatedButton("Elevated Button"),
            ft.FilledButton("Filled Button", elevation=5.0, animate_rotation=100, on_hover=animate, ),
            ft.FloatingActionButton(icon=ft.Icons.ADD, content="Nigga",badge=ft.Badge(label="you're a Nigger"), rotate=45 ),
            ft.Dropdown(
        label="Favorite color",
        options=[
            ft.dropdown.Option("Red"),
            ft.dropdown.Option("Green"),
            ft.dropdown.Option("Blue"),
        ],
    ),  

            ft.NavigationRail(
    selected_index=0,
    destinations=[
        ft.NavigationRailDestination(icon=ft.Icons.STAR, label="Star"),
        ft.NavigationRailDestination(icon=ft.Icon(ft.Icons.ADD),label="Add"),
        ft.NavigationRailDestination(icon=ft.Icons.DELETE, label=ft.Text("Delete"))
    ],
    height=200,
    width=100,
),  
            ft.TextField(label="Name"),
            ft.Checkbox(label="I agree to the terms",shape=ft.CircleBorder(),),
            ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.IconButton(ft.Icons.REMOVE, on_click=minus_click ),
                        
                        input,
                        ft.IconButton(ft.Icons.ADD, on_click=plus_click),
                    ],
                ),
            ft.ContextMenu(
                primary_items=[
                    ft.PopupMenuItem(content="Primary 1", on_click=handle_item_click),
                    ft.PopupMenuItem(content="Primary 2", on_click=handle_item_click),
                ],
                primary_trigger=ft.ContextMenuTrigger.DOWN,
                secondary_items=[
                    ft.PopupMenuItem(content="Secondary 1", on_click=handle_item_click),
                    ft.PopupMenuItem(content="Secondary 2", on_click=handle_item_click),
                ],
                secondary_trigger=ft.ContextMenuTrigger.DOWN,
                tertiary_items=[
                    ft.PopupMenuItem(content="Tertiary 1", on_click=handle_item_click),
                    ft.PopupMenuItem(content="Tertiary 2", on_click=handle_item_click),
                ],
                tertiary_trigger=ft.ContextMenuTrigger.DOWN,
                on_select=lambda e: print(f"Selected item: {e.item.content}"),
                on_dismiss=lambda e: print("Menu dismissed"),

                content=ft.Container(
                    bgcolor=ft.Colors.BLUE,
                    padding=10,
                    border_radius=ft.BorderRadius.all(12),
                    content=ft.Text("Left/middle/right click to open a context menu."),
                    ),
            )




            ],)
    tab1_content = ft.Container(
        content=ft.Text("This is Tab 1 Content", size=20),
        alignment=ft.Alignment.CENTER,
    )
    tab2_content = ft.Container(
        content=tab2,
        alignment=ft.Alignment.CENTER,
    )
    tab3_content = ft.Container(
        content= tab3,
        alignment=ft.Alignment.CENTER,
        
    )

    tabs = ft.Tabs(
        length=250,
        selected_index=0,
        animation_duration=300,
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                ft.TabBar(
                    tabs=[
                        ft.Tab(label="Home", icon=ft.Icons.HOME),
                        ft.Tab(label="Search", icon=ft.Icons.SEARCH),
                        ft.Tab(label="Profile", icon=ft.Icons.PERSON),
                    ],
                ),
                ft.TabBarView(
                    expand=True,
                    controls=[
                        tab1_content,
                        tab2_content,
                        tab3_content,
                    ],
                ),
            ],
        ),
    )

    page.add(tabs)


    



    




























ft.run(main, )