from dataclasses import field
from typing import Callable

import flet as ft


@ft.control
class TodoApp(ft.Row):
    def init(self):
        self.expand = True
        self.spacing = 0                     # no gap between panels
        self.vertical_alignment = ft.CrossAxisAlignment.STRETCH

        # ===================== LEFT NAV (Microsoft To-Do style) =====================
        self.nav_rail = ft.NavigationRail(
            selected_index=0,
            extended=True,                   # shows labels like real To-Do
            min_extended_width=260,
            label_type=ft.NavigationRailLabelType.ALL,
            bgcolor=ft.Colors.with_opacity(0.95, "#1E1E1E"),
            destinations=[
                ft.NavigationRailDestination(icon=ft.Icons.WB_SUNNY_OUTLINED, label="My Day"),
                ft.NavigationRailDestination(icon=ft.Icons.STAR_OUTLINED, label="Important"),
                ft.NavigationRailDestination(icon=ft.Icons.CALENDAR_TODAY, label="Planned"),
                ft.NavigationRailDestination(icon=ft.Icons.LIST, label="Tasks"),
                ft.NavigationRailDestination(icon=ft.Icons.PERSON_OUTLINE, label="Assigned to me"),
                ft.NavigationRailDestination(icon=ft.Icons.CHECK_CIRCLE_OUTLINE, label="Completed"),
                # you can add a Divider + custom lists later
            ],
            # on_change=self.on_nav_change,   # ← hook for switching views later
        )

        # ===================== MIDDLE - TASK LIST (scrollbar now perfect) =====================
        self.tasks = ft.ListView(
            expand=True,
            spacing=8,
            padding=ft.Padding.only(left=16, right=8, top=16, bottom=16),  # right=8 so scrollbar sits inside
            controls=[Task(task_name=f"Task {i+1}") for i in range(130)],
        )

        self.tasks_area = ft.Container(
            expand=True,
            content=self.tasks,
            # clip_behavior makes sure nothing ever leaks outside
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )

        # ===================== RIGHT PANEL =====================
        self.right_panel = ft.Container(
            width=380,
            bgcolor=ft.Colors.with_opacity(0.98, "#1E1E1E"),
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Text("Task details", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("Select a task on the left to see details here", 
                           color=ft.Colors.ON_SURFACE_VARIANT),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        self.controls = [
            self.nav_rail,
            self.tasks_area,
            self.right_panel,
        ]

    def on_nav_change(self, e):
        # TODO: here you will later filter the ListView depending on selected tab
        print("Selected tab:", e.control.selected_index)


@ft.control
class Task(ft.Container):
    task_name: str = ""

    def init(self):
        self.bgcolor = "#aa1E1E1E"
        self.border_radius = 8
        self.padding = ft.Padding.all(12)

        self.check_box = ft.Checkbox(shape=ft.CircleBorder())
        self.label = ft.Text(
            value=self.task_name,
            expand=True,
            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
        )

        self.content = ft.Row(
            controls=[self.check_box, self.label],
            alignment=ft.MainAxisAlignment.START,
        )


def main(page: ft.Page):
    page.title = "To-Do App"
    page.decoration = ft.BoxDecoration(
        image=ft.DecorationImage(
            src="https://images.hdqwalls.com/download/lavender-field-anime-girl-5k-8a-3440x1440.jpg",
            fit=ft.BoxFit.COVER,
        )
    )
    page.padding = 0                     # ← this + stretch fixes scrollbar "outside window"
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.TRANSPARENT

    app = TodoApp()
    page.add(app)
    page.update()


ft.run(main)