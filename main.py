import flet as ft
import json
import os

# Configure this outside the source code (environment variable).
# An empty value disables creator-panel access instead of using a public PIN.
ADMIN_PIN = os.environ.get("ASTRAL_ADMIN_PIN", "").strip()

PLATAFORMAS = [
    {"nombre": "Spotify", "cat": "Música", "icono": ft.Icons.MUSIC_NOTE, "color": "#1DB954"},
    {"nombre": "YouTube Music", "cat": "Música", "icono": ft.Icons.PLAY_CIRCLE_FILL, "color": "#FF0000"},
    {"nombre": "Apple Music", "cat": "Música", "icono": ft.Icons.MUSIC_VIDEO, "color": "#FA243C"},
    {"nombre": "Tidal HiFi", "cat": "Música", "icono": ft.Icons.DIAMOND, "color": "#00FFFF"},
    {"nombre": "Deezer", "cat": "Música", "icono": ft.Icons.EQUALIZER, "color": "#A238FF"},
    {"nombre": "Netflix", "cat": "Cine & TV", "icono": ft.Icons.MOVIE, "color": "#E50914"},
    {"nombre": "HBO Max", "cat": "Cine & TV", "icono": ft.Icons.LIVE_TV, "color": "#7928CA"},
    {"nombre": "Disney+", "cat": "Cine & TV", "icono": ft.Icons.AUTO_AWESOME, "color": "#113CCF"},
    {"nombre": "Prime Video", "cat": "Cine & TV", "icono": ft.Icons.VIDEO_LIBRARY, "color": "#00A8E1"},
    {"nombre": "Crunchyroll", "cat": "Cine & TV", "icono": ft.Icons.LOCAL_FIRE_DEPARTMENT, "color": "#FF6B00"},
    {"nombre": "Canva Pro", "cat": "Gaming & Pro", "icono": ft.Icons.PALETTE, "color": "#00C4CC"},
    {"nombre": "ChatGPT Plus", "cat": "Gaming & Pro", "icono": ft.Icons.SMART_TOY, "color": "#10A37F"},
    {"nombre": "Xbox Game Pass", "cat": "Gaming & Pro", "icono": ft.Icons.SPORTS_ESPORTS, "color": "#107C10"},
    {"nombre": "Discord Nitro", "cat": "Gaming & Pro", "icono": ft.Icons.CHAT_BUBBLE, "color": "#5865F2"},
]

def main(page: ft.Page):
    page.title = "Astral Hub"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0B0813"
    page.padding = 16
    page.scroll = ft.ScrollMode.AUTO

    def obtener_bd():
        try:
            raw = page.client_storage.get("astral_cuentas")
            datos = json.loads(raw) if raw else {}
            if not isinstance(datos, dict):
                return {}
            # Ignore malformed entries instead of crashing the account screen.
            bd_segura = {}
            for plataforma, cuentas in datos.items():
                if not isinstance(plataforma, str) or not isinstance(cuentas, list):
                    continue
                cuentas_validas = []
                for cuenta in cuentas:
                    if (
                        isinstance(cuenta, dict)
                        and isinstance(cuenta.get("usuario"), str)
                        and isinstance(cuenta.get("password"), str)
                    ):
                        cuentas_validas.append({
                            "usuario": cuenta["usuario"],
                            "password": cuenta["password"],
                        })
                bd_segura[plataforma] = cuentas_validas
            return bd_segura
        except (TypeError, ValueError, json.JSONDecodeError):
            return {}
        except Exception:
            mostrar_toast("⚠️ No se pudieron leer las cuentas guardadas")
            return {}

    def guardar_bd(datos):
        try:
            page.client_storage.set("astral_cuentas", json.dumps(datos))
            return True
        except Exception:
            mostrar_toast("❌ No se pudieron guardar los cambios en este dispositivo")
            return False

    bd = obtener_bd()
    filtro_actual = "Todos"
    toques_titulo = 0

    def mostrar_toast(mensaje):
        page.overlay.append(ft.SnackBar(ft.Text(mensaje), open=True))
        page.update()

    def abrir_cuentas_dialog(plat_nombre):
        cuentas = bd.get(plat_nombre, [])
        detalles = []

        if not cuentas:
            detalles.append(
                ft.Container(
                    content=ft.Text("😔 Sin cuentas disponibles por ahora.", color="#94A3B8"),
                    alignment=ft.alignment.center,
                    padding=20,
                )
            )
        else:
            for i, c in enumerate(cuentas, start=1):
                clave_visible = {"valor": False}
                texto_clave = ft.Text("••••••••", expand=True, color="#F8FAFC", size=13)

                def alternar_clave(e, control=texto_clave, estado=clave_visible, clave=c['password']):
                    estado["valor"] = not estado["valor"]
                    control.value = clave if estado["valor"] else "••••••••"
                    e.control.icon = ft.Icons.VISIBILITY_OFF if estado["valor"] else ft.Icons.VISIBILITY
                    e.control.tooltip = "Ocultar clave" if estado["valor"] else "Mostrar clave"
                    page.update()

                detalles.append(
                    ft.Container(
                        bgcolor="#171226",
                        border_radius=12,
                        padding=12,
                        margin=ft.margin.only(bottom=8),
                        border=ft.border.all(1, "#3B2D54"),
                        content=ft.Column([
                            ft.Text(f"CUENTA #{i}", size=11, color="#C084FC", weight=ft.FontWeight.BOLD),
                            ft.Row([
                                ft.Icon(ft.Icons.PERSON, size=16, color="#38BDF8"),
                                ft.Text(c['usuario'], expand=True, color="#F8FAFC", size=13),
                                ft.IconButton(
                                    ft.Icons.COPY,
                                    icon_size=16,
                                    icon_color="#38BDF8",
                                    tooltip="Copiar correo",
                                    on_click=lambda e, u=c['usuario']: [page.set_clipboard(u), mostrar_toast("Correo copiado")]
                                )
                            ]),
                            ft.Row([
                                ft.Icon(ft.Icons.KEY, size=16, color="#4ADE80"),
                                texto_clave,
                                ft.IconButton(
                                    ft.Icons.VISIBILITY,
                                    icon_size=16,
                                    icon_color="#C084FC",
                                    tooltip="Mostrar clave",
                                    on_click=alternar_clave
                                ),
                                ft.IconButton(
                                    ft.Icons.COPY,
                                    icon_size=16,
                                    icon_color="#4ADE80",
                                    tooltip="Copiar clave",
                                    on_click=lambda e, p=c['password']: [page.set_clipboard(p), mostrar_toast("Clave copiada")]
                                )
                            ])
                        ])
                    )
                )

        dlg = ft.AlertDialog(
            title=ft.Text(f"✦ {plat_nombre}", color="#E9D5FF", weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column(detalles, scroll=ft.ScrollMode.AUTO),
                width=340,
                height=300
            ),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo(dlg))],
            bgcolor="#120D1F"
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def cerrar_dialogo(dlg):
        dlg.open = False
        page.update()

    def abrir_panel_admin():
        sel_plat = ft.Dropdown(
            label="Plataforma",
            value="Spotify",
            options=[ft.dropdown.Option(p["nombre"]) for p in PLATAFORMAS],
            border_color="#7E22CE"
        )
        txt_smart = ft.TextField(
            label="⚡ Smart Paste (usuario:clave o lista)",
            multiline=True,
            min_lines=2,
            max_lines=5,
            border_color="#A855F7",
            hint_text="ej: correo@gmail.com:clave123\nO pega varias líneas de un golpe",
        )
        col_lista = ft.Column(scroll=ft.ScrollMode.AUTO, height=150)

        def recargar_lista_admin():
            col_lista.controls.clear()
            total = 0
            for plat, lista in bd.items():
                for idx, c in enumerate(lista):
                    total += 1
                    col_lista.controls.append(
                        ft.Container(
                            bgcolor="#1E1730",
                            border_radius=8,
                            padding=6,
                            margin=ft.margin.only(bottom=4),
                            content=ft.Row([
                                ft.Column([
                                    ft.Text(plat, size=12, weight=ft.FontWeight.BOLD, color="#C084FC"),
                                    ft.Text(c['usuario'], size=11, color="#38BDF8")
                                ], expand=True),
                                ft.IconButton(
                                    ft.Icons.DELETE_OUTLINE,
                                    icon_color="#EF4444",
                                    icon_size=18,
                                    on_click=lambda e, pl=plat, i=idx: borrar_cuenta(pl, i)
                                )
                            ])
                        )
                    )
            if total == 0:
                col_lista.controls.append(ft.Text("Sin cuentas guardadas.", color="#64748B", size=12))
            page.update()

        def borrar_cuenta(plat, idx):
            bd[plat].pop(idx)
            if not bd[plat]:
                del bd[plat]
            guardar_bd(bd)
            recargar_lista_admin()
            renderizar_grid()
            mostrar_toast("Cuenta eliminada")

        def guardar_cuentas(e):
            texto = txt_smart.value.strip()
            if not texto:
                mostrar_toast("⚠️ Pega al menos una cuenta")
                return

            plat = sel_plat.value
            if plat not in bd:
                bd[plat] = []

            guardadas = 0
            for linea in texto.split("\n"):
                linea = linea.strip()
                if not linea:
                    continue
                for sep in [":", "|", ";", "\t"]:
                    if sep in linea:
                        u, p = linea.split(sep, 1)
                        if u.strip() and p.strip():
                            bd[plat].append({"usuario": u.strip(), "password": p.strip()})
                            guardadas += 1
                        break

            if guardadas > 0:
                guardar_bd(bd)
                txt_smart.value = ""
                recargar_lista_admin()
                renderizar_grid()
                mostrar_toast(f"✅ {guardadas} cuenta(s) guardadas")
            else:
                mostrar_toast("⚠️ Usa el formato usuario:clave")

        recargar_lista_admin()

        dlg_admin = ft.AlertDialog(
            title=ft.Text("👑 Panel Astral Creator", color="#C084FC", weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    sel_plat,
                    txt_smart,
                    ft.ElevatedButton(
                        "➕ Guardar Cuentas",
                        bgcolor="#7E22CE",
                        color="white",
                        on_click=guardar_cuentas,
                        width=320
                    ),
                    ft.Divider(color="#3B2D54"),
                    ft.Text("Stock en memoria:", size=12, color="#A855F7", weight=ft.FontWeight.BOLD),
                    col_lista
                ], scroll=ft.ScrollMode.AUTO),
                width=340,
                height=430
            ),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo(dlg_admin))],
            bgcolor="#120D1F"
        )
        page.dialog = dlg_admin
        dlg_admin.open = True
        page.update()

    def pedir_pin():
        txt_pin = ft.TextField(
            label="PIN de acceso",
            password=True,
            can_reveal_password=True,
            text_align=ft.TextAlign.CENTER,
            border_color="#9333EA"
        )

        def comprobar_pin(e):
            if not ADMIN_PIN:
                mostrar_toast("⚠️ Panel desactivado: configura ASTRAL_ADMIN_PIN en el entorno")
                return
            if txt_pin.value == ADMIN_PIN:
                dlg_pin.open = False
                page.update()
                abrir_panel_admin()
            else:
                mostrar_toast("❌ PIN Incorrecto")

        dlg_pin = ft.AlertDialog(
            title=ft.Text("🔐 Acceso Creador", color="#E9D5FF"),
            content=ft.Container(content=txt_pin, width=280),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo(dlg_pin)),
                ft.ElevatedButton("Entrar", bgcolor="#7E22CE", color="white", on_click=comprobar_pin)
            ],
            bgcolor="#120D1F"
        )
        page.dialog = dlg_pin
        dlg_pin.open = True
        page.update()

    def click_titulo(e):
        nonlocal toques_titulo
        toques_titulo += 1
        if toques_titulo >= 5:
            toques_titulo = 0
            pedir_pin()

    header = ft.Container(
        content=ft.Column([
            ft.GestureDetector(
                content=ft.Text("✦ ASTRAL ✦", size=24, weight=ft.FontWeight.BOLD, color="#C084FC"),
                on_tap=click_titulo
            ),
            ft.Text("Portal Astral • Catálogo Digital", size=12, color="#94A3B8")
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        alignment=ft.alignment.center,
        margin=ft.margin.only(bottom=16)
    )

    buscador = ft.TextField(
        hint_text="Buscar plataforma...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=20,
        bgcolor="#171226",
        border_color="#3B2D54",
        height=45,
        content_padding=ft.padding.symmetric(horizontal=10),
        on_change=lambda e: renderizar_grid()
    )

    grid_cards = ft.ResponsiveRow(run_spacing=12, spacing=12)

    def cambiar_tab(e, cat):
        nonlocal filtro_actual
        filtro_actual = cat
        for btn in tabs_row.controls:
            btn.style = ft.ButtonStyle(
                bgcolor="#7E22CE" if btn.text == cat else "#171226",
                color="white" if btn.text == cat else "#94A3B8"
            )
        renderizar_grid()
        page.update()

    tabs = ["Todos", "Música", "Cine & TV", "Gaming & Pro"]
    tabs_row = ft.Row([
        ft.ElevatedButton(
            t,
            style=ft.ButtonStyle(
                bgcolor="#7E22CE" if t == "Todos" else "#171226",
                color="white" if t == "Todos" else "#94A3B8"
            ),
            on_click=lambda e, cat=t: cambiar_tab(e, cat)
        ) for t in tabs
    ], scroll=ft.ScrollMode.AUTO)

    def renderizar_grid():
        query = buscador.value.lower() if buscador.value else ""
        grid_cards.controls.clear()

        for plat in PLATAFORMAS:
            if filtro_actual != "Todos" and plat["cat"] != filtro_actual:
                continue
            if query and query not in plat["nombre"].lower():
                continue

            stock = len(bd.get(plat["nombre"], []))
            badge_color = "#4ADE80" if stock > 0 else "#64748B"
            badge_bg = "#14532D" if stock > 0 else "#1E293B"

            card = ft.Container(
                col={"xs": 6, "sm": 4, "md": 3},
                bgcolor="#150F24",
                border_radius=16,
                padding=14,
                border=ft.border.all(1, "#2E2145"),
                on_click=lambda e, n=plat["nombre"]: abrir_cuentas_dialog(n),
                content=ft.Column([
                    ft.Row([
                        ft.Icon(plat["icono"], color=plat["color"], size=28),
                        ft.Container(
                            content=ft.Text(f"{stock}", size=11, color=badge_color, weight=ft.FontWeight.BOLD),
                            bgcolor=badge_bg,
                            border_radius=10,
                            padding=ft.padding.symmetric(horizontal=8, vertical=2)
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(height=8),
                    ft.Text(plat["nombre"], size=14, weight=ft.FontWeight.BOLD, color="#F8FAFC"),
                    ft.Text(plat["cat"], size=11, color="#94A3B8")
                ])
            )
            grid_cards.controls.append(card)

        page.update()

    page.add(
        header,
        buscador,
        ft.Container(height=6),
        tabs_row,
        ft.Container(height=10),
        grid_cards
    )

    renderizar_grid()

if __name__ == "__main__":
    ft.app(target=main)
