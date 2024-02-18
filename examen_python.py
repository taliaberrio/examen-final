import pickle


class Libro:
    def __init__(self, titulo, autor, cantidad=1):
        self.titulo = titulo
        self.autor = autor
        self.cantidad = cantidad
        self.disponible = True


class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre


class Biblioteca:
    def __init__(self):
        self.libros = {}
        self.usuarios = {}
        self.cargar_datos()

    def agregar_libro(self, titulo, autor):
        if titulo in self.libros:
            self.libros[titulo].cantidad += 1
        else:
            self.libros[titulo] = Libro(titulo, autor)

    def mostrar_libros(self):
        for libro in self.libros.values():
            disponibilidad = "Disponible" if libro.disponible else "No disponible"
            print(
                f"{libro.titulo} - {libro.autor} - Cantidad: {libro.cantidad} - {disponibilidad}"
            )

    def prestar_libro(self, titulo, nombre_usuario):
        if nombre_usuario not in self.usuarios:
            print("Usuario no registrado. Por favor, regístrese primero.")
            return

        if titulo in self.libros and self.libros[titulo].disponible:
            self.libros[titulo].disponible = False
            print(f"Libro '{titulo}' prestado a {nombre_usuario}")
        else:
            print("Libro no disponible")

    def registrar_usuario(self, nombre):
        self.usuarios[nombre] = Usuario(nombre)
        print(f"Usuario {nombre} registrado")

    def guardar_datos(self):
        with open("datos_biblioteca.pkl", "wb") as f:
            pickle.dump((self.libros, self.usuarios), f)

    def cargar_datos(self):
        try:
            with open("datos_biblioteca.pkl", "rb") as f:
                self.libros, self.usuarios = pickle.load(f)
        except FileNotFoundError:
            pass

    def listar_usuarios(self):
        for usuario in self.usuarios.values():
            print(usuario.nombre)

    def listar_libros_usuario(self, nombre_usuario):
        for libro in self.libros.values():
            if not libro.disponible:
                print(libro.titulo)

    def devolver_libro(self, titulo):
        if titulo in self.libros and not self.libros[titulo].disponible:
            self.libros[titulo].disponible = True
            print(f"Libro '{titulo}' devuelto correctamente")
        else:
            print("El libro no puede ser devuelto")


def menu():
    print("=" * 80)
    print("Bienvenido al sistema de gestión de biblioteca".center(80))
    print("=" * 80)
    print(" 1. Agregar libro")
    print(" 2. Mostrar libros")
    print(" 3. Prestar libro")
    print(" 4. Registrar usuario")
    print(" 5. Listar usuarios")
    print(" 6. Listar libros de usuario")
    print(" 7. Devolver libro")
    print(" 8. Salir")


biblioteca = Biblioteca()

while True:
    menu()
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        titulo = input("Ingrese el título del libro: ")
        autor = input("Ingrese el autor del libro: ")
        biblioteca.agregar_libro(titulo, autor)
        biblioteca.guardar_datos()

    elif opcion == "2":
        biblioteca.mostrar_libros()

    elif opcion == "3":
        titulo = input("Ingrese el título del libro a prestar: ")
        nombre_usuario = input("Ingrese el nombre del usuario: ")
        biblioteca.prestar_libro(titulo, nombre_usuario)
        biblioteca.guardar_datos()

    elif opcion == "4":
        nombre_usuario = input("Ingrese el nombre del nuevo usuario: ")
        biblioteca.registrar_usuario(nombre_usuario)
        biblioteca.guardar_datos()

    elif opcion == "5":
        print("Usuarios registrados:")
        biblioteca.listar_usuarios()

    elif opcion == "6":
        nombre_usuario = input("Ingrese el nombre del usuario: ")
        print(f"Libros prestados a {nombre_usuario}:")
        biblioteca.listar_libros_usuario(nombre_usuario)

    elif opcion == "7":
        titulo = input("Ingrese el título del libro a devolver: ")
        biblioteca.devolver_libro(titulo)
        biblioteca.guardar_datos()

    elif opcion == "8":
        break

    else:
        print("Opción no válida")

print("¡Gracias por usar el sistema de gestión de biblioteca!")
