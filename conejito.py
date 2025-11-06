import tkinter as tk
import threading
import time
import random

compliments = [
    "Eres increíble",
    "Tienes una sonrisa hermosa",
    "Eres muy talentosa",
    "Tu amabilidad es contagiosa",
    "Eres una persona muy especial",
    "Tienes un gran sentido del humor",
    "Eres muy inteligente",
    "Tu creatividad es impresionante",
    "Eres una gran amiga",
    "Tu energía positiva ilumina la habitación",
    "Tienes una risa que alegra el día",
    "Tu forma de ver la vida es inspiradora",
    "Siempre sabes cómo animar a los demás",
    "Eres una persona muy generosa",
    "Tienes una presencia que calma",
    "Tu honestidad es admirable",
    "Siempre das lo mejor de ti",
    "Eres un ejemplo a seguir",
    "Tienes un corazón enorme",
    "Tu pasión es inspiradora",
    "Eres muy resiliente",
    "Tu amabilidad no pasa desapercibida",
    "Eres una persona valiente",
    "Siempre encuentras el lado positivo de las cosas",
    "Tienes un alma hermosa",
    "Tu sentido de la justicia es admirable",
    "Eres una excelente oyente",
    "Siempre tienes las palabras justas",
    "Eres una persona confiable",
    "Tienes una paciencia infinita",
    "Tu dulzura es inigualable",
    "Eres muy perspicaz",
    "Tienes un don para hacer sentir bien a los demás",
    "Tu lealtad es incomparable",
    "Siempre das buenos consejos",
    "Eres una persona muy dedicada",
    "Tu entusiasmo es contagioso",
    "Eres un faro de luz en la oscuridad",
    "Tienes una mente brillante",
    "Eres muy comprensiva",
    "Tu optimismo es admirable",
    "Siempre encuentras soluciones creativas",
    "Eres un apoyo incondicional",
    "Tienes una intuición asombrosa",
    "Tu determinación es inspiradora",
    "Eres una persona muy trabajadora",
    "Siempre sabes cómo hacer reír",
    "Tienes un alma noble",
    "Tu bondad no conoce límites",
    "Eres muy valiosa para quienes te rodean",
    "Tienes una forma única de ver el mundo",
    "Tu sinceridad es refrescante",
    "Eres una fuerza de la naturaleza",
    "Siempre encuentras el equilibrio perfecto",
    "Eres la definición de perseverancia",
    "Tu calidez hace que todos se sientan bienvenidos",
    "Eres muy creativa e innovadora",
    "Siempre encuentras el lado bueno de las personas",
    "Tienes un talento natural para inspirar a otros",
    "Eres la alegría personificada",
    "Tu curiosidad es admirable",
    "Siempre estás dispuesta a ayudar",
    "Eres un tesoro para quienes te conocen",
    "Tienes una energía que motiva a todos",
    "Eres un ejemplo de humildad",
    "Siempre buscas aprender algo nuevo",
    "Eres muy empática",
    "Tu generosidad no tiene límites",
    "Eres una persona con un espíritu libre",
    "Siempre das el 100% en todo lo que haces",
    "Tienes una capacidad de adaptación increíble",
    "Tu fuerza interior es admirable",
    "Eres un pilar para los que te rodean",
    "Tu espíritu aventurero es inspirador",
    "Eres un remanso de paz",
    "Siempre encuentras una razón para sonreír",
    "Tienes una habilidad natural para liderar",
    "Eres una persona que deja huella",
    "Tu pasión por la vida es contagiosa",
    "Siempre sabes cómo sorprender",
    "Eres una chispa de alegría",
    "Tu bondad transforma el mundo",
    "Eres una persona llena de sabiduría",
    "Tu ternura es conmovedora",
    "Siempre aportas una perspectiva valiosa",
    "Eres una persona que inspira confianza",
    "Tienes una fuerza de voluntad impresionante",
    "Tu espíritu luchador es admirable",
    "Eres una persona con un corazón de oro",
    "Siempre enfrentas los desafíos con valentía",
    "Tienes un aura de paz",
    "Eres un rayo de sol en días grises",
    "Tu determinación mueve montañas",
    "Siempre buscas el bien común",
    "Eres un ejemplo de empatía",
    "Tu presencia llena de calma a los demás",
    "Eres una inspiración diaria",
    "Siempre dejas una marca positiva",
    "Eres una persona increíblemente amable",
    "Tu forma de amar la vida es inspiradora",
    "Eres una joya única en el mundo",
    "Tienes una magia que nadie puede replicar",
    "Tu autenticidad es admirable",
    "Eres la personificación de la alegría",
    "Siempre ves el vaso medio lleno"
]



def show_message():
    root = tk.Tk()
    root.title("Buenas buenas")
    compliment = random.choice(compliments)
    label = tk.Label(root, text=f"Para que no se te olvide, {compliment}")
    label.pack(padx=20, pady=20)
    root.after(1000, lambda: root.attributes('-topmost', False))  # Remove topmost attribute after 1 second
    root.mainloop()

def create_windows():
    for _ in range(60):
        threading.Thread(target=show_message).start()
        time.sleep(1)

if __name__ == "__main__":
    create_windows()