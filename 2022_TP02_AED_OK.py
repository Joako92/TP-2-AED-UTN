import random


def es_valido_opc_menu(num):
    numeros = ("1", "2", "3")
    return num in numeros


def es_numero(str_num):
    numeros = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')
    for car_num in str_num:
        if car_num not in numeros:
            return False
    return True


def puede_robar(puntaje_jugador, robo):
    return puntaje_jugador < 21 and (robo is None or len(robo) == 0 or robo not in ("s", "n") or robo == 's')


def agregar_al_pozo(pozo):
    print(">> Dispone de $", pozo)
    ingreso = solicitar_fondos(pozo, True)

    if ingreso != 0:
        pozo += ingreso
        print(">> Su nuevo pozo es de $", pozo)

    return pozo


def solicitar_fondos(fondos_actuales=0, permitir_cero_salir=False):
    if permitir_cero_salir:
        print(">> Ingrese 0 para salir")
    monto = None
    monto_str = input("Ingrese monto para el pozo (entre 1 y 100000): $")
    while monto_str == "":
        monto_str = input("Ingrese monto para el pozo (entre 1 y 100000): $")

    minimo = 1
    if permitir_cero_salir:
        minimo = 0

    if es_numero(monto_str):
        monto = int(monto_str)

    while monto is None or monto < minimo or (fondos_actuales + monto) > 100000:
        print("❌ ERROR! ❌ La cantidad ingresada no es valida (Mínimo", minimo, " - Máximo 100000)")
        if permitir_cero_salir:
            print(">> Ingrese 0 para salir")
        monto_str = input("Ingrese monto para el pozo (entre " + str(minimo) + " y 100000): $")
        if es_numero(monto_str):
            monto = int(monto_str)

    return monto


def solicitar_apuesta(pozo):
    apuesta = None

    apuesta_str = input("Realice su apuesta (Debe ser un multiplo de 5): $")
    while apuesta_str == "":
        apuesta_str = input("Realice su apuesta (Debe ser un multiplo de 5): $")

    if es_numero(apuesta_str):
        apuesta = int(apuesta_str)

    while apuesta is None or apuesta > pozo or apuesta < 1 or apuesta % 5 != 0:
        print("ERROR! La apuesta no es valida.")
        apuesta_str = input("Realice su apuesta (Debe ser un múltiplo de 5): $")
        if es_numero(apuesta_str):
            apuesta = int(apuesta_str)

    return apuesta


# Dada una carta y el puntaje actual, retorna el puntaje de la carta
# Rectroactividad en base a: https://uv.frc.utn.edu.ar/mod/forum/discuss.php?d=54315
def obtener_puntaje_carta(carta, puntaje, cantidad_as):
    valor_carta = carta[0]

    if valor_carta >= 10:  # JKQ
        puntaje += 10
    elif valor_carta == 1:
        cantidad_as += 1  # Cantidad AS
        puntaje += 11
    else:
        puntaje += valor_carta

    # Hacer retroactivos los AS
    while puntaje > 21 and cantidad_as > 0:
        puntaje -= 10
        cantidad_as -= 1

    return puntaje, cantidad_as


def mostrar_carta(carta):
    return "[" + carta[1] + " " + carta[2] + "] "


def es_blackjack(puntaje):
    return puntaje == 21


def jugar_mano():
    carta_jugador_1 = generar_carta()
    carta_jugador_2 = generar_carta()
    puntaje_jugador, cantidad_as_jug = obtener_puntaje_carta(carta_jugador_1, 0, 0)
    puntaje_jugador, cantidad_as_jug = obtener_puntaje_carta(carta_jugador_2, puntaje_jugador, cantidad_as_jug)
    es_bj_nat_jug = es_blackjack(puntaje_jugador)

    carta_crupier_1 = generar_carta()
    puntaje_crupier, cantidad_as_crup = obtener_puntaje_carta(carta_crupier_1, 0, 0)

    # Obtener los graficos de las cartas
    str_cartas_jugador = mostrar_carta(carta_jugador_1) + mostrar_carta(carta_jugador_2)
    str_cartas_crupier = mostrar_carta(carta_crupier_1)

    print("\nMANO INICIAL")
    print(">> Cartas del jugador:")
    print(str_cartas_jugador)
    print(">> Puntaje actual:", puntaje_jugador)
    print("\n>> Cartas crupier:")
    print(str_cartas_crupier)
    print(">> Puntaje actual:", puntaje_crupier)

    robo = None

    while puede_robar(puntaje_jugador, robo):
        if robo is not None and robo != "s":
            print("Valor ingresado no es valido")
        elif robo == "s":
            nueva_carta = generar_carta()
            puntaje_jugador, cantidad_as_jug = obtener_puntaje_carta(nueva_carta, puntaje_jugador, cantidad_as_jug)
            str_cartas_jugador += mostrar_carta(nueva_carta)
            print(str_cartas_jugador)
            print(">> Puntaje actual:", puntaje_jugador)

        if puntaje_jugador < 21:
            robo = input("\nQuiere robar otra carta (S/N)?:").lower()

    es_bj_nat_crup = False
    es_seg_carta_crupier = True

    input("\n>> Presione ENTER para continuar con el juego del croupier")
    print("\n>> Juego Crupier")
    while puntaje_crupier <= 16:
        print(">> El crupier da otra carta...")
        nueva_carta = generar_carta()
        puntaje_crupier, cantidad_as_crup = obtener_puntaje_carta(nueva_carta, puntaje_crupier, cantidad_as_crup)
        str_cartas_crupier += mostrar_carta(nueva_carta)
        print(str_cartas_crupier)
        print(">> Puntaje actual:", puntaje_crupier, "\n")

        # Comprobar si el crupier tiene un bj natural en la 2da carta
        if es_seg_carta_crupier:
            if es_blackjack(puntaje_crupier):
                es_bj_nat_crup = True

            es_seg_carta_crupier = False

    ganador = definir_ganador(puntaje_jugador, puntaje_crupier, es_bj_nat_jug, es_bj_nat_crup)
    return ganador, (es_bj_nat_jug or es_bj_nat_crup)


def definir_ganador(puntaje_jugador, puntaje_crupier, bj_nat_jug, bj_nat_crup):  # new
    if bj_nat_crup and bj_nat_jug:
        return 0
    elif bj_nat_crup:
        return -1
    elif bj_nat_jug:
        return 1
    else:
        # En caso de que se pasen, igualamos a 0
        if puntaje_crupier > 21:
            print(">> El crupier se pasó de 21")
            puntaje_crupier = 0

        if puntaje_jugador > 21:
            print(">> El jugador se pasó de 21")
            puntaje_jugador = 0

        if puntaje_crupier == puntaje_jugador:
            if puntaje_crupier != 0:
                return 0  # Empataron sin pasarse
            else:
                return -1  # Ambos se pasaron, entonces gana el crupier
        elif puntaje_jugador > puntaje_crupier:
            return 1
        else:
            return -1


def generar_carta():
    cartas = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
    palos = ("♥", "♦", "♣", "♠")

    valor_carta = random.randint(1, 13)  # Es representación de la carta ENTERO
    carta = cartas[valor_carta - 1]  # Signo de la carta STRING
    palo = random.choice(palos)  # Palo de la carta STRING

    # TUPLA: (VALOR CARTA, CARTA, PALO)
    return valor_carta, carta, palo


def programa():
    print("""    ♥♦#######################♣♠
    BIENVENIDO A BLACKJACK 1k12
    ♥♦#######################♣♠\n
    INSTRUCCIONES: El que llegue mas cerca de 21 gana!\n
    Iniciando configuracion inicial . . . """)

    # Nombre del jugador
    jugador = input("Ingrese nombre del jugador: ")
    # Si vacia se llama anonymus
    if len(jugador) == 0:
        print("El jugador se quiere mantener en el anonimato, se lo llamara: Anónimo")
        jugador = "Anónimo"

    print("Bienvenido,", jugador)

    monto = solicitar_fondos()

    # Variables estadisticas:
    partidas = 0
    partidas_ganadas_jugador = 0
    monto_maximo = monto
    may_racha_crup = 0
    ult_mano_gano_crup = None
    racha_actual_crup = 0
    cant_manos_bj_nat = 0
    acc_apuestas = 0
    mayor_perdida = None

    menu = """
  MENÚ:
    1- Apostar
    2- Jugar una mano
    3- Salir
  
  Ingrese una opción (1, 2 o 3):"""

    opc = None

    while opc is None or opc != 3:
        opc_str = input(menu)
        if es_valido_opc_menu(opc_str):
            opc = int(opc_str)  # Convertirlo en Int solo cuando el STR es valido
            if opc == 1:
                if monto >= 100000:
                    print(">> Usted ya tiene el maximo o más, no puede agregar más fondos")
                else:
                    monto = agregar_al_pozo(monto)
            elif opc == 2:
                print(">> Dispone de: $", monto)
                if monto >= 5:
                    apuesta = solicitar_apuesta(monto)

                    # Estadisticas
                    acc_apuestas += apuesta
                    partidas += 1

                    print(">> Su apuesta: $", apuesta)

                    ganador, hubo_bj_natural = jugar_mano()

                    if hubo_bj_natural:
                        cant_manos_bj_nat += 1

                    if ganador == 1:  # Jugador
                        partidas_ganadas_jugador += 1
                        monto += apuesta

                        print('>> Felicidades,', jugador, 'Ganaste!')

                        ult_mano_gano_crup = False

                    elif ganador == -1:  # Crupier
                        monto -= apuesta
                        print('>> Gana la casa!')
                        if mayor_perdida is None or mayor_perdida < apuesta:
                            mayor_perdida = apuesta

                        if ult_mano_gano_crup is None or not ult_mano_gano_crup:
                            racha_actual_crup = 1
                            ult_mano_gano_crup = True
                        elif ult_mano_gano_crup:
                            racha_actual_crup += 1

                        if racha_actual_crup > may_racha_crup:
                            may_racha_crup = racha_actual_crup

                    else:  # Empate
                        print('>> Hay un empate!')

                    print(">> Su nuevo pozo es de: $", monto)
                else:
                    print(">> Usted no tiene fondo para jugar, dirijase a la opción 1 para cargar más.")
                input("\n>> Presione ENTER para continuar")
        else:
            print("❌ ERROR! ❌: seleccione una opción entre 1  y 3")

        if monto > monto_maximo:
            monto_maximo = monto

    print("\n>> Su pozo final fue: $", monto)

    if partidas > 0:
        porcentaje_victorias = (partidas_ganadas_jugador * 100) / partidas
        promedio_apuestas = acc_apuestas / partidas

        print("\n>> Porcentaje de vicotrias del jugador: %", porcentaje_victorias, sep="")
        print(">> La racha de victorias mas larga del crupier:", may_racha_crup)
        print(">> Cantidad de manos donde hubo al menos un BJ natural:", cant_manos_bj_nat)
        print(">> Monto maximo del jugador: $", monto_maximo, sep="")
        print(">> Monto promedio que aposto el jugador: $", promedio_apuestas, sep="")
        if mayor_perdida:
            print(">> Perdida mas grande del jugador: $", mayor_perdida, sep="")
    else:
        print("\n>> No se jugo ninguna mano.")


programa()
