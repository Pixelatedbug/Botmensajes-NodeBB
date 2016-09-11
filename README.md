# Botmensajes-NodeBB
Bot que cuenta el número de mensajes de cada usuario de los temas. Responde al ser llamado con una tabla.

### Para que funcione: 
1. Inicia sesión desde un navegador y copiarle la cookie express.sid en `Configuracion.py`
2. Pon el nick del bot para que reconozca las menciones en `Configuracion.py`

# Dependencies

Puedes instalarlas utilizando `pip install -r requirements.txt` o instalando tú mismo los siguientes paquetes:

### 1. Websocket-client

`pip install websocket-client` or download it from https://pypi.python.org/pypi/websocket-client

# Problemas
+ No cuenta exactamente los mensajes. Puede que al calcular varias páginas con varios hilos, alguna página se pierda por grabar los valores a la vez en la array.
