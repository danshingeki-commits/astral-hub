import flet as ft
import json
import os

# Archivo de base de datos local para guardar las cuentas
DB_FILE = "cuentas_astralhub.json"

def main(page: ft.Page):
    # --- CONFIGURACIÓN DE LA APP ---
    page.title = "AstralHub - Gestor de Cuentas"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#090610" # Fondo oscuro estilo Liquid Glass
    page.padding = 20
    page.window_width = 400
    page.window_height = 750
    
    # --- 1. SOLUCIÓN DEL PANEL DE ADMIN ---
    # Cambiamos esto a False para que NUNCA te diga que está desactivado
    panel_adm_desactivado = False  

    # --- FUNCIONES DE BASE DE DATOS ---
    def cargar_cuentas():
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r") as f:
                return json.load(f)
        return []

    def guardar_cuentas(cuentas):
        with open(DB_FILE, "w") as f:
            json.dump(cuentas, f, indent=4)

    cuentas_db = cargar_cuentas()
    lista_cuentas = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=12)

    # --- INTERFAZ PRINCIPAL ---
    def actualizar_interfaz():
        lista_cuentas.controls.clear()
        
        if panel_adm_desactivado:
            # Este es el error que te salía antes. Ya no saldrá porque la variable es False.
            lista_cuentas.controls.append(
                ft.Container(
                    content=ft.Text("El panel de adm está desactivado 🚫", size=18, color=ft.colors.RED_400, weight="bold"),
                    alignment=ft.alignment.center,
                    margin=ft.margin.only(top=100)
                )
            )
        elif len(cuentas_db) == 0:
            # --- 2. EL MENSAJE CUANDO ESTÁS SOLITO ---
            lista_cuentas.controls.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(name=ft.icons.SENTIMENT_VERY_DISSATISFIED, size=90, color="#38BDF8"),
                            ft.Text("¿Por qué estoy solito? 🥺", size=24, color="#F8FAFC", weight=ft.FontWeight.BOLD),
                            ft.Text("No tienes ninguna cuenta guardada aún.", size=14, color="#94A3B8")
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    alignment=ft.alignment.center,
                    margin=ft.margin.only(top=150)
                )
            )
        else:
            # Dibuja las tarjetas de las cuentas si existen
            for cuenta in cuentas_db:
                lista_cuentas.controls.append(
                    ft.Container(
                        content=ft.ListTile(
                            leading=ft.Icon(ft.icons.ACCOUNT_CIRCLE, color="#C084FC", size=45),
                            title=ft.Text(cuenta['plataforma'], weight="bold", color="#F8FAFC", size=16),
                            subtitle=ft.Text(f"User: {cuenta['usuario']}", color="#94A3B8"),
                            trailing=ft.IconButton(
                                icon=ft.icons.DELETE_OUTLINE, 
                                icon_color=ft.colors.RED_400,
                                data=cuenta,
                                on_click=borrar_cuenta
                            )
                        ),
                        bgcolor="#150E24", # Cristal oscuro
                        border_radius=16,
                        border=ft.border.all(1, "#33C084FC") # Borde brillante neón
                    )
                )
        page.update()

    # --- LÓGICA DE BOTONES ---
    def borrar_cuenta(e):
        cuentas_db.remove(e.control.data)
        guardar_cuentas(cuentas_db)
        actualizar_interfaz()

    def agregar_cuenta(e):
        if not txt_plataforma.value or not txt_usuario.value:
            return
        
        nueva_cuenta = {
            "plataforma": txt_plataforma.value,
            "usuario": txt_usuario.value
        }
        cuentas_db.append(nueva_cuenta)
        guardar_cuentas(cuentas_db)
        
        txt_plataforma.value = ""
        txt_usuario.value = ""
        dlg_agregar.open = False
        actualizar_interfaz()

    # --- DIÁLOGO PARA AGREGAR CUENTAS ---
    txt_plataforma = ft.TextField(label="Plataforma (ej. Netflix, Spotify)", bgcolor="#1C1430", color="#F8FAFC", border_color="#38BDF8")
    txt_usuario = ft.TextField(label="Usuario / Correo", bgcolor="#1C1430", color="#F8FAFC", border_color="#38BDF8")

    dlg_agregar = ft.AlertDialog(
        title=ft.Text("Agregar Nueva Cuenta", color="#39C5BB"),
        content=ft.Column([txt_plataforma, txt_usuario], tight=True),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo()),
            ft.ElevatedButton("Guardar", on_click=agregar_cuenta, bgcolor="#C084FC", color="white")
        ],
        bgcolor="#0E0919",
        shape=ft.RoundedRectangleBorder(radius=20)
    )

    def abrir_dialogo(e):
        page.dialog = dlg_agregar
        dlg_agregar.open = True
        page.update()

    def cerrar_dialogo():
        dlg_agregar.open = False
        page.update()

    # --- ENCABEZADO (HEADER) ---
    header = ft.Row(
        controls=[
            ft.Text("ASTRAL HUB", size=26, weight="bold", color="#39C5BB", letter_spacing=2),
            ft.Container(expand=True),
            ft.IconButton(icon=ft.icons.ADD_CIRCLE_ROUNDED, icon_color="#38BDF8", icon_size=42, on_click=abrir_dialogo)
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # --- RENDERIZADO FINAL ---
    page.add(header, ft.Divider(color="#2A1E45", height=20), lista_cuentas)
    actualizar_interfaz()

# Iniciar la app nativa o web
ft.app(target=main)
