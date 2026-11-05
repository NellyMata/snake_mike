
# Importación de las bibliotecas necesarias.
import pygame
import sys

# Inicialización de los módulos de Pygame.
pygame.init()

# Definición de las dimensiones de la ventana en píxeles.
ANCHO = 800
ALTO = 600

# Creación de la ventana principal de la escena interactiva.
pantalla = pygame.display.set_mode((ANCHO, ALTO))

# Configuración del título de la ventana.
pygame.display.set_caption("Mi escena interactiva")

# Creación del reloj para controlar los fotogramas por segundo.
reloj = pygame.time.Clock()

# Definición de los colores mediante valores RGB.
BLANCO = (255, 255, 255)
AZUL = (50, 120, 220)
VERDE = (50, 180, 90)

# Creación del rectángulo que representa al personaje.
# Los valores indican posición horizontal, posición vertical, ancho y alto.
personaje = pygame.Rect(50, 50, 40, 40)

# Creación del rectángulo que representa al objetivo estático.
objetivo = pygame.Rect(650, 450, 50, 50)
# Definición de la velocidad de movimiento del personaje.
VELOCIDAD = 5
# Definición del ancho de la ventana en píxeles.
ANCHO = 800

# Definición de la altura de la ventana en píxeles.
ALTO = 600
# Variable de control para mantener activo el programa.
ejecutando = True
# Variable para registrar si el objetivo ya fue alcanzado.
objetivo_alcanzado = False

# Bucle principal de ejecución de la escena.
while ejecutando:

    # Detección y procesamiento de los eventos de Pygame.
    for evento in pygame.event.get():

        # Finalización del bucle cuando se solicita cerrar la ventana.
        if evento.type == pygame.QUIT:
            ejecutando = False

    
    # Detección de las teclas presionadas.
    teclas = pygame.key.get_pressed()
    
    # Movimiento hacia la izquierda con A o la flecha izquierda.
    if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
        personaje.x -= VELOCIDAD

    # Movimiento hacia la derecha con D o la flecha derecha.
    if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
        personaje.x += VELOCIDAD

    # Movimiento hacia arriba con W o la flecha arriba.
    if teclas[pygame.K_w] or teclas[pygame.K_UP]:
        personaje.y -= VELOCIDAD

    # Movimiento hacia abajo con S o la flecha abajo.
    if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
        personaje.y += VELOCIDAD

    # Limitación del movimiento dentro de los bordes de la ventana.
    personaje.clamp_ip(pantalla.get_rect())
    # Relleno del fondo con color blanco.
    pantalla.fill(BLANCO)

    # Dibujo del personaje mediante un rectángulo azul.
    pygame.draw.rect(pantalla, AZUL, personaje)

    # Dibujo del objetivo mediante un rectángulo verde.
    
    pygame.draw.rect(pantalla, VERDE, objetivo)
    # Detección de colisión cuando el objetivo aún no ha sido alcanzado.
    if personaje.colliderect(objetivo) and not objetivo_alcanzado:
       print("¡Felicidades! Se alcanzó el objetivo.")
       objetivo_alcanzado = True
    # Actualización de la pantalla para mostrar los elementos dibujados.
    pygame.display.flip()

    # Control de la velocidad de ejecución a 60 fotogramas por segundo.
    reloj.tick(60)

# Cierre de los módulos de Pygame al finalizar el bucle principal.
pygame.quit()

# Finalización del programa.
sys.exit()
