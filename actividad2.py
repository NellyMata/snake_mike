import pygame
import random
import sys

# Inicializar Pygame y el sonido
pygame.init()
pygame.mixer.init()

# Cargar efectos de sonido
sonidos_comer = pygame.mixer.Sound("sonidos/comer.wav")
sonidos_perder = pygame.mixer.Sound("sonidos/perder.wav")
sonidos_nivel = pygame.mixer.Sound("sonidos/nivel.wav")

# Configuración de pantalla
ANCHO = 600
ALTO = 400
TAMANO = 20

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Snake - Mi primer videojuego")

# Colores
NEGRO = (15, 18, 25)
ROJO = (255, 75, 75)
BLANCO = (255, 255, 255)

fuente = pygame.font.Font(None, 30)
fuente_grande = pygame.font.Font(None, 55)
reloj = pygame.time.Clock()

# Cargar imágenes de los virus
virus_verde = pygame.image.load(
    "imagenes/virus/virus_verde.png"
).convert_alpha()

virus_naranja = pygame.image.load(
    "imagenes/virus/virus_naranja.png"
).convert_alpha()

virus_morado = pygame.image.load(
    "imagenes/virus/virus_morado.png"
).convert_alpha()

virus_rojo = pygame.image.load(
    "imagenes/virus/virus_rojo.png"
).convert_alpha()

# Preparar virus para los cuatro niveles
virus_por_nivel = [
    pygame.transform.smoothscale(virus, (30, 30))
    for virus in (
        virus_verde,
        virus_naranja,
        virus_morado,
        virus_rojo
    )
]

# Cargar imágenes de las serpientes
hoja_serpientes = pygame.image.load(
    "imagenes/serpientes_niveles.png"
).convert_alpha()

cabezas = []
cuerpos = []

for fila in range(4):
    y = fila * 256

    cabeza = hoja_serpientes.subsurface(
        (10, y + 5, 215, 245)
    )

    cuerpo = hoja_serpientes.subsurface(
        (235, y + 60, 170, 150)
    )

    cabezas.append(
        pygame.transform.scale(cabeza, (TAMANO, TAMANO))
    )

    cuerpos.append(
        pygame.transform.scale(cuerpo, (TAMANO, TAMANO))
    )


# Crear comida en una posición libre
def crear_comida(serpiente):
    while True:
        x = random.randrange(0, ANCHO, TAMANO)
        y = random.randrange(0, ALTO, TAMANO)
        posicion = (x, y)

        if posicion not in serpiente:
            return posicion


# Reiniciar todos los datos de la partida
def nueva_partida():
    serpiente = [
        (300, 200),
        (280, 200),
        (260, 200)
    ]

    direccion = (TAMANO, 0)
    comida = crear_comida(serpiente)
    puntuacion = 0
    perdido = False

    return serpiente, direccion, comida, puntuacion, perdido


# Iniciar partida
serpiente, direccion, comida, puntuacion, perdido = nueva_partida()

ejecutando = True

# Bucle principal del videojuego
while ejecutando:

    # Procesar eventos del teclado
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            ejecutando = False

        elif evento.type == pygame.KEYDOWN:

            if perdido and evento.key == pygame.K_r:
                serpiente, direccion, comida, puntuacion, perdido = nueva_partida()

            elif not perdido:

                if evento.key == pygame.K_UP and direccion != (0, TAMANO):
                    direccion = (0, -TAMANO)

                elif evento.key == pygame.K_DOWN and direccion != (0, -TAMANO):
                    direccion = (0, TAMANO)

                elif evento.key == pygame.K_LEFT and direccion != (TAMANO, 0):
                    direccion = (-TAMANO, 0)

                elif evento.key == pygame.K_RIGHT and direccion != (-TAMANO, 0):
                    direccion = (TAMANO, 0)

    # Movimiento de la serpiente
    if not perdido:

        cabeza_x = serpiente[0][0] + direccion[0]
        cabeza_y = serpiente[0][1] + direccion[1]

        nueva_cabeza = (cabeza_x, cabeza_y)

        # Comprobar si encontró comida
        comio = nueva_cabeza == comida

        # Evitar colisiones incorrectas con la cola
        cuerpo_a_comprobar = (
            serpiente if comio else serpiente[:-1]
        )

        # Detectar colisiones
        if (
            cabeza_x < 0
            or cabeza_x >= ANCHO
            or cabeza_y < 0
            or cabeza_y >= ALTO
            or nueva_cabeza in cuerpo_a_comprobar
        ):
            perdido = True
            sonidos_perder.play()

        else:
            serpiente.insert(0, nueva_cabeza)

            if comio:
                puntuacion += 1
                sonidos_comer.play()

                # Cambiar nivel cada cinco puntos
                if puntuacion % 5 == 0 and puntuacion <= 15:
                    sonidos_nivel.play()

                comida = crear_comida(serpiente)

            else:
                serpiente.pop()

    # Dibujar el fondo
    pantalla.fill(NEGRO)

    # Seleccionar nivel
    nivel = min(puntuacion // 5, 3)

    # Dibujar virus
    virus_actual = virus_por_nivel[nivel]

    pantalla.blit(
        virus_actual,
        (comida[0] - 5, comida[1] - 5)
    )

    # Dibujar serpiente
    for i, segmento in enumerate(serpiente):

        if i == 0:
            imagen = cabezas[nivel]
        else:
            imagen = cuerpos[nivel]

        pantalla.blit(imagen, segmento)

    # Mostrar puntuación
    texto = fuente.render(
        f"Puntuacion: {puntuacion}",
        True,
        BLANCO
    )

    pantalla.blit(texto, (10, 10))

    # Pantalla de Game Over
    if perdido:

        mensaje = fuente_grande.render(
            "GAME OVER", True, ROJO
        )

        reiniciar = fuente.render(
            "Presiona R para reiniciar",
            True,
            BLANCO
        )

        pantalla.blit(
            mensaje,
            (
                ANCHO // 2 - mensaje.get_width() // 2,
                ALTO // 2 - 35
            )
        )

        pantalla.blit(
            reiniciar,
            (
                ANCHO // 2 - reiniciar.get_width() // 2,
                ALTO // 2 + 20
            )
        )

    # Actualizar pantalla y controlar velocidad
    pygame.display.flip()
    reloj.tick(10)

# Cerrar Pygame
pygame.quit()
sys.exit()