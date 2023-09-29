import flet as ft
import flet_fastapi
from routers import products, users, basic_auth_users, jwt_auth_users, users_db




async def main(page: ft.Page):
    page.title= "Testing FastApi + Flet"
    page.window_max_width = 360,
    page.window_max_height = 740,

    async def btnCreate_clicked(e):
        await users_db.create_user(txtUsername.value, txtEmail.value)
        print(await users_db.getUsers())

    async def btnUpdate_clicked(e):
        await users_db.update_user(txtUsername.value, txtEmail.value)
        print(await users_db.getUsers())

    async def btnDelete_clicked(e):
        await users_db.delete_user(txtUsername.value)
        print(await users_db.getUsers())


    txtUsername = ft.TextField(label="Enter username",
                    border=ft.InputBorder.UNDERLINE,
                    filled=True,
                    hint_text="Enter username")
    
    txtEmail =  ft.TextField(label="Enter email",
                    border=ft.InputBorder.UNDERLINE,
                    filled=True,
                    hint_text="Enter email")
    
    btnCreate = ft.ElevatedButton(
                            text="CREATE",
                            icon=ft.icons.ADD,
                            width=130,
                            height=40,
                            style=ft.ButtonStyle(
                            bgcolor={ ft.MaterialState.FOCUSED: ft.colors.PINK_700,
                                "": ft.colors.ORANGE_700},
                            color=ft.colors.PURPLE_800,
                            ),
                            on_click=btnCreate_clicked
                )
    btnUpdate = ft.ElevatedButton(text="UPDATE",
                              bgcolor=ft.colors.ORANGE_700,
                              color=ft.colors.PURPLE_800,
                              icon=ft.icons.UPDATE,
                              width=130,
                              height=40,
                              on_click=btnUpdate_clicked
                )
    
    btnDelete = ft.ElevatedButton(text="DELETE",
                              bgcolor=ft.colors.ORANGE_700,
                              color=ft.colors.PURPLE_800,
                              icon=ft.icons.DELETE,
                              width=130,
                              height=40,
                              on_click=btnDelete_clicked
                )

    await page.add_async (
        txtUsername,
        txtEmail,
        ft.Row([
            btnCreate,
            btnUpdate,
            btnDelete            
        ]),
    )
    await page.update_async()

app = flet_fastapi.app(main)

ft.app(target=main)

app.include_router(products.router)
app.include_router(users.router)

app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)

app.include_router(users_db.router)

#ft.app(target=main)
app.mount("/", flet_fastapi.app(main))