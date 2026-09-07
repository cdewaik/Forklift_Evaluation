"""Generate English and Spanish audio-script PDFs for the forklift evaluation form."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

NAVY = "#122150"
ROYAL = "#2540bf"
MUTED = "#5a6479"

SECTIONS = [
    ("Picking Up a Load", "Recogiendo una Carga", [
        (1,
         "Square up on the center of the load. Position the forklift squarely in front of the load, forks centered, so the weight is balanced evenly across both forks.",
         "Cuadre el montacargas en el centro de la carga. Coloque el montacargas directamente frente a la carga, con las horquillas centradas, para que el peso quede distribuido de manera uniforme entre ambas horquillas."),
        (2,
         "Level the forks; then slowly drive forward until the load contacts the carriage. Tilt the forks level with the ground, then drive forward slowly and steadily until the load rests firmly against the fork carriage.",
         "Nivele las horquillas; luego avance lentamente hasta que la carga haga contacto con el carro portahorquillas. Nivele las horquillas con el suelo, luego avance lentamente y de manera constante hasta que la carga quede firmemente apoyada contra el carro portahorquillas."),
        (3,
         "Lift the load carefully and smoothly until it is clear. Raise the load slowly and smoothly, just high enough to clear the ground or the stack beneath it, avoiding sudden or jerky movements.",
         "Levante la carga con cuidado y suavidad hasta que quede libre del suelo. Levante la carga de forma lenta y uniforme, solo lo necesario para que quede libre del suelo o de la pila debajo de ella, evitando movimientos bruscos."),
        (4,
         "Tilt the mast back slightly to stabilize the load. Tilt the mast back a few degrees so the load rests securely against the backrest and won't slide forward off the forks.",
         "Incline el mástil ligeramente hacia atrás para estabilizar la carga. Incline el mástil hacia atrás unos pocos grados para que la carga descanse de forma segura contra el respaldo y no se deslice hacia adelante fuera de las horquillas."),
        (5,
         "Look over both shoulders. Before moving, check over both shoulders for people, obstacles, or other equipment in your path.",
         "Mire sobre ambos hombros. Antes de moverse, mire sobre ambos hombros para verificar que no haya personas, obstáculos u otro equipo en su camino."),
    ]),
    ("Traveling", "Desplazamiento", [
        (6,
         "After out and stopped, lower the load to travel height. Once clear of the rack or stack and stopped, lower the load to a safe travel height, about four to six inches off the ground.",
         "Una vez fuera y detenido, baje la carga a la altura de traslado. Una vez que esté libre del estante o pila y detenido, baje la carga a una altura segura de traslado, aproximadamente diez a quince centímetros del suelo."),
        (7,
         "Do not raise or lower the load and forks while traveling. Keep the forks at a fixed height while the forklift is moving. Raise or lower the load only when stopped.",
         "No suba ni baje la carga ni las horquillas mientras se desplaza. Mantenga las horquillas a una altura fija mientras el montacargas está en movimiento. Suba o baje la carga solo cuando esté detenido."),
        (8,
         "Maintain a safe speed. Travel at a speed that allows you to stop safely for the conditions, the load, and your surroundings. Never rush.",
         "Mantenga una velocidad segura. Circule a una velocidad que le permita detenerse de forma segura según las condiciones, la carga y el entorno. Nunca se apresure."),
        (9,
         "Observe all traffic rules, warning signs, floor load limits and overhead clearances. Follow posted traffic patterns, warning signs, floor weight limits, and overhead clearance markings at all times.",
         "Respete todas las normas de tránsito, señales de advertencia, límites de carga del piso y alturas libres superiores. Respete en todo momento los patrones de tránsito señalados, las señales de advertencia, los límites de peso del piso y las alturas libres superiores."),
        (10,
         "Keep arms and legs inside the forklift. Keep your arms, legs, and head fully inside the operator compartment at all times while driving.",
         "Mantenga los brazos y las piernas dentro del montacargas. Mantenga siempre los brazos, las piernas y la cabeza completamente dentro de la cabina del operador mientras conduce."),
        (11,
         "Follow other vehicles at safe distance. Leave enough space behind other vehicles, about three truck lengths, so you can stop safely if they stop suddenly.",
         "Siga a otros vehículos a una distancia segura. Deje suficiente espacio detrás de otros vehículos, aproximadamente tres largos de camión, para poder detenerse de forma segura si se detienen repentinamente."),
        (12,
         "Slow down when cornering. Reduce your speed before turning to avoid tipping the forklift or losing control of the load.",
         "Reduzca la velocidad al tomar curvas. Reduzca la velocidad antes de girar para evitar que el montacargas vuelque o que se pierda el control de la carga."),
        (13,
         "Use the horn to alert others. Sound the horn at intersections, blind corners, and doorways to warn pedestrians and other operators that you're approaching.",
         "Use la bocina para alertar a los demás. Toque la bocina en intersecciones, esquinas ciegas y puertas para advertir a los peatones y a otros operadores de su presencia."),
        (14,
         "Travel with the load facing uphill while on a ramp or incline. On ramps or inclines, keep the load pointed uphill. Drive forward going up and in reverse going down, so the load can't slide off.",
         "Desplácese con la carga orientada hacia la subida en rampas o pendientes. En rampas o pendientes, mantenga la carga orientada hacia la subida. Conduzca hacia adelante al subir y en reversa al bajar, para que la carga no se deslice."),
    ]),
    ("Placing the Load", "Colocando la Carga", [
        (15,
         "Stop smoothly. Bring the forklift to a gradual, controlled stop rather than braking abruptly, to keep the load stable.",
         "Deténgase suavemente. Detenga el montacargas de forma gradual y controlada, en lugar de frenar bruscamente, para mantener la carga estable."),
        (16,
         "Make sure there is sufficient clearance for the load. Before placing the load, confirm there's enough overhead and side clearance for it to fit without hitting anything.",
         "Asegúrese de que haya suficiente espacio libre para la carga. Antes de colocar la carga, confirme que haya suficiente espacio libre por arriba y a los lados para que quepa sin golpear nada."),
        (17,
         "Clear personnel from the area near the load. Make sure no one is standing near the placement area or under the load before setting it down.",
         "Despeje al personal del área cercana a la carga. Asegúrese de que nadie esté parado cerca del área de colocación o debajo de la carga antes de bajarla."),
        (18,
         "Square up to the location; then stop about one foot away. Align the forklift squarely with the storage location, then stop with the load about one foot away before making final adjustments.",
         "Cuadre el montacargas con el lugar; luego deténgase a aproximadamente 30 centímetros de distancia. Alinee el montacargas directamente con el lugar de almacenamiento, luego deténgase con la carga a unos treinta centímetros de distancia antes de hacer los ajustes finales."),
        (19,
         "Raise the load to placement level. Raise the load to the exact height of the shelf or stack where it will be placed.",
         "Eleve la carga hasta el nivel de colocación. Eleve la carga hasta la altura exacta del estante o pila donde será colocada."),
        (20,
         "Move slowly forward. Ease the forklift forward slowly and steadily until the load is fully positioned in place.",
         "Avance lentamente hacia adelante. Avance con el montacargas lentamente y de manera constante hasta que la carga quede completamente posicionada en su lugar."),
        (21,
         "If the load is on a pallet, lower it into position and lower the forks further. Lower the pallet gently into its final position, then continue lowering the forks slightly further so they clear the pallet openings.",
         "Si la carga está sobre una tarima, bájela hasta su posición y baje las horquillas un poco más. Baje la tarima suavemente hasta su posición final, luego continúe bajando las horquillas un poco más para que queden libres de las aberturas de la tarima."),
        (22,
         "Look over both shoulders before backing out. Check over both shoulders again to confirm the path is clear before reversing away from the load.",
         "Mire sobre ambos hombros antes de retroceder. Vuelva a mirar sobre ambos hombros para confirmar que el camino esté despejado antes de retroceder alejándose de la carga."),
        (23,
         "Back straight out until the forks have cleared. Reverse in a straight line until the forks are completely clear of the load and the rack.",
         "Retroceda en línea recta hasta que las horquillas queden libres. Retroceda en línea recta hasta que las horquillas queden completamente libres de la carga y del estante."),
    ]),
    ("Dismounting & Parking", "Desmontaje y Estacionamiento", [
        (24,
         "Lower the forks to traveling position. After backing clear, lower the forks to the standard travel height, about four to six inches off the ground.",
         "Baje las horquillas a la posición de traslado. Después de retroceder y quedar libre, baje las horquillas a la altura estándar de traslado, aproximadamente diez a quince centímetros del suelo."),
        (25,
         "Fully lower the forks. Once parked, lower the forks all the way to the ground so they don't create a tripping or safety hazard.",
         "Baje las horquillas completamente. Una vez estacionado, baje las horquillas completamente hasta el suelo para que no representen un riesgo de tropiezo."),
        (26,
         "Neutralize the controls. Shift the direction control and any other levers to neutral before leaving the seat.",
         "Coloque los controles en neutral. Coloque el control de dirección y cualquier otra palanca en neutral antes de dejar el asiento."),
        (27,
         "Set the brakes. Engage the parking brake fully before dismounting so the forklift can't roll.",
         "Aplique los frenos. Aplique completamente el freno de estacionamiento antes de bajarse para evitar que el montacargas se desplace."),
        (28,
         "Turn off the power. Turn the key to the off position, or shut down the electric motor, once parked.",
         "Apague la energía. Gire la llave a la posición de apagado, o apague el motor eléctrico, una vez estacionado."),
        (29,
         "If parked on an incline, block the wheels. If you must park on a slope, place wheel chocks against the wheels to keep the forklift from rolling.",
         "Si estaciona en una pendiente, bloquee las ruedas. Si debe estacionar en una pendiente, coloque calzas en las ruedas para evitar que el montacargas ruede."),
        (30,
         "Park only in authorized areas. Park the forklift only in designated parking areas. Never in aisles, in front of exits, or blocking other equipment.",
         "Estacione únicamente en áreas autorizadas. Estacione el montacargas únicamente en las áreas designadas para ello. Nunca en pasillos, frente a salidas o bloqueando otro equipo."),
    ]),
    ("Safety & Housekeeping", "Seguridad y Orden", [
        (31,
         "Engine off. Confirm the engine or motor is completely off before walking away from the forklift.",
         "Motor apagado. Confirme que el motor esté completamente apagado antes de alejarse del montacargas."),
        (32,
         "Fire extinguisher nearby. Verify a working fire extinguisher is mounted on the forklift or readily available nearby.",
         "Extintor de incendios cerca. Verifique que haya un extintor de incendios en funcionamiento montado en el montacargas o disponible cerca de él."),
        (33,
         "Proper personal protective equipment worn. Confirm the operator is wearing all required personal protective equipment, such as a hard hat, safety vest, and steel-toed boots.",
         "Equipo de protección personal adecuado en uso. Confirme que el operador esté utilizando todo el equipo de protección personal requerido, como casco, chaleco de seguridad y botas con punta de acero."),
        (34,
         "Safe fueling and battery recharging procedures followed. Confirm that fueling or battery charging is done in a designated, ventilated area, following proper safety procedures.",
         "Se siguen los procedimientos seguros de reabastecimiento de combustible y recarga de batería. Confirme que el reabastecimiento de combustible o la recarga de batería se realice en un área designada y ventilada, siguiendo los procedimientos de seguridad adecuados."),
        (35,
         "Spills cleaned up immediately. Confirm that any fuel, oil, or hydraulic fluid spills are cleaned up right away to prevent slips and fire hazards.",
         "Los derrames se limpian de inmediato. Confirme que cualquier derrame de combustible, aceite o líquido hidráulico se limpie de inmediato para evitar resbalones y riesgos de incendio."),
    ]),
]

RATINGS_EN = ("For each item, rate the operator GOOD if the step was performed correctly, FAIR if it was "
              "performed but needs improvement, POOR if it was not performed safely or was skipped, or N/A "
              "if the step didn't apply to this evaluation.")
RATINGS_ES = ("Para cada punto, califique al operador como BUENO si el paso se realizó correctamente, REGULAR "
              "si se realizó pero necesita mejorar, DEFICIENTE si no se realizó de forma segura o se omitió, "
              "o NO APLICA si el paso no correspondía a esta evaluación.")


def build_pdf(filename, lang_title, section_title_index, text_index, ratings_text):
    doc = SimpleDocTemplate(
        filename, pagesize=letter,
        topMargin=0.75 * inch, bottomMargin=0.75 * inch,
        leftMargin=0.85 * inch, rightMargin=0.85 * inch,
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleCustom", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=18, textColor=NAVY, spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        "SubtitleCustom", parent=styles["Normal"], fontName="Helvetica",
        fontSize=10, textColor=MUTED, spaceAfter=20,
    )
    section_style = ParagraphStyle(
        "SectionCustom", parent=styles["Heading2"], fontName="Helvetica-Bold",
        fontSize=13, textColor=ROYAL, spaceBefore=18, spaceAfter=8,
    )
    item_style = ParagraphStyle(
        "ItemCustom", parent=styles["Normal"], fontName="Helvetica",
        fontSize=10.5, leading=15, spaceAfter=12, alignment=TA_LEFT,
    )
    num_style = ParagraphStyle(
        "NumCustom", parent=item_style, fontName="Helvetica-Bold", textColor=ROYAL,
    )

    story = [
        Paragraph("Forklift Operator Evaluation", title_style),
        Paragraph(lang_title, subtitle_style),
    ]

    for section in SECTIONS:
        story.append(Paragraph(section[section_title_index], section_style))
        for item in section[2]:
            num, text = item[0], item[text_index]
            story.append(Paragraph(f"<b>{num}.</b> {text}", item_style))

    story.append(Paragraph("Rating Scale" if text_index == 1 else "Escala de Calificación", section_style))
    story.append(Paragraph(ratings_text, item_style))

    doc.build(story)


build_pdf(
    "audio-script-english.pdf",
    "Audio Narration Script — English",
    section_title_index=0, text_index=1, ratings_text=RATINGS_EN,
)

build_pdf(
    "audio-script-spanish.pdf",
    "Guion de Narración de Audio — Español",
    section_title_index=1, text_index=2, ratings_text=RATINGS_ES,
)

print("Done.")
