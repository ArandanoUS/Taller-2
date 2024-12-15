from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de SQLAlchemy y MariaDB
DATABASE_URL = "mysql+mysqlconnector://recetas_user:password@localhost/recetas"

# Base de datos y ORM
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Modelo ORM para la tabla de recetas
class Receta(Base):
    __tablename__ = "recetas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    ingredientes = Column(String(1000), nullable=False)
    pasos = Column(String(2000), nullable=False)

# Crear la base de datos si no existe
def inicializar_db():
    Base.metadata.create_all(bind=engine)

# Funciones de CRUD
def agregar_receta():
    """Agregar una nueva receta."""
    session = SessionLocal()
    try:
        nombre = input("Nombre de la receta: ")
        ingredientes = input("Ingredientes (separados por comas): ")
        pasos = input("Pasos de la receta: ")

        nueva_receta = Receta(nombre=nombre, ingredientes=ingredientes, pasos=pasos)
        session.add(nueva_receta)
        session.commit()
        print("✅ Receta agregada exitosamente.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        session.close()

def actualizar_receta():
    """Actualizar una receta existente."""
    session = SessionLocal()
    try:
        nombre = input("Nombre de la receta a actualizar: ")
        receta = session.query(Receta).filter(Receta.nombre == nombre).first()

        if receta:
            print(f"Receta encontrada:\nIngredientes: {receta.ingredientes}\nPasos: {receta.pasos}")
            nuevo_ingredientes = input("Nuevos ingredientes (dejar en blanco para no cambiar): ")
            nuevo_pasos = input("Nuevos pasos (dejar en blanco para no cambiar): ")

            if nuevo_ingredientes:
                receta.ingredientes = nuevo_ingredientes
            if nuevo_pasos:
                receta.pasos = nuevo_pasos

            session.commit()
            print("✅ Receta actualizada exitosamente.")
        else:
            print("❌ No se encontró la receta especificada.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        session.close()

def eliminar_receta():
    """Eliminar una receta existente."""
    session = SessionLocal()
    try:
        nombre = input("Nombre de la receta a eliminar: ")
        receta = session.query(Receta).filter(Receta.nombre == nombre).first()

        if receta:
            session.delete(receta)
            session.commit()
            print("✅ Receta eliminada exitosamente.")
        else:
            print("❌ No se encontró la receta especificada.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        session.close()

def ver_listado_recetas():
    """Mostrar el listado de todas las recetas."""
    session = SessionLocal()
    try:
        recetas = session.query(Receta).all()
        if recetas:
            print("📜 Listado de recetas:")
            for i, receta in enumerate(recetas, start=1):
                print(f"{i}. {receta.nombre}")
        else:
            print("❌ No hay recetas disponibles.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        session.close()

def buscar_receta():
    """Buscar los detalles de una receta específica."""
    session = SessionLocal()
    try:
        nombre = input("Nombre de la receta a buscar: ")
        receta = session.query(Receta).filter(Receta.nombre == nombre).first()

        if receta:
            print(f"📖 Receta: {receta.nombre}")
            print(f"Ingredientes: {receta.ingredientes}")
            print(f"Pasos: {receta.pasos}")
        else:
            print("❌ No se encontró la receta especificada.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        session.close()

# Menú principal
def menu():
    """Mostrar el menú principal y gestionar las opciones del usuario."""
    while True:
        print("\n=== Libro de Recetas ===")
        print("1. Agregar nueva receta")
        print("2. Actualizar receta existente")
        print("3. Eliminar receta existente")
        print("4. Ver listado de recetas")
        print("5. Buscar ingredientes y pasos de receta")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_receta()
        elif opcion == "2":
            actualizar_receta()
        elif opcion == "3":
            eliminar_receta()
        elif opcion == "4":
            ver_listado_recetas()
        elif opcion == "5":
            buscar_receta()
        elif opcion == "6":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    inicializar_db()
    menu()
