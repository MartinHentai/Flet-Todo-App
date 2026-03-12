import flet as ft

class TodoApp(ft.Row):
    def __init__(self, ):
        super().__init__()          # important!

        self.expand = True
        self.spacing = 0

        # ====================== LEFT NAVIGATION ======================
        self.nav_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_extended_width=200,
            extended=True,
            destinations=[                 
                ft.NavigationRailDestination(icon=ft.Icons.WB_SUNNY_OUTLINED, label="My Day"),
                ft.NavigationRailDestination(icon=ft.Icons.STAR_OUTLINED, label="Important"),
                ft.NavigationRailDestination(icon=ft.Icons.CALENDAR_TODAY, label="Planned"),
                ft.NavigationRailDestination(icon=ft.Icons.LIST, label="Tasks"),
                ft.NavigationRailDestination(icon=ft.Icons.PERSON_OUTLINE, label="Assigned to me"),
                ft.NavigationRailDestination(icon=ft.Icons.CHECK_CIRCLE_OUTLINE, label="Completed"),],
            on_change=self.change_view,   # ← direct method, no lambda needed
        )

        # ====================== MAIN TASK LIST ======================
        self.task_list = ft.ListView(
            expand=True,
            spacing=6,
            padding=ft.padding.all(20),
        )
        for i in range(30):
            t = Task(task_name=f"Task {i + 1} – this is a sample task")
            self.task_list.controls.append(t)

        self.main_area = ft.Container(
            content=self.task_list,
            expand=True,
        )

        # ====================== RIGHT PANEL ======================
        right_panel = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Right Panel", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("Filters, stats, or selected task details go here"),
                ],
                spacing=20,
            ),
            width=340,
            bgcolor=ft.Colors.with_opacity(0.95, ft.Colors.BLUE_GREY_900),
            padding=20,
            border=ft.border.only(left=ft.border.BorderSide(1, ft.Colors.BLUE_GREY_800)),
        )

        self.controls = [
            self.nav_rail,
            ft.VerticalDivider(width=1, color=ft.Colors.RED_100),
            self.main_area,
            right_panel,
        ]

    def change_view(self, e: ft.ControlEvent):
        index = e.control.selected_index
        if index == 0:
            self.main_area.content = ft.Text("My Day view (you can put another ListView here)", size=30)
        elif index == 1:
            self.main_area.content = ft.Text("Important view", size=30)
        else:
            self.main_area.content = self.task_list
        self.page.update()


class Task(ft.Container):
    def __init__(self, task_name: str = ""):
        super().__init__()
        self.task_name = task_name
        self.bgcolor = "#1E1E1E"
        self.padding = ft.padding.symmetric(horizontal=10, vertical=8)

        self.check_box = ft.Checkbox(
            shape=ft.CircleBorder(),
            on_change=self._toggle_strike,
        )
        self.label = ft.Text(
            value=self.task_name,
            style=ft.TextStyle(
                decoration=ft.TextDecoration.NONE,
                decoration_thickness=2,
            ),
            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
            font_family="Segoe UI",
            expand=True,
        )
        self.content = ft.Row(
            controls=[self.check_box, self.label],
            alignment=ft.MainAxisAlignment.START,
        )

    def _toggle_strike(self, e):
        self.label.style.decoration = (
            ft.TextDecoration.LINE_THROUGH if self.check_box.value else ft.TextDecoration.NONE
        )
        self.update()


def main(page: ft.Page):
    page.title = "To-Do App"
    page.padding = 0
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.theme_mode = "dark"
    page.bgcolor = ft.Colors.TRANSPARENT
    page.decoration = ft.BoxDecoration(
        image=ft.DecorationImage(
            src="https://images.hdqwalls.com/download/lavender-field-anime-girl-5k-8a-3440x1440.jpg",
            fit=ft.BoxFit.COVER,
        )
    )

    app = TodoApp()
    page.add(app)
    page.update()


ft.run(main)