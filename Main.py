import cv2
from Rastreador import *
seguimiento = Rastreador()

#lectura del video

#esp 32 cam
cap = cv2.VideoCapture("http://192.168.15.181:81/stream")


#lectura con background
deteccion = cv2.createBackgroundSubtractorMOG2(history=10000, varThreshold=12)

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (500, 500))

    #Elegimos un corto
    zona = frame    # fila:fila , column:colum
    # mascara
    mascara = deteccion.apply(zona)
    _, mascara = cv2.threshold(mascara, 254, 255, cv2.THRESH_BINARY)
    contornos, _ = cv2.findContours(mascara, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detecciones = []

    for cont in contornos:
        area = cv2.contourArea(cont)
        if area > 450:
            x, y, ancho, alto = cv2.boundingRect(cont)
            cv2.rectangle(zona, (x, y), (x + ancho, y + alto), (255, 255, 0), 3)
            detecciones.append([x, y, ancho, alto])


    info_id = seguimiento.rastreo(detecciones)
    for inf in info_id:
        print(inf)
        x, y, ancho, alto, id = inf
        cv2.putText(zona, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,255),2)
        cv2.rectangle(zona, (x, y), (x + ancho, y + alto),(255, 255, 0), 3)

    print(info_id)
    cv2.imshow("Zona de intereses", zona)
    cv2.imshow("Carretera", frame)
    cv2.imshow("Mascara", mascara)

    key = cv2.waitKey(5)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
