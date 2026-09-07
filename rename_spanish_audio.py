"""
Copy the Spanish TTS audio files (auto-named/truncated by the TTS tool) into
forklift-evaluation/audio/ with names matching the form's field IDs
(q1_es.<ext> ... q35_es.<ext>).

The source filenames were truncated to a fixed 20 characters by whatever
tool exported them, e.g. "1. Cu......llas..wav" or "[emph......ante..wav".
Most start with "<item number>. " (matches the script's item number
directly); 13 of them instead start with a bracketed tag like "[emphasis]"
or "[short pause]" — presumably added ad hoc before the text was pasted
into the TTS tool — so those are matched by the last few characters of the
filename against the known ending of each item's Spanish script text
instead.

This only COPIES files (originals in Downloads are left untouched) so it's
safe to re-run or inspect before doing anything with the originals.
"""

import os
import re
import shutil

SRC_DIR = r"C:\Users\cmaxi\Downloads\Spanish Audio files FLE"
DEST_DIR = r"C:\Users\cmaxi\CLaude_local\forklift-evaluation\audio"

# Full Spanish script text per item (same content as audio-script.md / the
# Spanish PDF) — used only to derive each item's expected ending, to match
# against the bracket-tagged files that don't carry the item number.
SPANISH_TEXT = {
    1: "Cuadre el montacargas en el centro de la carga. Coloque el montacargas directamente frente a la carga, con las horquillas centradas, para que el peso quede distribuido de manera uniforme entre ambas horquillas.",
    2: "Nivele las horquillas; luego avance lentamente hasta que la carga haga contacto con el carro portahorquillas. Nivele las horquillas con el suelo, luego avance lentamente y de manera constante hasta que la carga quede firmemente apoyada contra el carro portahorquillas.",
    3: "Levante la carga con cuidado y suavidad hasta que quede libre del suelo. Levante la carga de forma lenta y uniforme, solo lo necesario para que quede libre del suelo o de la pila debajo de ella, evitando movimientos bruscos.",
    4: "Incline el mástil ligeramente hacia atrás para estabilizar la carga. Incline el mástil hacia atrás unos pocos grados para que la carga descanse de forma segura contra el respaldo y no se deslice hacia adelante fuera de las horquillas.",
    5: "Mire sobre ambos hombros. Antes de moverse, mire sobre ambos hombros para verificar que no haya personas, obstáculos u otro equipo en su camino.",
    6: "Una vez fuera y detenido, baje la carga a la altura de traslado. Una vez que esté libre del estante o pila y detenido, baje la carga a una altura segura de traslado, aproximadamente diez a quince centímetros del suelo.",
    7: "No suba ni baje la carga ni las horquillas mientras se desplaza. Mantenga las horquillas a una altura fija mientras el montacargas está en movimiento. Suba o baje la carga solo cuando esté detenido.",
    8: "Mantenga una velocidad segura. Circule a una velocidad que le permita detenerse de forma segura según las condiciones, la carga y el entorno. Nunca se apresure.",
    9: "Respete todas las normas de tránsito, señales de advertencia, límites de carga del piso y alturas libres superiores. Respete en todo momento los patrones de tránsito señalados, las señales de advertencia, los límites de peso del piso y las alturas libres superiores.",
    10: "Mantenga los brazos y las piernas dentro del montacargas. Mantenga siempre los brazos, las piernas y la cabeza completamente dentro de la cabina del operador mientras conduce.",
    11: "Siga a otros vehículos a una distancia segura. Deje suficiente espacio detrás de otros vehículos, aproximadamente tres largos de camión, para poder detenerse de forma segura si se detienen repentinamente.",
    12: "Reduzca la velocidad al tomar curvas. Reduzca la velocidad antes de girar para evitar que el montacargas vuelque o que se pierda el control de la carga.",
    13: "Use la bocina para alertar a los demás. Toque la bocina en intersecciones, esquinas ciegas y puertas para advertir a los peatones y a otros operadores de su presencia.",
    14: "Desplácese con la carga orientada hacia la subida en rampas o pendientes. En rampas o pendientes, mantenga la carga orientada hacia la subida. Conduzca hacia adelante al subir y en reversa al bajar, para que la carga no se deslice.",
    15: "Deténgase suavemente. Detenga el montacargas de forma gradual y controlada, en lugar de frenar bruscamente, para mantener la carga estable.",
    16: "Asegúrese de que haya suficiente espacio libre para la carga. Antes de colocar la carga, confirme que haya suficiente espacio libre por arriba y a los lados para que quepa sin golpear nada.",
    17: "Despeje al personal del área cercana a la carga. Asegúrese de que nadie esté parado cerca del área de colocación o debajo de la carga antes de bajarla.",
    18: "Cuadre el montacargas con el lugar; luego deténgase a aproximadamente 30 centímetros de distancia. Alinee el montacargas directamente con el lugar de almacenamiento, luego deténgase con la carga a unos treinta centímetros de distancia antes de hacer los ajustes finales.",
    19: "Eleve la carga hasta el nivel de colocación. Eleve la carga hasta la altura exacta del estante o pila donde será colocada.",
    20: "Avance lentamente hacia adelante. Avance con el montacargas lentamente y de manera constante hasta que la carga quede completamente posicionada en su lugar.",
    21: "Si la carga está sobre una tarima, bájela hasta su posición y baje las horquillas un poco más. Baje la tarima suavemente hasta su posición final, luego continúe bajando las horquillas un poco más para que queden libres de las aberturas de la tarima.",
    22: "Mire sobre ambos hombros antes de retroceder. Vuelva a mirar sobre ambos hombros para confirmar que el camino esté despejado antes de retroceder alejándose de la carga.",
    23: "Retroceda en línea recta hasta que las horquillas queden libres. Retroceda en línea recta hasta que las horquillas queden completamente libres de la carga y del estante.",
    24: "Baje las horquillas a la posición de traslado. Después de retroceder y quedar libre, baje las horquillas a la altura estándar de traslado, aproximadamente diez a quince centímetros del suelo.",
    25: "Baje las horquillas completamente. Una vez estacionado, baje las horquillas completamente hasta el suelo para que no representen un riesgo de tropiezo.",
    26: "Coloque los controles en neutral. Coloque el control de dirección y cualquier otra palanca en neutral antes de dejar el asiento.",
    27: "Aplique los frenos. Aplique completamente el freno de estacionamiento antes de bajarse para evitar que el montacargas se desplace.",
    28: "Apague la energía. Gire la llave a la posición de apagado, o apague el motor eléctrico, una vez estacionado.",
    29: "Si estaciona en una pendiente, bloquee las ruedas. Si debe estacionar en una pendiente, coloque calzas en las ruedas para evitar que el montacargas ruede.",
    30: "Estacione únicamente en áreas autorizadas. Estacione el montacargas únicamente en las áreas designadas para ello. Nunca en pasillos, frente a salidas o bloqueando otro equipo.",
    31: "Motor apagado. Confirme que el motor esté completamente apagado antes de alejarse del montacargas.",
    32: "Extintor de incendios cerca. Verifique que haya un extintor de incendios en funcionamiento montado en el montacargas o disponible cerca de él.",
    33: "Equipo de protección personal adecuado en uso. Confirme que el operador esté utilizando todo el equipo de protección personal requerido, como casco, chaleco de seguridad y botas con punta de acero.",
    34: "Se siguen los procedimientos seguros de reabastecimiento de combustible y recarga de batería. Confirme que el reabastecimiento de combustible o la recarga de batería se realice en un área designada y ventilada, siguiendo los procedimientos de seguridad adecuados.",
    35: "Los derrames se limpian de inmediato. Confirme que cualquier derrame de combustible, aceite o líquido hidráulico se limpie de inmediato para evitar resbalones y riesgos de incendio.",
}


def normalize_ending(text, length=4):
    """Last `length` alphanumeric-ish characters, lowercased, punctuation stripped."""
    cleaned = re.sub(r"[.\s]+$", "", text.strip())
    return cleaned[-length:].lower()


os.makedirs(DEST_DIR, exist_ok=True)

files = os.listdir(SRC_DIR)
matched = {}   # item number -> source filename
unmatched = []

# Pass 1: numbered files ("N. ...")
for f in files:
    m = re.match(r"^(\d+)\.\s", f)
    if m:
        num = int(m.group(1))
        matched[num] = f

# Pass 2: bracket-tagged files, matched by ending
remaining_items = [n for n in SPANISH_TEXT if n not in matched]
ending_lookup = {normalize_ending(SPANISH_TEXT[n]): n for n in remaining_items}

for f in files:
    if re.match(r"^\d+\.\s", f):
        continue
    base, ext = os.path.splitext(f)
    file_ending = normalize_ending(base, 4)
    if file_ending in ending_lookup:
        matched[ending_lookup[file_ending]] = f
    else:
        unmatched.append(f)

print(f"Matched {len(matched)} of 35 items.")
if unmatched:
    print("Could not match:", unmatched)
missing = sorted(set(SPANISH_TEXT) - set(matched))
if missing:
    print("No file found for items:", missing)

for num, fname in sorted(matched.items()):
    src_path = os.path.join(SRC_DIR, fname)
    ext = os.path.splitext(fname)[1]
    dest_name = f"q{num}_es{ext}"
    dest_path = os.path.join(DEST_DIR, dest_name)
    shutil.copy2(src_path, dest_path)
    print(f"q{num:>2} <- {fname}  ({ext})")
