# Astral Hub

Aplicación de escritorio hecha con Python y Flet. Este proyecto mantiene el código existente y concentra los cambios de mejora en la rama `mejoras-astral-hub`.

## Requisitos

- Python compatible con la versión de Flet fijada en `requirements.txt`
- Dependencias del proyecto: `pip install -r requirements.txt`

## Ejecutar

Desde la carpeta del proyecto:

```bash
pip install -r requirements.txt
python main.py
```

## Panel de administración

El PIN ya no está escrito en el código. Para habilitar el panel, define la variable de entorno `ASTRAL_ADMIN_PIN` antes de ejecutar la aplicación. No guardes el PIN en el repositorio.

Ejemplo en PowerShell:

```powershell
$env:ASTRAL_ADMIN_PIN = "elige-un-pin-propio"
python main.py
```

Ejemplo en macOS/Linux:

```bash
export ASTRAL_ADMIN_PIN="elige-un-pin-propio"
python main.py
```

Si la variable no está configurada, el panel de administración permanece desactivado.

## Nota importante de seguridad

Las cuentas se guardan en el almacenamiento local de Flet. **Ese almacenamiento no debe considerarse cifrado por defecto**; los cambios actuales validan los datos y avisan si falla la lectura o escritura, pero no cifran las contraseñas. Evita guardar credenciales reales o sensibles hasta que se implemente y pruebe una solución de almacenamiento seguro adecuada para la plataforma de destino.

## Estado

Los cambios de desarrollo se realizan en `mejoras-astral-hub`; no se modifica `main` durante esta etapa. Los cambios deben probarse en el entorno de destino antes de publicarse.
