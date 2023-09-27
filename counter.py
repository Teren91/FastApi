import flet as ft
import flet_fastapi

async def main(page: ft.Page):
    counter = ft.Text("0", size=50, data=0)

    async def add_click(e):
        counter.data += 2
        counter.value = str(counter.data)
        await counter.update_async()

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.icons.ADD, on_click=add_click
    )
    await page.add_async(
        ft.Container(counter, alignment=ft.alignment.center, expand=True)
    )

async def sub_main(page: ft.Page):
    await page.add_async(ft.Text("This is sub app!"))


app = flet_fastapi.FastAPI()


#app.mount("/sub-app", flet_fastapi.app(sub_main))
app.mount("/", flet_fastapi.app(main))