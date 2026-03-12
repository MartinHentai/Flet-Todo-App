import flet as ft
import data_json as dj

class SidebarItem(ft.Container):
    def __init__(self, icon, label, count=None, selected=False, on_click=None):
        super().__init__()
        self.label = label
        self.selected = selected
        self.selection_func = on_click
        self.on_click = self.select_on_click
        
        # Dimensions & Styling
        self.height = 40
        self.border_radius = ft.BorderRadius.all(50)
        self.padding = ft.Padding.only(left=10, right=10)
        
        # Selection Styling (The Blue Left Border & Background)

        # Hover events
        self.on_hover = self.highlight_on_hover

        # --- Content Layout ---
        # 1. Leading Icon
        leading_icon = ft.Icon(icon, size=20, color=ft.Colors.WHITE70)
        
        # 2. Text Label
        text_label = ft.Text(label, size=14, expand=True, color=ft.Colors.WHITE)
        
        # 3. Trailing Badge (Optional)
        badge = ft.Container(
            content=ft.Text(str(count), size=12, color=ft.Colors.WHITE70),
            bgcolor=ft.Colors.WHITE10,
            padding=ft.Padding.symmetric(horizontal=6, vertical=2),
            border_radius=10,
            visible=bool(count) # Only show if count exists
        )

        self.content = ft.Row([leading_icon, text_label,badge ], alignment=ft.MainAxisAlignment.START)
        #----------------------STARTUP FUNCTIONS-----------------------
        self.render_selection()

    def render_selection(self):
        if self.selected:
            self.bgcolor = ft.Colors.WHITE10 
            self.border = ft.Border.only(left=ft.BorderSide(3, ft.Colors.BLUE) ) 
        else:
            self.bgcolor =  ft.Colors.TRANSPARENT
            self.border = ft.Border.only(left=ft.BorderSide(3,  ft.Colors.TRANSPARENT)) 
        

    def highlight_on_hover(self, e):
        # Don't change background on hover if it's already selected
        if not self.selected:
            self.bgcolor = ft.Colors.WHITE_10 if e.data  else ft.Colors.TRANSPARENT
            self.update()
    
    def select_on_click(self):
        self.selection_func()
        self.selected = not self.selected
        self.render_selection()
        self.update()
        




class Sidebar(ft.Container):
    def __init__(self, ):
        super().__init__()
        # self.bgcolor = "#FFffff"
        self.selected_tab_name = ""
        self.width = 260
        self.tab_list = ft.ListView( expand=1, spacing= 8, controls=[

            SidebarItem(ft.Icons.LIGHTBULB_OUTLINE, "My Day", on_click=self.diselect_tab),
            SidebarItem(ft.Icons.STAR_BORDER, "Important", on_click=self.diselect_tab),
            SidebarItem(ft.Icons.CALENDAR_MONTH, "Planned", on_click=self.diselect_tab),
            SidebarItem(ft.Icons.PERSON_OUTLINE, "Assigned to me", on_click=self.diselect_tab),
            SidebarItem(ft.Icons.HOME_OUTLINED, "Tasks", on_click=self.diselect_tab),
            
            ft.Divider(color=ft.Colors.WHITE12, height=20,),
            
            SidebarItem(ft.Icons.MENU, "Todo App", count=1300,  on_click=self.diselect_tab),
            SidebarItem(ft.Icons.MENU, "tests", count=3, on_click=self.diselect_tab),
            SidebarItem(ft.Icons.FOLDER_OUTLINED, "Untitled group", on_click=self.diselect_tab),            
        ])











        self.top_area = ft.Container(padding=10,content=ft.Column(
                controls=[
                    ft.Row(controls=[
                                ft.CircleAvatar(foreground_image_src=dj.user_avatar),
                                ft.Text(value=dj.user_name)]),
                    ft.SearchBar(bar_hint_text="Search...", bar_trailing=ft.Icon(ft.Icons.SEARCH), width=(self.width-20), height=40)
                ]))
        self.navigation_area = ft.Container(content=self.tab_list, expand=1)
        self.bottom_area = ft.Container(content= ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,controls=[
            ft.TextButton("New list", style=ft.ButtonStyle(alignment=ft.Alignment.CENTER_LEFT,), icon=ft.Icons.ADD, expand=True, icon_color=ft.Colors.WHITE),
            ft.IconButton(icon=ft.Icons.CREATE_NEW_FOLDER_OUTLINED, icon_size=20, icon_color=ft.Colors.WHITE70),
        
         ]))






        self.content = ft.Column(controls=[
                            self.top_area,
                            self.navigation_area, 
                            self.bottom_area                     
                            ])


    def render_tabs(self):
        pass

















    def select_tab(self,tab_name):
        try:
            tab_to_select = next((tab for tab in self.tab_list.controls if isinstance(tab, SidebarItem) and tab.label == tab_name))
        except StopIteration:
            raise ValueError("Incorrect tab name")
        selected_tab = next((tab for tab in self.tab_list.controls if isinstance(tab, SidebarItem) and tab.selected),None)
        if selected_tab:
            self.diselect_tab(selected_tab)
        
        self.select_tab_name = tab_to_select.label
        tab_to_select.selected = True
        tab_to_select.render_selection()
        

    def diselect_tab(self,tab=None):
        if tab:
            selected_tab = tab
            self.selected_tab_name = ""
        else:
            selected_tab = next((tab for tab in self.tab_list.controls if isinstance(tab, SidebarItem) and tab.selected),None)
            self.selected_tab_name = selected_tab.label
        if selected_tab:
            selected_tab.selected = False
            selected_tab.render_selection()
        self.update()

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.bgcolor = ft.Colors.BLACK87


    sidebar = Sidebar()
    sidebar.select_tab("My Day")
    # Add to page alongside a dummy main content area
    page.add(
        ft.Row(
            expand=True,
            spacing=0,
            controls=[
                sidebar,
                # Main app area
                ft.Container(expand=True, bgcolor=ft.Colors.BLACK) 
            ]
        )
    )

ft.run(main)