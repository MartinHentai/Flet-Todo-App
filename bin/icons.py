import asyncio
import os
from itertools import islice

import flet as ft

os.environ["FLET_WS_MAX_MESSAGE_SIZE"] = "8000000"
ft.context.disable_auto_update()   # recommended for large lists / batch updates


class IconBrowser(ft.Container):
    def __init__(self, expand=False, height=500):
        super().__init__()
        if expand:
            self.expand = expand
        else:
            self.height = height

    def build(self):
        def batches(iterable, batch_size):
            iterator = iter(iterable)
            while batch := list(islice(iterator, batch_size)):
                yield batch

        # fetch all icon enum members (new in 0.80+)
        icons_list = list(ft.Icons)

        search_txt = ft.TextField(
            expand=1,
            hint_text="Enter keyword and press search button. To view all icons enter *",
            autofocus=True,
            on_submit=lambda e: asyncio.create_task(display_icons(e.control.value)),
        )

        async def search_click(e):
            await display_icons(search_txt.value)

        search_query = ft.Row(
            [search_txt, ft.IconButton(icon=ft.Icons.SEARCH, on_click=search_click)]
        )

        search_results = ft.GridView(
            expand=1,
            runs_count=10,
            max_extent=150,
            spacing=5,
            run_spacing=5,
            child_aspect_ratio=1,
        )
        status_bar = ft.Text()

        async def copy_to_clipboard(e):
            icon_key = e.control.data
            print("Copy to clipboard:", icon_key)
            await ft.Clipboard().set(icon_key)          # new Clipboard service
            self.page.show_dialog(
                ft.SnackBar(ft.Text(f"Copied {icon_key}"))
            )                                           # new way to show SnackBar

        def search_icons(search_term: str):
            all_icons = False
            for icon in icons_list:                     # now yield enum member
                icon_name = icon.name
                if all_icons or search_term:
                    if search_term and search_term in icon_name:
                        all_icons = False
                        yield icon
                    elif search_term == "*":
                        all_icons = True
                        search_term = ""
                        yield icon
                    elif search_term == "" and all_icons:
                        yield icon
                    else:
                        all_icons = False

        async def display_icons(search_term: str):
            # clean search results
            search_query.disabled = True
            self.update()

            search_results.controls.clear()
            search_results.update()

            for batch in batches(search_icons(search_term.upper()), 200):
                for icon in batch:
                    icon_name = icon.name
                    icon_key = f"ft.Icons.{icon_name}"
                    search_results.controls.append(
                        ft.TextButton(
                            content=ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Icon(icon=icon, size=30),   # now accepts enum member
                                        ft.Text(
                                            value=icon_name,
                                            size=12,
                                            width=100,
                                            no_wrap=True,
                                            text_align=ft.TextAlign.CENTER,
                                            color=ft.Colors.ON_SURFACE_VARIANT,
                                        ),
                                    ],
                                    spacing=5,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                alignment=ft.Alignment.CENTER,
                            ),
                            tooltip=f"{icon_key}\nClick to copy to clipboard",
                            on_click=copy_to_clipboard,
                            data=icon_key,
                        )
                    )
                status_bar.value = f"Icons found: {len(search_results.controls)}"
                self.update()
                await asyncio.sleep(0.05)   # keep UI responsive during large batches

            if len(search_results.controls) == 0:
                self.page.show_dialog(ft.SnackBar(ft.Text("No icons found")))

            search_query.disabled = False
            self.update()

        self.content = ft.Column(
            [
                search_query,
                search_results,
                status_bar,
            ],
            expand=True,
        )


def main(page: ft.Page):
    page.title = "Flet icons browser"
    page.add(IconBrowser(expand=True))


ft.run(main)   # ← new entry point