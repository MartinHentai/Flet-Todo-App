import flet as ft
from dataclasses import dataclass, field

@ft.observable
@dataclass
class Count:
    val: int = 0

    def minus_click(self,e):
        self.val -= 1


    def plus_click(self,e):
        self.val += 1



@ft.component
def counter():
    
    state, _ = ft.use_state(Count())

    return ft.Row(
        controls=[
                ft.IconButton(ft.Icons.REMOVE, on_click=state.minus_click),
                ft.Text(value=state.val, size=50, 
                        color=(
                            ft.Colors.RED if state.val < 0 else
                            ft.Colors.GREEN if state.val > 0 else
                            ft.Colors.BLACK)),
                ft.IconButton(ft.Icons.ADD, on_click=state.plus_click),
                ],
        alignment=ft.MainAxisAlignment.CENTER,
        )


def main(page: ft.Page):
    page.title = "Declarative Counter"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    page.render(counter)

ft.run(main)