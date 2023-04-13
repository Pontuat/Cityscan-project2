import math


class Rastreador:

    def __init__(self):
        #posición central
       self.centro_puntos = {}

       self.id_count = 1

    def rastreo(self, objetos):
        #objetos identificados
        objetos_id = []

        for rect in objetos:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            #ya fue detectado
            objeto_det = False
            for id, pt in self.centro_puntos.items():
                dist = math.hypot(cx - pt[0], cy - pt [1])

                if dist < 25:
                    self.centro_puntos[id] = (cx, cy)
                    print(self.centro_puntos)
                    objetos_id.append([x, y, w, h, id])
                    objeto_det = True
                    break

            if objeto_det is False:
                self.centro_puntos[self.id_count] = (cx,cy)
                objetos_id.append([x, y, h, w, self.id_count])
                self.id_count = self.id_count + 1 #aumentas


        new_center_points = {}
        for obj_bb_id in objetos_id:
            print(obj_bb_id)
            _, _, _, _, object_id = obj_bb_id
            center = self.centro_puntos[object_id]
            new_center_points[object_id] = center

        self.centro_puntos = new_center_points
        return objetos_id
