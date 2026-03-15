import flet as ft
import asyncio


ANIM_DURATION = 600
OFF_ANIMATION_AFTER = ANIM_DURATION/1000 + 0.05

@ft.component
def drag(i, num, func, last_droped):
    width= 800
    is_dragged, set_drag_over = ft.use_state(False)
    is_hovered, handle_hover = ft.use_state(False)

    def render_hover(e):
        handle_hover(e.data == True) 

    bg_color = ft.Colors.WHITE10 if ( is_hovered) else ft.Colors.TRANSPARENT
    
    

    def click(e):
        print(e)

    def will_accept(e):
        set_drag_over(True)



    def accept(e):
        set_drag_over(False)
        handle_hover(False)
        func(old_index=e.src.data,new_index=i)

    def leave(e):
        set_drag_over(False)
        handle_hover(False)
    
    def set_opacity(e, n):
        e.control.parent.parent.parent.parent.opacity = n


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
                    animate=ft.Animation(200,ft.AnimationCurve.EASE_IN_OUT),
                    bgcolor=ft.Colors.TRANSPARENT,
                ),
                ft.Draggable( 
                    data=i, 
                    content=ft.Container(
                        height=40,
                        width=width,
                        border_radius = ft.BorderRadius.all(50),
                        padding = ft.Padding.only(left=10, right=10),
                        on_hover= render_hover,
                        bgcolor=bg_color,
                        content=ft.AnimatedSwitcher(
                            duration=ANIM_DURATION if last_droped  else 0,
                            reverse_duration=0,
                            transition=ft.AnimatedSwitcherTransition.FADE , 
                            switch_in_curve=ft.AnimationCurve.EASE_IN_CUBIC,
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.START,
                                controls=[
                                    ft.Icon(ft.Icons.ABC, size=20, color=ft.Colors.WHITE70), 
                                    ft.Text(value=(f"Item {num}"), size=14, expand=True, color=ft.Colors.WHITE),             
                                ],
                            )
                        )
                    ),
                    content_when_dragging=ft.Container(height=0),
                    content_feedback=ft.Container(
                        height=40,
                        width= width,
                        border_radius = ft.BorderRadius.all(50),
                        padding = ft.Padding.only(left=10, right=10),
                        on_hover= render_hover,
                        bgcolor=bg_color,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.START,
                            controls=[
                                ft.Icon(ft.Icons.ABC, size=20, color=ft.Colors.WHITE70), 
                                ft.Text(value=(f"Item {num}"), size=14, expand=True, color=ft.Colors.WHITE),             
                            ],
                        )
                    ),
                    

                )
            ]
        )
    ) 
                    
                



@ft.component
def drags():

    items, set_items = ft.use_state(list(range(20)))
    last_droped, set_droped = ft.use_state(None)

    def reorder(old_index, new_index):
        copy = items.copy()
        if old_index < new_index:
            new_index -= 1
        moved_item = copy.pop(old_index)
        copy.insert(new_index, moved_item)
        set_droped(moved_item)
        set_items(copy)

        async def clear_drop_state():
            await asyncio.sleep(OFF_ANIMATION_AFTER) # Wait 650ms (just slightly longer than your 600ms fade)
            set_droped(None)

        ft.context.page.run_task(clear_drop_state)



    

    return ft.Container(
        expand=1,
        content=ft.ListView(
            # opacity=0.5,
            expand=1,
            spacing=3,
            controls=[drag(i=i, num=num, func=reorder,last_droped=last_droped==num) for i, num in enumerate(items)]
        )
    )







def main(page):
    page.render(drags) 
ft.run(main=main)