from telegram import Poll
from telegram.ext import (
    Updater,
    CommandHandler,
    PollHandler,
)
import random
import telegram
import time


class Question:

    def __init__(self, text, list_answers, correct_answers):
        self.text = text
        self.list_answers = list_answers
        self.correct_answers = correct_answers


actual_question = 0
max_question = 6
respuestas_correctas = 0
random_question = Question('', '', '')
lista_Preguntas = [Question('¿Cuál de las siguientes alternativas está asociado a lo que es un Repositorio de Código?',
                            ['Lugar donde se almacena y distribuye el código de una aplicación',
                             'Suele contener diverso tipo de metadatos que acompañan al código',
                             'Lugar para trabajar de manera asincrónica e individual'],
                            ['Lugar donde se almacena y distribuye el código de una aplicación',
                             'Suele contener diverso tipo de metadatos que acompañan al código']),

                   Question('¿Qué es un hotspot?',
                            ['Sección del código el cuál no es tan importante',
                             'Sección de interés del código donde se requiere más esfuerzo',
                             'Sección del código que trabajará una sola persona'],
                            ['Sección de interés del código donde se requiere más esfuerzo']),

                   Question('¿Cuál de las siguientes sentencias describe un repositorio Git?',
                            ['Base de datos donde se almacena los archivos de un proyecto',
                             'Provee una copia de todos los archivos y una copia del repositorio en sí',
                             'Base de datos con todo lo necesario para manejar la historia de un proyecto'],
                            ['Provee una copia de todos los archivos y una copia del repositorio en sí',
                             'Base de datos con todo lo necesario para manejar la historia de un proyecto']),

                   Question('¿Cuál de las siguientes alternativas corresponden a estructuras de un repositorio Git?',
                            ['Blobs, trees, commits, tags, index',
                             'Archivos, carpetas, ficheros .exe',
                             'Bits, SHA-1'],
                            ['Blobs, trees, commits, tags, index']),

                   Question('¿Cuál de las siguientes alternativas describe un beneficio para usar una rama (tree)?',
                            ['Se puede usar para mostrar una versión del proyecton',
                             'Siempre una rama representa el trabajo de una persona',
                             'Encapsula una fase de desarrollo (prototipo, alfa, beta, estable, etc)'],
                            ['Encapsula una fase de desarrollo (prototipo, alfa, beta, estable, etc)']),

                   Question('¿Cuándo se usa el algoritmo Fast-forward para fusionar ramas?',
                            ['Se utiliza cuando hay un desarrollo lineal entre las ramas que se quieren fusionar',
                             'Se utiliza cuando no hay un desarrollo lineal entre las ramas',
                             'Se utiliza en cualquier contexto'],
                            ['Se utiliza cuando hay un desarrollo lineal entre las ramas que se quieren fusionar']),

                   Question('¿Por qué modificar commits?',
                            ['Desagrupar un gran cambio en una serie de cambios pequeños',
                             'Para que se vea estéticamente mejor el historial',
                             'Para agregar código adicional al proyecto'],
                            ['Desagrupar un gran cambio en una serie de cambios pequeños']),

                   Question('¿Qué describe a un repositorio clon?',
                            ['Contiene todos los objetos del original, es independiente y permite el trabajo local',
                             'Es una copia idéntica de otro repositorio',
                             'Es un repositorio el cual se actualiza automáticamente con el repositorio original creado'],
                            ['Contiene todos los objetos del original, es independiente y permite el trabajo local']),

                   Question('¿Qué beneficio nos otorga el seguimiento de tareas ?',
                            ['Permite visualizar más fácilmente los asuntos del proyecto',
                             'Permiten organizar, filtrar y manejar eficientemente asuntos del proyecto (issues).',
                             'Permite llevar un conteo de los asuntos del proyecto'],
                            ['Permiten organizar, filtrar y manejar eficientemente asuntos del proyecto (issues).']),

                   Question('¿Qué utilidad tiene la herramienta Git hook?',
                            ['Herramienta de Git, que permite visualizar tareas',
                             'Herramienta de Git, que permite el seguimiento de tareas',
                             'Herramienta de Git, que permite la automatización de tareas'],
                            ['Herramienta de Git, que permite la automatización de tareas']),

                   Question('¿Qué es la integración continua?',
                            ['Permite que desarrolladores suban/fusionen cambios del código en una misma rama de forma frecuente',
                             'Es una práctica para que los desarrolladores trabajen en una misma rama al mismo tiempo',
                             'Permite que los desarrolladores trabajen de manera integra dentro de las carpetas del proyecto'],
                            ['Permite que desarrolladores suban/fusionen cambios del código en una misma rama de forma frecuente']),

                   Question('¿Qué son los GitHub Actions?',
                            ['Son herramientas para clonar y manejar repositorios',
                             'Son herramientas para fusionar trabajar y fusionar ramas',
                             'Son herramientas para automatizar, personalizar y ejecutar flujos en desarrollo de software'],
                            ['Son herramientas para automatizar, personalizar y ejecutar flujos en desarrollo de software']),
                   ]


def add_typing(update, context):
    context.bot.send_chat_action(
        chat_id=get_chat_id(update, context),
        action=telegram.ChatAction.TYPING,
        timeout=1,
    )
    time.sleep(1)


def poll_handler(update, context):
    global respuestas_correctas

    add_typing(update, context)
    answers = update.poll.options

    answers_correct = random_question.correct_answers
    counter = 0
    count_answers = 0
    for answer in answers:
        if answer.voter_count == 1:
            count_answers += 1
            if answer.text in answers_correct:
                counter = counter + 1

    texto = ''

    if counter == len(answers_correct) and count_answers == len(answers_correct):

        texto = 'Respuesta(s) Correcta(s)'
        respuestas_correctas += 1

    else:

        texto = 'Respuesta(s) Incorrecta(s)'

    context.bot.send_message(chat_id=get_chat_id(update, context),
                             text=f"{texto}")

    question(update, context)


def get_chat_id(update, context):
    chat_id = -1
    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        chat_id = context.bot_data[update.poll.id]

    return chat_id


def question(update, context):
    global random_question, actual_question, max_question

    if actual_question < max_question:

        random_question = random.choice(lista_Preguntas)
        message = context.bot.send_poll(chat_id=get_chat_id(update, context),
                                        question=random_question.text,
                                        options=random_question.list_answers,
                                        type=Poll.REGULAR,
                                        allows_multiple_answers=True,
                                        is_anonymous=True)

        context.bot_data.update({message.poll.id: message.chat.id})

        actual_question += 1

    else:

        add_typing(update, context)
        context.bot.send_message(chat_id=get_chat_id(update, context),
                                 text=f"Total de preguntas: {max_question}\n"
                                      f"Preguntas Correctas: {respuestas_correctas}\n"
                                      f"Tu nota es: {respuestas_correctas + 1}")


def start_commander(update, context):
    c_id = get_chat_id(update, context)
    question(update, context)


def main():
    updater = Updater('2116134001:AAHl_y9JAdFs0-SKuzVZICONmJ-BHpZjZvI', use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_commander))

    dp.add_handler(PollHandler(poll_handler, pass_chat_data=True, pass_user_data=True))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
