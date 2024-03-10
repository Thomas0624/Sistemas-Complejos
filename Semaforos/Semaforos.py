import tkinter as tk
import random
import threading
import time

class Vehicle:
    def __init__(self, canvas, x, y, width, height, direction):
        self.canvas = canvas
        self.direction = direction
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.shape = None
        self.draw()

    def draw(self):
        if self.direction == "horizontal":
            self.shape = self.canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill="yellow")
        else:
            self.shape = self.canvas.create_rectangle(self.x, self.y, self.x + self.height, self.y + self.width, fill="blue")

    def move(self, x, y):
        self.canvas.move(self.shape, x, y)
        self.x += x
        self.y += y

class Semaforo:
    def __init__(self, canvas, x, y, radius, initial_color, direccion):
        self.vehiculos_cerca = 0
        self.contador=0
        self.direccion = direccion
    
        self.canvas = canvas
        self.x = x
        self.y = y
        self.radius = radius
        self.color = initial_color
        self.shape = self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=initial_color)

    def change_colores(self, new_color):
        self.color = new_color
        self.canvas.itemconfig(self.shape, fill=new_color)

    def is_green(self):
        return self.color == "green"

    def is_red(self):
        return self.color == "red"


class SemaphorSimulation:
    def __init__(self, master):
        
        
        self.master = master
        self.bandera_vertical = 10
        self.bandera_horizontal = 10

        self.contadorSemaforos = 0

        self.cont1=0
        self.cont2=0
        
        self.extra = False
        self.nn=False

        self.distancia_d =50
        self.corta_distancia_r = 3
        self.corta_distancia_e = 10
        self.umbral_n = 7

        self.vehicles_horizontal = []
        self.vehicles_vertical = []
                
        self.canvas = tk.Canvas(root, width=780, height=300, bg="black")  # Fondo negro
        self.canvas.pack()

        # Vincular el evento de clic del ratón al método on_canvas_click
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.semaforos = [
            Semaforo(self.canvas, 210, 60, 15, "red", "horizontal"),
            Semaforo(self.canvas, 250, 80, 15, "red", "vertical"),
            Semaforo(self.canvas, 510, 60, 15, "red", "horizontal"),
            Semaforo(self.canvas, 550, 80, 15, "red", "vertical")
        ]

        # Crear semáforos en el lienzo
        #self.semaforo_derecha = self.canvas.create_oval(210 - self.radius, 60 - self.radius, 210 + self.radius, 60+ self.radius, fill="red")
        #self.semaforo_arriba = self.canvas.create_oval(250 - self.radius, 80 - self.radius, 250 + self.radius, 80 + self.radius, fill="green")
        #self.semaforo_derecha1 = self.canvas.create_oval(510 - self.radius, 60 - self.radius, 510 + self.radius, 60+ self.radius, fill="red")
        #self.semaforo_arriba1 = self.canvas.create_oval(550 - self.radius, 80 - self.radius, 550 + self.radius, 80 + self.radius, fill="green")

        # Crear hilos para la simulación
        self.semaphore_thread = threading.Thread(target=self.run_semaphore)
        self.vehicle_thread = threading.Thread(target=self.run_vehicles)

        # Iniciar los hilos
        self.semaphore_thread.start()
        self.vehicle_thread.start()
        inicializarCruces(self.canvas)
    
    def on_canvas_click(self, event):
        x = event.x
        y = event.y

    def run_semaphore(self):
        while True:
            self.contadorSemaforos =0

            # CADA QUE CAMBIA EL SEMAFORO DEBO CAMBIAR  semaforo.vehiculos_cerca = 0

            #CONDICIONES:
            
            # Recorre la lista de semáforos
            for semaforo in self.semaforos:
                # 1. En cada paso de tiempo, agregar a un contador el número de vehículos que
                # se acercan o esperan ante una luz roja a una distancia d. Cuando este contador exceda 
                #un umbral_n, cambiar el semáforo (Siempre que el semáforo cambia reiniciar el contador a 0)
                if semaforo.is_red():
                    if(semaforo.direccion=="horizontal"):
                        # Recorre la lista de vehiculos horizontal
                        if(self.vehicles_horizontal!=None):  
                            for vehicle in self.vehicles_horizontal:
                                if (semaforo.x > vehicle.x >= (semaforo.x -self.distancia_d)):
                                    semaforo.vehiculos_cerca +=1
                            
                                if(semaforo.vehiculos_cerca > self.umbral_n):
                                    semaforo.vehiculos_cerca = 0
                                    #                  SEMAFORO, POSICIÓN SEMAFORO, HORIZONTAL, VERTICAL
                                    self.change_color(self.contadorSemaforos,"green","red")
                                    self.extra = True
                                    
                            
                    else:
                        # Recorre la lista de vehiculos vertical
                        if(self.vehicles_vertical!=None):  
                            for vehicle in self.vehicles_vertical:
                                if (semaforo.y < vehicle.y <=(semaforo.y + self.distancia_d)):
                                    semaforo.vehiculos_cerca +=1

                                if(semaforo.vehiculos_cerca > self.umbral_n):
                                    semaforo.vehiculos_cerca = 0
                                    #                  SEMAFORO, POSICIÓN SEMAFORO, HORIZONTAL, VERTICAL
                                    self.change_color(self.contadorSemaforos,"red","green")
                                    self.extra = True
                                    
                # 2. Si pocos vehículos(m o menos, >0) están por cruzar una luz verde a
                # una corta distancia r, no cambiar el semáforo
                
                elif(semaforo.is_green()):
                    self.cont1 =0
                    if(semaforo.direccion=="horizontal"):
                        if(self.vehicles_horizontal!=None):  
                            for vehicle in self.vehicles_horizontal:
                                if (semaforo.x > vehicle.x >= (semaforo.x -self.corta_distancia_r)):
                                    # Lo pongo así porque no tiene que cambiar
                                    self.cont1 = self.cont1 +1
                            if self.cont1>0:
                                self.change_color(self.contadorSemaforos,"green","red")
                                self.extra = True
                                        
                    else:
                        if(self.vehicles_vertical!=None):  
                            for vehicle in self.vehicles_vertical:
                                if (semaforo.y < vehicle.y <=(semaforo.y + self.corta_distancia_r)):
                                    self.cont1 = self.cont1 +1
                            if self.cont1>0:
                                self.change_color(self.contadorSemaforos,"red","green")
                                self.extra = True

                # 3. Si hay un vehiculo detenido en el camino a una corta distancia e 
                # más allá de una luz verde, cambiar el semaforo.

                    if semaforo.direccion == "horizontal":
                        if(self.vehicles_horizontal!=None):               
                            for vehicle in self.vehicles_horizontal:
                                if (semaforo.x+50)<=vehicle.x<=((semaforo.x+50)+self.corta_distancia_e):
                                    self.change_color(self.contadorSemaforos,"red","green")
                                    self.extra = True
                                    
                    else:
                        if(self.vehicles_vertical!=None):               
                            for vehicle in self.vehicles_vertical:
                                if (semaforo.y-50)>vehicle.y>=((semaforo.y-50)-self.corta_distancia_e):
                                    self.change_color(self.contadorSemaforos,"green","red")
                                    self.extra = True
                                    


                    # 4. Si hay vehiculos detenidos en ambas direcciones a una corta distancia 
                    # e más alla de la interseccion, entonces cambiar ambas luces a rojo.
                    # Cuando una de las direcciones se libere, restaurar la luz verde en esa direccion
                    self.cont2=0
                    self.cont1=0
                    if(self.vehicles_horizontal!=None): 
                        for vehicle in self.vehicles_horizontal:
                            if (semaforo.x+50)<=vehicle.x<=((semaforo.x+50)+self.corta_distancia_e):
                                self.cont1=1
                                break
                    if(self.vehicles_vertical!=None): 
                        for vehicle in self.vehicles_vertical:
                            if (semaforo.y-50)>vehicle.y>=((semaforo.y-50)-self.corta_distancia_e):
                                self.cont2=1
                                break
                    if(self.cont1==1 and self.cont2==1):
                        self.change_color(self.contadorSemaforos,"red","red")
                        self.extra = True
                        
                        self.cont1 =0
                        self.cont2 =0

                    # 5. Si no hay un vehiculo que se acerque a una luz verde a una distancia d
                    # y por lo menos unvehiculo se aproxima a una luz roja a una distancia d, 
                    # entonces cambair semaforo.
                        
                    if(semaforo.direccion=="horizontal"):
                        if(self.vehicles_horizontal!=None):               
                            for vehicle in self.vehicles_horizontal:
                                if semaforo.vehiculos_cerca==0:
                                    if self.semaforos[self.contadorSemaforos+1].vehiculos_cerca>0 and self.semaforos[self.contadorSemaforos+1].is_red():
                                            self.change_color(self.contadorSemaforos,"red","green")
                                            self.extra = True

                    elif(semaforo.direccion=="vertical"):
                        if(self.vehicles_vertical!=None):               
                            for vehicle in self.vehicles_vertical:
                                if semaforo.vehiculos_cerca==0:
                                    if self.semaforos[self.contadorSemaforos-1].vehiculos_cerca>0 and self.semaforos[self.contadorSemaforos-1].is_red():
                                        self.change_color(self.contadorSemaforos,"green","red")
                                        self.extra = True
                                        

                # Si no se cumple ninguna de las condiciones, entonces cambiarlos normal
                if self.extra==False:
                    if semaforo.is_red():
                        if semaforo.direccion=="horizontal":
                            self.change_color(self.contadorSemaforos,"green","red")
                            
                        else:
                            self.change_color(self.contadorSemaforos,"red","green")
                    else:
                        if semaforo.direccion=="horizontal":
                            self.change_color(self.contadorSemaforos,"red","green")

                        else:
                            self.change_color(self.contadorSemaforos,"green","red")

                self.extra = False
                self.contadorSemaforos +=1

    def change_color(self, pos, horizontal, vertical):
        if pos == 0 or pos == 1:
            self.semaforos[0].change_colores(horizontal)
            self.semaforos[1].change_colores(vertical)
        elif pos == 2 or pos == 3:
            self.semaforos[2].change_colores(horizontal)
            self.semaforos[3].change_colores(vertical)
        time.sleep(2)


    def run_vehicles(self):
        while True:
            self.generate_vehicles()
            # Esperar un tiempo antes de generar nuevos vehículos
            time.sleep(0.3)
            # Mover los vehículos
            self.move_vehicles()
            

    def move_vehicles(self):
        # Semaforos horizontales
        banderaCarro =False
        for vehicle in self.vehicles_horizontal:
            if 300 <= vehicle.x < 500:
                if self.semaforos[2].is_green():  # Si el semáforo está en verde
                    vehicle.move(60, 0)
                elif self.semaforos[2].is_red():  # Si el semáforo está en rojo
                    if 300 < vehicle.x < 400: 
                        destination_occupied = any(vehicle2.x == vehicle.x + 60 and vehicle2.y == vehicle.y for vehicle2 in self.vehicles_horizontal)
                        if not destination_occupied:
                            vehicle.move(60, 0)
                    elif vehicle.x>=530:  # Verificar si el vehículo está más allá del borde izquierdo
                        vehicle.move(60, 0)

            elif 16 <= vehicle.x < 230:
                if self.semaforos[0].is_green():  # Si el semáforo está en verde
                    vehicle.move(60, 0)
                elif self.semaforos[0].is_red():  # Si el semáforo está en rojo
                    if 16 < vehicle.x < 160: 
                        destination_occupied = any(vehicle2.x == vehicle.x + 60 and vehicle2.y == vehicle.y for vehicle2 in self.vehicles_horizontal)
                        if not destination_occupied:
                            vehicle.move(60, 0)
                    elif vehicle.x>=220:  # Verificar si el vehículo está más allá del borde izquierdo
                        vehicle.move(60, 0)
            else:
                vehicle.move(60, 0)
                
        #Semaforos verticles   
        for vehicle in self.vehicles_vertical:
            if 90 <= vehicle.y < 180 and 298>vehicle.x>212:
                if self.semaforos[1].is_green():  # Si el semáforo está en rojo
                    vehicle.move(0, -60)
                elif self.semaforos[1].is_red():
                    if 90 < vehicle.y < 110: 
                        destination_occupied = any(vehicle2.y == vehicle.y - 60 and vehicle2.x == vehicle.x for vehicle2 in self.vehicles_vertical)
                        if not destination_occupied:
                            vehicle.move(0,-60)
                    elif vehicle.x<=-10:  # Verificar si el vehículo está más allá del borde izquierdo
                        vehicle.move(0,-60)
            elif 94 <= vehicle.y < 150 and 566>vehicle.x>499:
                if self.semaforos[3].is_green():  # Si el semáforo está en rojo
                    vehicle.move(0, -60) 
                elif self.semaforos[3].is_red():
                    if 90 < vehicle.y < 110: 
                        destination_occupied = any(vehicle2.y == vehicle.y - 60 and vehicle2.x == vehicle.x for vehicle2 in self.vehicles_vertical)
                        if not destination_occupied:
                            vehicle.move(0,-60)
                    elif vehicle.x<=-10:  # Verificar si el vehículo está más allá del borde izquierdo
                        vehicle.move(0,-60)
            else:
                vehicle.move(0, -60)

        for vehicle in self.vehicles_vertical:
            if vehicle.y<-10:
                self.vehicles_vertical.remove(vehicle)
        for vehicle in self.vehicles_horizontal:
            if vehicle.x>=780:
                self.vehicles_horizontal.remove(vehicle)


    def generate_vehicles(self):
        direction = random.choice(["horizontal", "vertical", "vertical","vertical","vertical"])
        if direction == "horizontal":
            x = random.randint(0, 2)
            y = random.choice([40, 65])
        else:
            x = random.choice([230, 260, 510, 540])
            y = random.randint(470, 473)
        vehicle = Vehicle(self.canvas, x=x, y=y, width=20, height=10, direction=direction)
        if direction == "horizontal":
            self.vehicles_horizontal.append(vehicle)
        else:
            self.vehicles_vertical.append(vehicle)

def inicializarCruces(canvas):
    canvas.create_rectangle(10, 10, 200, 20, fill="white")
    canvas.create_rectangle(10, 100, 200, 110, fill="white")

    canvas.create_rectangle(200, 100, 210, 300, fill="white")
    canvas.create_rectangle(290, 100, 300, 300, fill="white")
    
    canvas.create_rectangle(290, 10, 480, 20, fill="white")
    canvas.create_rectangle(290, 100, 480, 110, fill="white")

    canvas.create_rectangle(470, 100, 480, 300, fill="white")
    canvas.create_rectangle(560, 100, 570, 300, fill="white")

    canvas.create_rectangle(560, 10, 780, 20, fill="white")
    canvas.create_rectangle(560, 100, 780, 110, fill="white")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Simulación de tráfico")
    app = SemaphorSimulation(root)
    root.mainloop()