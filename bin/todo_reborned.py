# OWN LIBRARIES
import todo_sidebar

from dataclasses import field
from typing import Callable

import flet as ft


# FIX THE NEW LINE ON SUBMIT




class TodoApp(ft.Row):


    def __init__(self, ):
        super().__init__()
        self.expand = True
        self.dummy = ft.Button(content="",width=0, height=0, opacity=0, style=ft.ButtonStyle(padding=0))
        self.left_width = 260
        self.right_width = 340
        self.edit_panel_is_mapped = False
        self.curr_task = None
        self.spacing = 0
        self.blur = ft.Blur(10, 10, ft.BlurTileMode.MIRROR)

        
        #-------------TABS-------------
        self.user_name = "Hentai"
        self.tab_name = ft.Text(value="", expand=True, size=30,weight=ft.FontWeight.W_600 )
        self.tabs_area = ft.NavigationRail(
    selected_index=0,label_type=ft.NavigationRailLabelType.ALL,min_extended_width=self.left_width,
            extended=True,
            leading=ft.Column(
                controls=[
                    ft.Row(controls=[
                                ft.CircleAvatar(foreground_image_src="https://hypixel.net/attachments/1594987971226-png.1852248/"),
                                ft.Text(value=self.user_name)]),
                    ft.SearchBar(bar_hint_text="Search...", width=(self.left_width-20), height=40)
                ]),
            trailing=ft.Row(controls=[
                ft.TextButton(icon=ft.Icons.ADD,content="New list", tooltip="Add a new list"),
                ft.IconButton(icon=ft.Icons.ABC, tooltip="Create a new group")

                ]),
            destinations=[                 
                ft.NavigationRailDestination(icon=ft.Icons.WB_SUNNY_OUTLINED, label="My Day"),
                ft.NavigationRailDestination(icon=ft.Icons.STAR_OUTLINED, label="Important"),
                ft.NavigationRailDestination(icon=ft.Icons.CALENDAR_TODAY, label="Planned"),
                ft.NavigationRailDestination(icon=ft.Icons.LIST, label="Tasks"),
                ft.NavigationRailDestination(icon=ft.Icons.PERSON_OUTLINE, label="Assigned to me"),
                ft.NavigationRailDestination(icon=ft.Icons.CHECK_CIRCLE_OUTLINE, label="Completed"),],
                on_change=self.tab_name_set, 
    ) 
        
       #-------------TASKS AREA-------------
        tasks = ft.ListView(expand=True,   spacing=6, padding=ft.Padding.all(20), 
                controls=[Task(task_name=f"Task {i+1}",edit_func=self.render_edit_panel, on_task_delete=self.delete_tsk) for i in range(130)],
                )
        
        self.new_task_entry = ft.TextField(label="Type task name", hint_text="dfghj", expand=True, visible=False)
        self.tasks_area =ft.Container( expand=True,  content=ft.Column(controls=[
                ft.Container( padding=ft.Padding(left=23, right=23),content=ft.Row(controls=[ self.tab_name,
                    ft.IconButton(icon=ft.Icons.PERSON_ADD, tooltip="Share tasks list"),
                    ft.IconButton(icon=ft.Icons.PICTURE_IN_PICTURE, tooltip="Keep on top"),
                    ft.IconButton(icon=ft.Icons.MORE_HORIZ, tooltip="List options"),
                ], alignment=ft.Alignment.CENTER_RIGHT, )),
                tasks,
                ft.Container(padding=5, content=ft.Stack(controls=[
                    ft.TextButton(icon=ft.Icons.ADD, style=ft.TextStyle(color="#ffffff"),icon_color="#ffffff",content="Add a new task", expand=True, height=50, on_click=self.render_new_task_entry),
                    self.new_task_entry
                ]))
            ]))
        #-------------EDIT PANEL-------------
        self.edit_panel_cb = ft.Checkbox(shape=ft.CircleBorder(), on_change=self.on_cb_change, align=ft.Alignment.TOP_CENTER,)

        self.edit_panel_text_entry = ft.TextField(value="task_name",  shift_enter=True, on_submit=self.edit_tsk, max_length=250,
                                                   multiline=True, min_lines=1, counter='' )
        
        self.edit_panel = ft.Container( theme=ft.Theme(color_scheme_seed=ft.Colors.WHITE),visible=self.edit_panel_is_mapped, width=self.right_width,
            content=ft.Column(controls=[
                ft.Container(alignment=ft.Alignment.CENTER_RIGHT,content=ft.IconButton(icon=ft.Icons.CLOSE_OUTLINED, on_click=self.close_edit_panel)),
                ft.Container(alignment=ft.Alignment.TOP_CENTER,content=ft.Row(controls=[self.edit_panel_cb,self.edit_panel_text_entry], spacing=(-1)),),
                ft.Container(content=ft.TextButton(icon=ft.Icons.SUNNY, content="Add to my day" ,on_click=lambda e:self.set_edit_text_style(not self.edit_panel_cb.value))),
                ft.Container(content=ft.Column(spacing=5, controls=[
                    ft.TextButton(icon=ft.Icons.ALARM, content="Remind me" ),
                    ft.TextButton(icon=ft.Icons.CALENDAR_MONTH_OUTLINED, content="Add Due date" ),
                    ft.TextButton(icon=ft.Icons.EVENT_REPEAT_OUTLINED, content="Repeat" )

                ])),
                ft.Container(content=ft.TextButton(icon=ft.Icons.PERSON_ADD, content="Asign to" )),
                ft.Container(content=ft.TextButton(icon=ft.Icons.ATTACH_FILE, content="Add file" )),
                ft.Container(content=ft.TextButton(icon=ft.Icons.NOTE, content="Add a note" )),
                self.dummy

                ], spacing= 25
            
            
            
            
            ), blur=self.blur, bgcolor=ft.Colors.with_opacity(0.45,"#6b6b6b"),
         )
        self.controls = [ 
                         self.tabs_area,
                        
                            
                         self.tasks_area,
                         self.edit_panel
                         ]
        #--------------STARTUP FUNCTIONS-----------------
        self.tab_name_set()

    def tab_name_set(self):
        dest = self.tabs_area.destinations[self.tabs_area.selected_index]
        label = dest.label
        self.tab_name.value = label
        

    async def render_new_task_entry(self, e):
        e.control.visible = False
        self.new_task_entry.visible = True
        await self.set_focus()

    async def set_focus(self,):
        await self.new_task_entry.focus()


    def close_edit_panel(self):
        self.edit_panel.visible = False

    def render_edit_panel(self, task: Task ):
        self.edit_panel.visible = True
        self.edit_panel_text_entry.value = task.task_name
        self.set_edit_text_style(task.cb.value) 
        self.edit_panel_cb.value = task.cb.value
        self.curr_task = task
        self.curr_task.is_editing = True
        # self.curr_task.update()
        self.edit_panel.update()


    def on_cb_change(self):
        self.curr_task.cb.value = self.edit_panel_cb.value
        self.curr_task.on_cb_click()
        self.edit_panel_text_entry.value = self.curr_task.task_name
        self.set_edit_text_style(state=self.edit_panel_cb.value)
        self.curr_task.update()
    
    def set_edit_text_style(self, state: bool):
        panel = self.edit_panel_text_entry
        if  state:
            panel.text_style = ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH)
        else:
            panel.text_style = ft.TextStyle(decoration=ft.TextDecoration.NONE)

    async def focus_out(self):
        await self.dummy.focus()

    async def edit_tsk(self,  ):
        new_name = self.edit_panel_text_entry.value
        if new_name.strip():
            self.curr_task.task_name = new_name.strip()
            self.curr_task.label.value = new_name.strip()
            self.curr_task.update()
        else:
            self.edit_panel_text_entry.value = self.curr_task.task_name
        await self.focus_out()


    def delete_tsk(self, task: Task, ):
        self.tasks_area.content.controls.remove(task)

   




class Task(ft.Container):
    def __init__(self,
                  task_name: str = "", edit_func:Callable[["Task"], None] = field(default=lambda task: None),
                  on_task_delete: Callable[["Task"], None] = field(default=lambda task: None),
                  
                  ):
        super().__init__()
        self.blur = ft.Blur(10, 10, ft.BlurTileMode.MIRROR)
        self.delete = on_task_delete
        self.is_editing = False
        self.on_click = lambda e: edit_func(self)
        self.bgcolor = ft.Colors.with_opacity(0.45, "#6b6b6b") 
        self.padding = ft.Padding.symmetric(horizontal=10, vertical=8)
        self.task_name = task_name
        self.cb = ft.Checkbox(shape=ft.CircleBorder(), on_change=self.on_cb_click)
        self.is_favorite = False
        self.favorite = ft.IconButton(icon=ft.Icons.STAR, on_click=self.on_favorite_click,)
        self.label = ft.Text(value=self.task_name, align=ft.Alignment.TOP_LEFT,expand = True,
            style=ft.TextStyle(
                decoration=ft.TextDecoration.NONE,
                decoration_thickness=2,
            ), 
            theme_style=ft.TextThemeStyle.TITLE_MEDIUM, font_family="Segoe UI"
        )


        self.content = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            controls=[
                self.cb,
                self.label,
                self.favorite




             ],
        )

    def on_cb_click(self):
        if self.is_editing:
            self.on_click(None)
        value = self.label.style
        if self.cb.value:
             value.decoration = ft.TextDecoration.LINE_THROUGH
        else:
            value.decoration = ft.TextDecoration.NONE

    def on_favorite_click(self):

        if not self.is_favorite:
            
            self.favorite.icon_color = ft.Colors.DEEP_PURPLE_ACCENT  
        else:
            self.favorite.icon_color = None
        self.is_favorite = not self.is_favorite
        


    def delete_task(self,):
        self.delete(self)                          

    def edit_task(self,):
        self.edit(self)        
                                 
                                 

def main(page: ft.Page):
    page.title = "To-Do App"
    page.decoration = ft.BoxDecoration(image=ft.DecorationImage(src="https://images.hdqwalls.com/download/lavender-field-anime-girl-5k-8a-3440x1440.jpg", fit=ft.BoxFit.COVER,),)
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.padding = 0
    page.theme_mode = "dark"
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.PINK_50)
    page.bgcolor = ft.Colors.TRANSPARENT
    app = TodoApp()
    
    # add application's root control to the page
    page.add(app)
    page.update()
    

ft.run(main, ) 