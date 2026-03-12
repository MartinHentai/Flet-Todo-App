import flet as ft


@ft.component
def drag(i, num, func):
    width= 800
    height= 50
    is_dragged, set_drag_over = ft.use_state(False)


    def click(e):
        print(e)

    def will_accept(e):
        set_drag_over(True)



    def accept(e):
        set_drag_over(False)
        print("SOURCE :", e.src.content.title)
        print("Dragged item id", e.src.data)
        print("DESTINATION :", e.control.content.controls[1].content.title)
        print("DESTINATION I :", i)

        func(old_index=e.src.data,new_index=i)

    def leave(e):
        set_drag_over(False)

    



    return ft.DragTarget(
        expand=1,
        
        on_will_accept=will_accept,
        on_leave=leave,
        on_accept=accept,
        
        content=ft.Column(
            spacing=0,
            controls=[
                ft.Container(
                    height=50 if is_dragged else 0,
                    animate=ft.Animation(300,ft.AnimationCurve.EASE_IN_OUT),
                    bgcolor=ft.Colors.TRANSPARENT,
                ),
                ft.Draggable( 
                    data=i,
                    content=ft.ListTile(
                        trailing=ft.IconButton(icon=ft.Icons.ABC, on_click=click),
                        expand=1,
                        title=(f"Item {num}"),
                        bgcolor="#999999",
                        height= 50,
                    ),
                    
                    content_when_dragging=ft.Container(height=0),
                    content_feedback=ft.Container(
                        bgcolor="#ff0000",
                        width= 800,
                        height= 50,
                        content=ft.ListTile(
                            title=(f"Item {num}"),
                            bgcolor="#FF0000",
                        )
                    

                    )
                )
            ]
        )
    ) 
                    
                



@ft.component
def drags():

    items, set_items = ft.use_state(list(range(20)))

    def reorder(old_index, new_index):
        copy = items.copy()
        if old_index < new_index:
            new_index = new_index -1
        moved_item = copy.pop(old_index)
        copy.insert(new_index, moved_item)
        set_items(copy)



    

    return ft.Container(
        expand=1,
        content=ft.ListView(
            expand=1,
            spacing=3,
            controls=[drag(i=i, num=num, func=reorder) for i, num in enumerate(items)]
        )
    )







def main(page):
    page.render(drags) 
ft.run(main=main)